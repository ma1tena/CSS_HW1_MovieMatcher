import { useState } from "react";
import QuizPage from "./pages/QuizPage";

// NOTE: this temporary result view is a placeholder. It will be replaced by
// ResultsPage (movie cards + analytics) in Milestone 4.
function RawResultPreview({ result, onRestart }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-16 gap-8">
      <h1 className="font-display text-3xl text-paper text-center">
        Бекенд відповів! (тимчасовий перегляд)
      </h1>
      <pre className="max-w-2xl w-full overflow-auto text-xs bg-surface border border-hairline rounded-lg p-6 text-muted">
        {JSON.stringify(result, null, 2)}
      </pre>
      <button
        type="button"
        onClick={onRestart}
        className="font-body text-sm font-medium bg-marquee text-ink px-8 py-3 rounded-full hover:bg-marquee/90 transition-colors"
      >
        Пройти квіз ще раз
      </button>
    </div>
  );
}

export default function App() {
  const [result, setResult] = useState(null);

  if (result) {
    return <RawResultPreview result={result} onRestart={() => setResult(null)} />;
  }

  return <QuizPage onResult={setResult} />;
}
