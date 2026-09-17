import { ANCHOR_MOVIES } from "../quizData";

export default function AnchorMovieCarousel({ value, onChange }) {
  return (
    <div className="w-full max-w-2xl">
      <h2 className="font-display text-3xl leading-snug text-paper mb-3 text-center">
        Який із цих фільмів тобі найближчий?
      </h2>
      <p className="text-sm text-muted text-center mb-10">
        Ми відштовхнемось від нього, щоб знайти схожі фільми
      </p>

      <div className="flex gap-4 overflow-x-auto pb-4 px-1 snap-x snap-mandatory">
        {ANCHOR_MOVIES.map((movie) => {
          const selected = value === movie.title;
          return (
            <button
              key={movie.title}
              type="button"
              onClick={() => onChange(movie.title)}
              className={`snap-start shrink-0 w-44 text-left rounded-lg border px-4 py-5 transition-colors ${
                selected
                  ? "border-marquee bg-marqueeDim"
                  : "border-hairline bg-surface hover:border-marquee/40"
              }`}
            >
              <div className="text-xs text-muted font-body mb-3">{movie.year}</div>
              <div className="font-display text-lg leading-tight text-paper mb-2">
                {movie.title}
              </div>
              <div className="text-xs text-muted">{movie.blurb}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
