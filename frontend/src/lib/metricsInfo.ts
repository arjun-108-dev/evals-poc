import type { MathMetricKey, MetricKey } from "./types";

export interface MetricInfo {
  key: string;
  title: string;
  /** One-line hint shown under the chart title. */
  hint: string;
  /** What the metric measures. */
  description: string;
  /** How to read the bars / axis. */
  howToRead: string;
  /** "high" = higher is better, "low" = lower is better. */
  goodDirection: "high" | "low";
  /** Things to watch for when interpreting this chart. */
  watchFor: string[];
}

export const METRIC_INFO: Record<MetricKey, MetricInfo> = {
  overall_score: {
    key: "overall_score",
    title: "Overall Score",
    hint: "0.45·call + 0.25·arg + 0.20·abstain + 0.10·format",
    description:
      "A single 0–1 score that ranks a model's end-to-end tool-calling ability. It blends four " +
      "component metrics so that no single skill (e.g. just naming the right tool) can mask a " +
      "weakness elsewhere (e.g. calling tools when it shouldn't).",
    howToRead:
      "Bars range from 0.0 (worst) to 1.0 (perfect). Models are colored by their legend color. " +
      "Use this chart for a quick ranking, then open the component charts below to understand why.",
    goodDirection: "high",
    watchFor: [
      "This is a weighted composite, not a raw accuracy — a model can score mid-range by being " +
        "consistently mediocre across skills rather than strong at one.",
      "Because it rewards correct ABSTENTION, a model that over-refuses (never calls tools) can " +
        "still earn points here. Check Call Accuracy to see if it actually uses tools.",
    ],
  },
  call_accuracy: {
    key: "call_accuracy",
    title: "Call Accuracy",
    hint: "correct tool name when a tool is needed",
    description:
      "Of the prompts that REQUIRE a tool (weather, timer, message, contacts), the fraction where " +
      "the model selected the correct tool. Prompts that should NOT call any tool are excluded.",
    howToRead:
      "Bars are a percentage 0–100%. A low bar means the model either named the wrong tool " +
        "(e.g. 'get_timer' instead of 'set_timer') or produced no usable call at all.",
    goodDirection: "high",
    watchFor: [
      "This only counts tool SELECTION, not argument quality — a model can ace this yet still " +
        "fill arguments with garbage (see Argument Accuracy).",
      "A near-0% here (e.g. FunctionGemma 270M) usually means the model over-refuses and answers " +
        "in plain text even when a tool is clearly required.",
    ],
  },
  arg_accuracy: {
    key: "arg_accuracy",
    title: "Argument Accuracy",
    hint: "args match expected when the tool is correct",
    description:
      "Among prompts where the model picked the CORRECT tool, the fraction where the extracted " +
      "arguments matched the expected arguments (after normalization: case/whitespace trimming, " +
      "numeric tolerance, and substring matching for short strings).",
    howToRead:
      "Bars are a percentage 0–100%. A gap between Call Accuracy and Argument Accuracy reveals " +
        "models that choose the right tool but struggle to populate its parameters.",
    goodDirection: "high",
    watchFor: [
      "Common failures: inventing argument names ('to' instead of 'recipient'), wrong number " +
        "words ('two' vs 2), or stuffing unrelated text into a field.",
      "Extra, unexpected argument keys are ignored (fair to the model); only the EXPECTED keys " +
        "must be present and correct.",
    ],
  },
  abstain_accuracy: {
    key: "abstain_accuracy",
    title: "Abstain Accuracy",
    hint: "correctly calls NO tool when none is needed",
    description:
      "Of the prompts that should NOT trigger any tool (casual chat, trivia, math, poems — " +
      "12 examples in this dataset), the fraction where the model correctly answered in plain " +
      "text and called NO tool. It is the exact complement of the False Positive Rate " +
      "(Abstain Accuracy = 1 − FPR).",
    howToRead:
      "Bars are a percentage 0–100%. A HIGH bar is good: the model understands when NOT to use " +
        "tools. A LOW bar means the model hallucinates tool calls it doesn't need.",
    goodDirection: "high",
    watchFor: [
      "'Abstain' is the opposite of a false positive. A model that always answers 'I'm not sure' " +
        "or 'I cannot help' can score high here while being useless — pair with Call Accuracy.",
      "This is where several tiny models fail hardest: they blindly emit get_weather() for " +
        "'What is 2 + 2?'.",
    ],
  },
  false_positive_rate: {
    key: "false_positive_rate",
    title: "False Positive Rate",
    hint: "called a tool when none was needed (lower is better)",
    description:
      "Of the prompts that should NOT call any tool, the fraction where the model wrongly emitted " +
      "a tool call anyway. This is the failure mode of 'over-calling' and is the mirror image of " +
      "Abstain Accuracy.",
    howToRead:
      "Bars are a percentage 0–100%; LOWER is better. 0% means the model never invented a tool " +
        "call on chit-chat; 100% means it always did.",
    goodDirection: "low",
    watchFor: [
      "High FPR is the classic tiny-model trap: the model learns 'there are tools' but not 'when " +
        "to use them', so it calls get_weather() for everything.",
      "Because this chart's bars are 'lower is better', read it in reverse of the others.",
    ],
  },
  avg_latency_ms: {
    key: "avg_latency_ms",
    title: "Average Latency",
    hint: "milliseconds per request (lower is faster)",
    description:
      "Average wall-clock time per prompt, measured from request send to full response, on this " +
      "machine's Ollama instance (CPU inference for these tiny models).",
    howToRead:
      "Bars are in milliseconds; LOWER is faster. This is a secondary quality axis, not a " +
        "correctness metric — a fast model that is wrong is still wrong.",
    goodDirection: "low",
    watchFor: [
      "Latency depends heavily on hardware and prompt length; compare models relatively, not " +
        "as absolutes.",
      "Very high values (e.g. FunctionGemma 270M) often indicate degenerate outputs — the model " +
        "loops and generates many tokens before stopping.",
    ],
  },
};

