const ERA_LABELS = {
  before2000: "До 2000",
  "2000-2015": "2000–2015",
  "2016+": "2016+",
};

export default function ClusterAnalyticsCard({ cluster }) {
  const eraEntries = Object.entries(cluster.era_distribution);
  const maxEra = Math.max(...eraEntries.map(([, v]) => v));

  return (
    <div className="rounded-lg border border-hairline bg-surface p-8">
      <p className="text-xs text-muted font-body uppercase tracking-wide mb-2">
        Твій кластер
      </p>
      <h2 className="font-display text-2xl text-paper mb-6">{cluster.cluster_name}</h2>

      <div className="grid grid-cols-2 gap-8">
        <div>
          <p className="text-xs text-muted mb-2">Середній рейтинг кластера</p>
          <p className="font-display text-3xl text-marquee">{cluster.avg_rating}</p>

          <p className="text-xs text-muted mt-6 mb-2">Провідні жанри</p>
          <div className="flex flex-wrap gap-2">
            {cluster.top_genres.map((genre) => (
              <span
                key={genre}
                className="text-xs text-paper bg-marqueeDim border border-marquee/30 rounded-full px-3 py-1"
              >
                {genre}
              </span>
            ))}
          </div>
        </div>

        <div>
          <p className="text-xs text-muted mb-3">Розподіл за епохами</p>
          <div className="flex flex-col gap-3">
            {eraEntries.map(([era, percent]) => (
              <div key={era}>
                <div className="flex justify-between text-xs text-muted mb-1">
                  <span>{ERA_LABELS[era] || era}</span>
                  <span>{percent}%</span>
                </div>
                <div className="h-1.5 rounded-full bg-hairline overflow-hidden">
                  <div
                    className="h-full bg-marquee rounded-full"
                    style={{ width: `${(percent / maxEra) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
