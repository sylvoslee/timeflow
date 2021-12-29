# Local Setup instructions

1) Install [npm](https://nodejs.org/en/download/)

2) Install npx

```bash
npm install -g npx
```

3) Install [lowdefy](https://docs.lowdefy.com/tutorial-start)

4) Install FastAPI

```bash
pip install FastAPI
```

5) Spin up the lowdefy development server

```bash
cd frontend
npx lowdefy@latest dev
```

6) Spin up the backend Fastapi dev server

```bash
cd timesheets
uvicorn backend.main:app --reload
```