export const METRIC_ORDER: MetricKey[] = [
  "overall_score",
  "call_accuracy",
  "arg_accuracy",
  "abstain_accuracy",
  "false_positive_rate",
  "avg_latency_ms",
];

export const MATH_METRIC_INFO: Record<MathMetricKey, MetricInfo> = {
  overall_score: {
    key: "overall_score",
    title: "Overall Score",
    hint: "0.75·accuracy + 0.25·parse_rate",
    description:
      "A single 0–1 score that ranks a model's end-to-end math ability. It blends raw answer " +
      "accuracy (75%) with extraction success (25%) so a model that fails to emit any number " +
      "can't hide behind the smaller subset of examples it did answer.",
    howToRead:
      "Bars range from 0.0 (worst) to 1.0 (perfect). Models are colored by their legend color. " +
      "Use this chart for a quick ranking, then open the component charts below to understand why.",
    goodDirection: "high",
    watchFor: [
      "This is a weighted composite, not a raw accuracy — a model that always extracts SOME " +
        "answer (even wrong ones) earns parse-rate points while scoring low on accuracy.",
      "All 4 math runs achieved a 100% parse rate here, so overall tracks accuracy closely " +
        "for this dataset.",
    ],
  },
  accuracy: {
    key: "accuracy",
    title: "Accuracy",
    hint: "fraction of examples where the extracted answer matched",
    description:
      "Of all examples, the fraction where the model's extracted numeric answer matched the " +
      "expected answer (after the grader's normalization: numeric tolerance and fraction " +
      "simplification). Unparsed examples count against accuracy.",
    howToRead:
      "Bars are a percentage 0–100%. A gap between Accuracy and Parse Rate reveals examples " +
        "where a number WAS extracted but it was wrong.",
    goodDirection: "high",
    watchFor: [
      "This counts everything as a denominator, so a model that refuses to answer is penalized " +
        "the same as one that answers wrongly.",
      "Category-level failures (fractions/percents vs arithmetic) are easier to spot in the " +
        "per-model view.",
    ],
  },
  parse_rate: {
    key: "parse_rate",
    title: "Parse Rate",
    hint: "fraction where ANY numeric answer was extractable",
    description:
      "Of all examples, the fraction where the grader could extract ANY numeric answer from " +
      "the raw model output. It measures whether the model emits a number at all — not whether " +
      "that number is right.",
    howToRead:
      "Bars are a percentage 0–100%. A high parse rate with low accuracy means the model is " +
        "confidently wrong; a low parse rate means it rarely produces a usable numeric answer.",
    goodDirection: "high",
    watchFor: [
      "A low parse rate is common on word problems, where models write prose and bury the " +
        "answer, or trail off without a final number.",
      "This is the 'does it even try to answer numerically' gate that the overall score uses " +
        "to keep accuracy honest.",
    ],
  },
  avg_latency_ms: {
    key: "avg_latency_ms",
    title: "Average Latency",
    hint: "milliseconds per request (lower is faster)",
    description:
      "Average wall-clock time per question, measured from request send to full response, on " +
      "this machine's Ollama instance (CPU inference for these tiny models).",
    howToRead:
      "Bars are in milliseconds; LOWER is faster. This is a secondary quality axis, not a " +
        "correctness metric — a fast model that is wrong is still wrong.",
    goodDirection: "low",
    watchFor: [
      "Latency depends heavily on hardware and prompt length; compare models relatively, not " +
        "as absolutes.",
      "Long chain-of-thought answers inflate latency without necessarily improving accuracy.",
    ],
  },
};

export const MATH_METRIC_ORDER: MathMetricKey[] = [
  "overall_score",
  "accuracy",
  "parse_rate",
  "avg_latency_ms",
];
