export default function SliderQuestion({ question, lowLabel, highLabel, value, onChange }) {
  return (
    <div className="w-full max-w-md">
      <h2 className="font-display text-3xl leading-snug text-paper mb-10 text-center">
        {question}
      </h2>

      <div className="px-2">
        <input
          type="range"
          min={1}
          max={5}
          step={1}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
        />
        <div className="flex justify-between mt-4 text-sm text-muted font-body">
          <span className="max-w-[45%]">{lowLabel}</span>
          <span className="max-w-[45%] text-right">{highLabel}</span>
        </div>
      </div>

      <div className="flex justify-center gap-3 mt-8">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            className={`h-9 w-9 rounded-full font-body text-sm transition-colors ${
              value === n
                ? "bg-marquee text-ink"
                : "bg-surface text-muted border border-hairline hover:border-marquee/50"
            }`}
            aria-label={`Оцінка ${n}`}
          >
            {n}
          </button>
        ))}
      </div>
    </div>
  );
}
