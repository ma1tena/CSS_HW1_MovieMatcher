import { useState } from "react";
import QuizPage from "./pages/QuizPage";
import ResultsPage from "./pages/ResultsPage";

export default function App() {
  const [result, setResult] = useState(null);

  if (result) {
    return <ResultsPage result={result} onRestart={() => setResult(null)} />;
  }

  return <QuizPage onResult={setResult} />;
}
