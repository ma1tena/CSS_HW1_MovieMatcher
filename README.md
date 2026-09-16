# Movie Vector Matcher

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
