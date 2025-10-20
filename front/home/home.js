    const apiUrl = "/api/team"; // ajuste se necessário
    const teamGrid = document.getElementById("teamGrid");
    const teamCount = document.getElementById("teamCount");
    const tpl = document.getElementById("memberCardTpl");
    const searchInput = document.getElementById("searchInput");
    const searchBtn = document.getElementById("searchBtn");
    document.getElementById("year").textContent = new Date().getFullYear();

    let members = [];

    function initials(name = "") {
      return name.split(" ").map(s => s[0]?.toUpperCase() || "").slice(0,2).join("");
    }

    function normalizeApiTeamResponse(data) {
      if (!Array.isArray(data)) return [];
      return data.map((row, idx) => ({
        id: String(row.id ?? idx),
        name: row.name ?? row.nome ?? "Membro",
        role: row.role ?? row.cargo ?? "Colaborador",
        experienceYears: row.experienceYears ?? row.anosExperiencia ?? null,
        avatarUrl: row.avatarUrl ?? row.fotoUrl ?? null,
        status: row.status ?? "offline",
        specialties: (row.specialties ?? row.especialidades ?? []).map(s => ({
          code: String(s.code ?? s.sigla ?? "SP"),
          label: String(s.label ?? s.nome ?? "Especialidade"),
          level: Number(s.level ?? s.nivel ?? 3)
        })),
        skills: (row.skills ?? row.habilidades ?? []).map(String),
        bio: row.bio ?? row.descricao ?? ""
      }));
    }

    function render(list) {
      teamGrid.innerHTML = "";
      list.forEach(m => {
        const node = tpl.content.cloneNode(true);

        const avatar = node.querySelector(".avatar");
        if (m.avatarUrl) {
          const img = document.createElement("img");
          img.src = m.avatarUrl; img.alt = m.name;
          avatar.textContent = ""; avatar.appendChild(img);
        } else {
          avatar.textContent = initials(m.name);
        }

        node.querySelector(".name").textContent = m.name;
        node.querySelector(".role").textContent = m.role;
        node.querySelector(".xps").textContent = m.experienceYears != null ? `${m.experienceYears}+ anos de experiência` : "";
        node.querySelector(".status-dot").setAttribute("data-status", m.status);

        const specs = node.querySelector(".specialties");
        m.specialties?.forEach(s => {
          const pill = document.createElement("span");
          pill.className = "pill";
          pill.title = s.label;
          pill.innerHTML = `<strong>${s.code}</strong> <span class="dots">${[0,1,2,3,4].map(i => `<span class="dot ${i < s.level ? "active" : ""}"></span>`).join("")}</span>`;
          specs.appendChild(pill);
        });

        const skills = node.querySelector(".skills");
        m.skills?.forEach(t => {
          const tag = document.createElement("span");
          tag.className = "tag";
          tag.textContent = t;
          skills.appendChild(tag);
        });

        node.querySelector(".bio").textContent = m.bio ?? "";
        teamGrid.appendChild(node);
      });
      teamCount.textContent = `${list.length} colaborador${list.length === 1 ? "" : "es"}`;
    }

    async function load() {
      try {
        const res = await fetch(apiUrl, { headers: { "Content-Type": "application/json" }});
        if (!res.ok) throw new Error("HTTP " + res.status);
        const data = await res.json();
        members = normalizeApiTeamResponse(data);
      } catch (e) {
        members = [
          { id:"1", name:"Sarah Chen", role:"Full Stack", experienceYears:5, avatarUrl:null, status:"online", specialties:[{code:"FR", label:"Frontend", level:4}], skills:["React","TS"], bio:"" },
          { id:"2", name:"Marcus Johnson", role:"DevOps", experienceYears:7, avatarUrl:null, status:"busy", specialties:[{code:"NU", label:"Nuvem", level:3}], skills:["Docker","K8s"], bio:"" }
        ];
      }
      render(members);
    }

    function doSearch() {
      const q = (searchInput.value || "").toLowerCase();
      if (!q) return render(members);
      const filtered = members.filter(m =>
        m.name.toLowerCase().includes(q) ||
        m.role.toLowerCase().includes(q) ||
        (m.bio || "").toLowerCase().includes(q) ||
        m.skills?.some(s => s.toLowerCase().includes(q)) ||
        m.specialties?.some(s => s.label.toLowerCase().includes(q) || s.code.toLowerCase().includes(q))
      );
      render(filtered);
    }

    searchBtn.addEventListener("click", doSearch);
    searchInput.addEventListener("keyup", (e) => { if (e.key === "Enter") doSearch(); });

    load();