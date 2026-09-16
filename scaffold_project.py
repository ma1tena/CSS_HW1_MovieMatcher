"""
scaffold_project.py

Створює повну структуру папок і базові файли для проєкту
"Movie Vector Matcher" (backend + frontend + docs).

Запуск (з кореня твого репозиторію, тобто з папки, яку ти вже
підключила до GitHub):

    python scaffold_project.py

Скрипт нічого не перезаписує: якщо файл/папка вже існує — пропускає її.
"""

import os

# ---- Структура папок ----------------------------------------------------
DIRS = [
    "backend/app",
    "backend/ml",
    "backend/data/raw",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/public",
    "docs/screenshots",
]

# ---- Файли-заглушки з базовим контентом ---------------------------------
FILES = {
    "README.md": """# Movie Vector Matcher

Інтерактивний вебдодаток-рекомендатель фільмів на основі датасету IMDb.
Користувач проходить короткий квіз (настрій, динаміка, тривалість, епоха,
якірний фільм), бекенд формує User Vector, знаходить кластер через KMeans
і повертає 5 найближчих фільмів через cosine similarity.

## Структура проєкту

- `backend/` — FastAPI + ML (навчання моделі, inference, API)
- `frontend/` — React + Vite + Tailwind CSS (квіз + сторінка результатів)
- `docs/` — скріншоти, нотатки, допоміжна документація

## Запуск бекенду

```bash
cd backend
pip install -r requirements.txt
python ml/train_model.py --basics data/raw/title.basics.tsv.gz --ratings data/raw/title.ratings.tsv.gz
uvicorn app.main:app --reload
```

## Запуск фронтенду

```bash
cd frontend
npm install
npm run dev
```

## Деплой

- Backend -> Render (`backend/Procfile`, `backend/requirements.txt`)
- Frontend -> Vercel (`frontend/vercel.json`)

## Статус розробки (майлстони)

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

# ML-артефакти та сирі дані (великі файли, не в git)
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
            print(f"[skip] {path} (вже існує)")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[file] {path}")


if __name__ == "__main__":
    print("Створення структури проєкту Movie Vector Matcher...\n")
    make_dirs()
    make_files()
    print("\nГотово! Структуру створено в поточній директорії.")
