// Slider questions (1-5 scale). Keep in sync with backend/app/recommend.py.
export const SLIDER_QUESTIONS = [
  {
    key: "mood",
    question: "Наскільки легкий настрій тобі потрібен?",
    lowLabel: "Серйозний, важкий",
    highLabel: "Легкий, веселий",
  },
  {
    key: "action",
    question: "Наскільки динамічним має бути фільм?",
    lowLabel: "Повільний, споглядальний",
    highLabel: "Багато екшену",
  },
  {
    key: "duration",
    question: "Наскільки довгим має бути фільм?",
    lowLabel: "Коротший (~85 хв)",
    highLabel: "Довший (~155 хв)",
  },
];

export const ERA_OPTIONS = [
  { key: "before2000", label: "До 2000", hint: "Класика" },
  { key: "2000-2015", label: "2000–2015", hint: "Нульові й десяті" },
  { key: "2016+", label: "2016+", hint: "Сучасне кіно" },
];

// Must match ANCHOR_MOVIES in backend/app/recommend.py exactly.
// 5 very popular titles, each from a distinct genre, so any answer
// in the quiz has a clear, high-vote-count anchor to pull from.
export const ANCHOR_MOVIES = [
  { title: "The Dark Knight", year: 2008, blurb: "Темний, напружений екшн-трилер" },
  { title: "Fight Club", year: 1999, blurb: "Жорстка, атмосферна драма" },
  { title: "Superbad", year: 2007, blurb: "Шалена комедія" },
  { title: "Interstellar", year: 2014, blurb: "Епічна космічна фантастика" },
  { title: "Titanic", year: 1997, blurb: "Велика романтична драма" },
];
