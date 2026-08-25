# +Aula — Sistema de Gestão de Aulas

Projeto em Python com Flask, arquitetura em camadas e frontend integrado. O projeto foi ajustado de acordo com o diagrama fornecido: **usuario → turma → atividade → entrega**.

## Como executar

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abra `http://localhost:5000`.

Sem configuração adicional o sistema usa SQLite automaticamente e cria o arquivo `backend/mais_aulas.db`. Para MySQL, copie `.env.example` para `.env`, configure `DATABASE_URL` e crie o banco com `backend/database/create_database.sql`.

## Arquitetura

```text
backend/
  controllers/
  services/
  models/
  repositories/
frontend/
  templates/
  static/
```

Fluxo de cada funcionalidade:

**Interface → API Flask → Controller → Service → Model/Repository → Banco de Dados**

As controllers são classes. Cada caso de uso possui sua própria classe Service. Os CRUDs básicos ficam nas Models por meio de `salvar`, `atualizar`, `deletar`, `listar_todos` e `buscar_por_id`. O Repository é utilizado no resumo do dashboard.

## Funcionalidades Implementadas

1. Cadastrar usuário
2. Listar usuários
3. Atualizar usuário
4. Excluir usuário
5. Cadastrar turma
6. Listar turmas
7. Atualizar turma
8. Cadastrar atividade
9. Listar atividades
10. Atualizar atividade
11. Excluir atividade
12. Registrar entrega
13. Listar entregas
14. Atualizar entrega
15. Excluir entrega
16. Consultar resumo do dashboard

Todas possuem fluxo completo do frontend até o banco de dados.

## Rotas principais

- `GET/POST /api/usuarios`
- `PUT/DELETE /api/usuarios/<id>`
- `GET/POST /api/turmas`
- `PUT/DELETE /api/turmas/<id>`
- `GET/POST /api/atividades`
- `PUT/DELETE /api/atividades/<id>`
- `GET/POST /api/entregas`
- `PUT/DELETE /api/entregas/<id>`
- `GET /api/dashboard`
- `GET /api/health`
