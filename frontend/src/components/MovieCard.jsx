function matchColor(percent) {
  if (percent >= 85) return "text-marquee";
  if (percent >= 70) return "text-paper";
  return "text-muted";
}

export default function MovieCard({ movie }) {
  return (
    <div className="rounded-lg border border-hairline bg-surface p-6 flex flex-col gap-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-display text-xl leading-tight text-paper">{movie.title}</h3>
          <p className="text-sm text-muted mt-1">{movie.year}</p>
        </div>
        <div
          className={`shrink-0 font-body text-sm font-semibold ${matchColor(
            movie.match_percent
          )}`}
        >
          {movie.match_percent}% Match
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {movie.genres.split(",").map((genre) => (
          <span
            key={genre}
            className="text-xs text-muted border border-hairline rounded-full px-3 py-1"
          >
            {genre}
          </span>
        ))}
      </div>

      <div className="flex items-center gap-2 text-sm text-paper mt-auto pt-2 border-t border-hairline">
        <span className="text-marquee">★</span>
        <span className="font-medium">{movie.rating.toFixed(1)}</span>
        <span className="text-muted">IMDb · {movie.runtime} хв</span>
      </div>
    </div>
  );
}
