import { ERA_OPTIONS } from "../quizData";

export default function EraSelect({ value, onChange }) {
  return (
    <div className="w-full max-w-md">
      <h2 className="font-display text-3xl leading-snug text-paper mb-10 text-center">
        Яку епоху кіно ти обираєш?
      </h2>

      <div className="grid grid-cols-3 gap-3">
        {ERA_OPTIONS.map((era) => (
          <button
            key={era.key}
            type="button"
            onClick={() => onChange(era.key)}
            className={`flex flex-col items-center gap-1 rounded-lg border px-3 py-6 transition-colors ${
              value === era.key
                ? "border-marquee bg-marqueeDim"
                : "border-hairline bg-surface hover:border-marquee/40"
            }`}
          >
            <span className="font-display text-xl text-paper">{era.label}</span>
            <span className="text-xs text-muted">{era.hint}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
