export default function ProgressDots({ total, current }) {
  return (
    <div className="flex items-center justify-center gap-2" aria-label={`Крок ${current + 1} з ${total}`}>
      {Array.from({ length: total }).map((_, i) => (
        <span
          key={i}
          className={`h-1.5 rounded-full transition-all duration-300 ${
            i === current ? "w-8 bg-marquee" : i < current ? "w-1.5 bg-marquee/50" : "w-1.5 bg-hairline"
          }`}
        />
      ))}
    </div>
  );
}
