import { useState } from "react";
import ProgressDots from "../components/ProgressDots";
import SliderQuestion from "../components/SliderQuestion";
import EraSelect from "../components/EraSelect";
import AnchorMovieCarousel from "../components/AnchorMovieCarousel";
import { SLIDER_QUESTIONS } from "../quizData";
import { fetchRecommendations } from "../api";

// Step order: 3 slider questions -> era -> anchor movie -> submit
const TOTAL_STEPS = SLIDER_QUESTIONS.length + 2;

const initialAnswers = {
  mood: 3,
  action: 3,
  duration: 3,
  era: null,
  anchor_movie: null,
};

export default function QuizPage({ onResult }) {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState(initialAnswers);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const isSliderStep = step < SLIDER_QUESTIONS.length;
  const isEraStep = step === SLIDER_QUESTIONS.length;
  const isAnchorStep = step === SLIDER_QUESTIONS.length + 1;

  const canGoNext = isSliderStep
    ? true
    : isEraStep
    ? Boolean(answers.era)
    : Boolean(answers.anchor_movie);

  function goNext() {
    if (!canGoNext) return;
    if (step < TOTAL_STEPS - 1) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  }

  function goBack() {
    setError(null);
    setStep((s) => Math.max(0, s - 1));
  }

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchRecommendations(answers);
      onResult(result);
    } catch (err) {
      setError(err.message || "Щось пішло не так. Спробуй ще раз.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-16">
      <div className="mb-12">
        <ProgressDots total={TOTAL_STEPS} current={step} />
      </div>

      <div className="flex-1 flex items-center justify-center w-full">
        {isSliderStep && (
          <SliderQuestion
            question={SLIDER_QUESTIONS[step].question}
            lowLabel={SLIDER_QUESTIONS[step].lowLabel}
            highLabel={SLIDER_QUESTIONS[step].highLabel}
            value={answers[SLIDER_QUESTIONS[step].key]}
            onChange={(v) =>
              setAnswers((a) => ({ ...a, [SLIDER_QUESTIONS[step].key]: v }))
            }
          />
        )}

        {isEraStep && (
          <EraSelect
            value={answers.era}
            onChange={(v) => setAnswers((a) => ({ ...a, era: v }))}
          />
        )}

        {isAnchorStep && (
          <AnchorMovieCarousel
            value={answers.anchor_movie}
            onChange={(v) => setAnswers((a) => ({ ...a, anchor_movie: v }))}
          />
        )}
      </div>

      {error && (
        <p className="text-sm text-red-400 font-body mt-6 text-center max-w-md">{error}</p>
      )}

      <div className="flex items-center gap-4 mt-12">
        <button
          type="button"
          onClick={goBack}
          disabled={step === 0 || loading}
          className="font-body text-sm text-muted hover:text-paper disabled:opacity-0 transition-colors px-4 py-2"
        >
          Назад
        </button>

        <button
          type="button"
          onClick={goNext}
          disabled={!canGoNext || loading}
          className="font-body text-sm font-medium bg-marquee text-ink px-8 py-3 rounded-full disabled:opacity-40 disabled:cursor-not-allowed hover:bg-marquee/90 transition-colors"
        >
          {loading
            ? "Шукаємо фільми..."
            : step === TOTAL_STEPS - 1
            ? "Знайти фільми"
            : "Далі"}
        </button>
      </div>
    </div>
  );
}
