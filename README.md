# Local Setup instructions

1) Install [npm](https://nodejs.org/en/download/)

```bash
npm install -g npm
```

2) Install npx

```bash
npm install -g npx
```

3) Install IDOM

```bash
pip install "idom[stable]"
```

4) Install Tailwind CSS
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

5) Install FastAPI

```bash
pip install FastAPI
```

6) Spin up the backend Fastapi dev server

```bash
cd timesheets
uvicorn backend.main:app --reload
```

7) Spin up the frontend IDOM dev server
```bash
cd timesheets/idom_frontend
python3 -m run_reload.py
```
8) Compile the tailwind css file

```bash
cd idom_frontend/tailwind
npm run build
```
9) Open a git bash terminal
10) Run `sh build.sh`
11) Run `docker-compose up`
