import MovieCard from "../components/MovieCard";
import ClusterAnalyticsCard from "../components/ClusterAnalyticsCard";

export default function ResultsPage({ result, onRestart }) {
  const { cluster, movies } = result;

  return (
    <div className="min-h-screen px-6 py-16 flex flex-col items-center">
      <div className="w-full max-w-4xl">
        <h1 className="font-display text-4xl text-paper text-center mb-2">
          Твої 5 фільмів
        </h1>
        <p className="text-sm text-muted text-center mb-10">
          Підібрано на основі твоїх відповідей
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10">
          {movies.map((movie) => (
            <MovieCard key={movie.tconst} movie={movie} />
          ))}
        </div>

        <ClusterAnalyticsCard cluster={cluster} />

        <div className="flex justify-center mt-10">
          <button
            type="button"
            onClick={onRestart}
            className="font-body text-sm font-medium bg-marquee text-ink px-8 py-3 rounded-full hover:bg-marquee/90 transition-colors"
          >
            Пройти квіз ще раз
          </button>
        </div>
      </div>
    </div>
  );
}
