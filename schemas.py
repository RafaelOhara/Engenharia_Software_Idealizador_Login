from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    nome: str
    sobrenome: str
    CPF: str
    nomeUsuario: str
    telefone: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str
