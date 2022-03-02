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

# Docker instructions
* Open a git bash terminal
* Ensure you are in the root directory of the project
* Run `sh build.sh`
* Run `docker-compose up`

# Notes
* Make sure to run `npm run build` to build the CSS before building the Docker images
* the `base_url` variable has to be modified in **idom_frontend/config.py** depending on the set up:
  * While the service is being run on the server, change `base_url` to `http://165.232.72.164:8000`
  * While the service is being run locally only, change `base_url` to `http://127.0.0.1:8000`
