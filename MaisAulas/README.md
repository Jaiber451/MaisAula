# +Aula — Sistema de Gestão Escolar

Projeto full-stack inspirado na referência visual enviada, com **frontend + backend Flask + MySQL**, seguindo a arquitetura em camadas solicitada:

- `controllers/` — recebe requisições HTTP e devolve respostas.
- `services/` — casos de uso e regras da aplicação.
- `models/` — entidades do domínio e CRUD básico via Flask-SQLAlchemy.
- `repositories/` — consultas específicas/complexas e chamadas de procedures.
- `database/` — script de criação do banco, tabelas, dados iniciais e procedures.
- `frontend/` — telas para dashboard, listagem, cadastro, edição e exclusão.

## 1. Requisitos

- Python 3.11+
- MySQL 8.0+
- Navegador moderno
- Git (opcional)

## 2. Estrutura

```text
aula-conectada/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── activity_controller.py
│   │   ├── announcement_controller.py
│   │   ├── class_controller.py
│   │   ├── dashboard_controller.py
│   │   ├── student_controller.py
│   │   ├── subject_controller.py
│   │   └── teacher_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── activity.py
│   │   ├── announcement.py
│   │   ├── school_class.py
│   │   ├── student.py
│   │   ├── subject.py
│   │   └── teacher.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── activity_repository.py
│   │   ├── dashboard_repository.py
│   │   └── student_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── activity_service.py
│   │   ├── announcement_service.py
│   │   ├── class_service.py
│   │   ├── dashboard_service.py
│   │   ├── student_service.py
│   │   ├── subject_service.py
│   │   └── teacher_service.py
│   └── database/
│       └── create_database.sql
├── docker-compose.yml
└── .gitignore
```

## 3. Banco de dados

### Opção A — Docker

Na raiz do projeto:

```bash
docker compose up -d db
```

O MySQL ficará disponível em `localhost:3306`.

O `create_database.sql` é montado automaticamente no container e cria:
- banco `aula_conectada`;
- tabelas;
- relacionamentos;
- índices;
- dados iniciais;
- procedures para consultas complexas.

### Opção B — MySQL instalado localmente

Execute o arquivo:

```bash
mysql -u root -p < backend/database/create_database.sql
```

## 4. Backend

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale:

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e ajuste usuário/senha:

```env
DATABASE_URL=mysql+pymysql://root:root@127.0.0.1:3306/aula_conectada
```

Execute:

```bash
python app.py
```

API: `http://localhost:5000`

Health check:

`GET /api/health`

## 5. Frontend

Com o backend rodando, abra:

```text
frontend/index.html
```

Para evitar restrições de `file://`, é recomendado servir a pasta com um servidor simples:

```bash
cd frontend
python -m http.server 5500
```

Acesse `http://localhost:5500`.

O frontend chama a API em `http://localhost:5000/api`.

## 6. CRUD implementado

### Students
- `GET /api/students`
- `GET /api/students/<id>`
- `POST /api/students`
- `PUT /api/students/<id>`
- `DELETE /api/students/<id>`

### Teachers
- `GET /api/teachers`
- `GET /api/teachers/<id>`
- `POST /api/teachers`
- `PUT /api/teachers/<id>`
- `DELETE /api/teachers/<id>`

### Subjects
- `GET /api/subjects`
- `GET /api/subjects/<id>`
- `POST /api/subjects`
- `PUT /api/subjects/<id>`
- `DELETE /api/subjects/<id>`

### Classes
- `GET /api/classes`
- `GET /api/classes/<id>`
- `POST /api/classes`
- `PUT /api/classes/<id>`
- `DELETE /api/classes/<id>`

### Activities
- `GET /api/activities`
- `GET /api/activities/<id>`
- `POST /api/activities`
- `PUT /api/activities/<id>`
- `DELETE /api/activities/<id>`

### Announcements
- `GET /api/announcements`
- `GET /api/announcements/<id>`
- `POST /api/announcements`
- `PUT /api/announcements/<id>`
- `DELETE /api/announcements/<id>`

## 7. Funcionalidades além do CRUD

Foram implementadas consultas específicas na camada Repository e encapsuladas em procedures MySQL:

- Filtro, busca e ordenação de atividades:
  - `GET /api/reports/activities?subject_id=1&status=pending&search=matematica&sort=due_date&direction=asc`
- Desempenho do aluno:
  - `GET /api/reports/students/<student_id>/performance`
- Dashboard:
  - `GET /api/dashboard?student_id=1`

As procedures principais são:

- `sp_list_activities_filtered`
- `sp_student_performance`
- `sp_dashboard_summary`

Assim, `Model` fica responsável pelo CRUD básico e o `Repository` encapsula consultas de negócio que vão além do CRUD.

## 8. Frontend

A interface inclui:

- Dashboard com próximas aulas, atividades pendentes, avisos e desempenho;
- menu lateral;
- telas de gerenciamento de alunos, professores, disciplinas, turmas, atividades e avisos;
- formulários de cadastro/edição;
- exclusão;
- filtros de atividades;
- tela de relatório/desempenho;
- mensagens e calendário visuais;
- layout responsivo inspirado na imagem de referência.

## 9. GitHub

Depois de validar o projeto:

```bash
git init
git add .
git commit -m "Implementa arquitetura full-stack +Aula"
git branch -M main
git remote add origin SEU_REPOSITORIO
git push -u origin main
```

Na entrega do Classroom, informe o link do repositório.

## 10. Observação sobre procedures

As procedures estão no script `backend/database/create_database.sql`. Para mudar as regras de consultas complexas, altere as procedures e a camada Repository, mantendo Models e Services desacoplados.

## 11. Credenciais de demonstração

Os dados iniciais são apenas dados fictícios para desenvolvimento. Não há autenticação real implementada nesta etapa.
