# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
import sqlite3
from schemas import Token, UserCreate, UserOut, UserLogin, UserWithToken
from auth import create_token, verify_token


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/front", StaticFiles(directory="front"), name="front")


DB_PATH = "micro_db/database_login.db"


pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

@app.post("/register", response_model=dict)
def register(user_in: UserCreate):
    try:
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            # Verifica email
            cursor.execute("SELECT email FROM usuarios WHERE email = ?", (user_in.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email já cadastrado")
            # Verifica nome_usuario
            cursor.execute("SELECT nome_usuario FROM usuarios WHERE nome_usuario = ?", (user_in.nomeUsuario,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado")
            cursor.execute(
                "INSERT INTO usuarios (email, senha_hash, nome, sobrenome, nome_usuario, cpf, telefone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_in.email, hash_password(user_in.password), user_in.nome, user_in.sobrenome, user_in.nomeUsuario, user_in.CPF, user_in.telefone)
            )
            conn.commit()
            print(f"Usuário criado: {user_in.email}")
            return {"email": user_in.email}
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Erro de integridade: " + str(e))

@app.post("/login", response_model=Token)
def login(user_in: UserLogin):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT senha_hash,nome_usuario FROM usuarios WHERE email = ?", (user_in.email,))
    row = cursor.fetchone()
    conn.close()
    if not row or not verify_password(user_in.password, row[0]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    _,nome_usuario = row
    token_data = {"sub": user_in.email, "email": user_in.email, "nome_usuario": nome_usuario}
    access_token = create_token(token_data)
    return {"access_token": access_token, "token_type":"bearer"}

@app.get("/user/{email}", response_model=UserWithToken)
def get_user_by_email(email: str, request: Request):
    # Verifica o token JWT no header Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação ausente")
    token = auth_header.split(" ", 1)[1]
    try:
        verify_token(token)
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM usuarios WHERE email = ?", (email,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return {"email": row[0], "access_token": token}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





