"""
scaffold_project.py

Creates the full folder structure and base files for the
"Movie Vector Matcher" project (backend + frontend + docs).

Usage (run from the root of your repo, i.e. the folder
already connected to GitHub):

    python scaffold_project.py

The script never overwrites existing files/folders: if something
already exists, it is skipped.
"""

import os

# ---- Folder structure ---------------------------------------------------
DIRS = [
    "backend/app",
    "backend/ml",
    "backend/data/raw",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/public",
    "docs/screenshots",
]

# ---- Placeholder files with base content --------------------------------
FILES = {
    "README.md": """# Movie Vector Matcher

Interactive movie-recommendation web app based on the IMDb dataset.
The user goes through a short quiz (mood, pace, runtime, era, anchor
movie), the backend builds a User Vector, finds the user's cluster
via KMeans, and returns the 5 closest movies via cosine similarity.

## Project structure

- `backend/` — FastAPI + ML (model training, inference, API)
- `frontend/` — React + Vite + Tailwind CSS (quiz + results page)
- `docs/` — screenshots, notes, supporting documentation

## Running the backend

```bash
cd backend
pip install -r requirements.txt
python ml/train_model.py --basics data/raw/title.basics.tsv.gz --ratings data/raw/title.ratings.tsv.gz
uvicorn app.main:app --reload
```

## Running the frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

- Backend -> Render (`backend/Procfile`, `backend/requirements.txt`)
- Frontend -> Vercel (`frontend/vercel.json`)

## Milestone status

- [x] Milestone 1 — Data Prep & Training Script
- [ ] Milestone 2 — Backend API (FastAPI + ML Inference)
- [ ] Milestone 3 — Frontend Quiz
- [ ] Milestone 4 — Results & Analytics UI
- [ ] Milestone 5 — Deployment Config
""",
    ".gitignore": """# Python
__pycache__/
*.pyc
.venv/
venv/

# ML artifacts and raw data (large files, not in git)
backend/data/raw/*
!backend/data/raw/.gitkeep
backend/ml/*.pkl
backend/ml/*.parquet

# Node / frontend
frontend/node_modules/
frontend/dist/
frontend/.vite/

# Env
.env
.env.local

# OS / IDE
.DS_Store
.vscode/
.idea/
""",
    "backend/requirements.txt": """fastapi
uvicorn[standard]
pandas
scikit-learn
joblib
pyarrow
python-multipart
""",
    "backend/Procfile": "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT\n",
    "backend/data/raw/.gitkeep": "",
    "backend/app/__init__.py": "",
    "frontend/vercel.json": """{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
""",
}


def make_dirs():
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
        print(f"[dir]  {d}")


def make_files():
    for path, content in FILES.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if os.path.exists(path):
            print(f"[skip] {path} (already exists)")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[file] {path}")


if __name__ == "__main__":
    print("Creating Movie Vector Matcher project structure...\n")
    make_dirs()
    make_files()
    print("\nDone! Structure created in the current directory.")
