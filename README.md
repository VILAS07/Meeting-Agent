# 🤖 Meeting Notes → Action Items Agent

> **An AI pipeline that transforms raw meeting transcripts into structured, prioritized action plans — using free LLMs via OpenRouter.**

![Models](https://img.shields.io/badge/Models-Free%20OpenRouter-orange)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Cursor](https://img.shields.io/badge/Cursor-Ready-purple)

---

## 💡 Why This Problem Was #1 Priority

Meeting action items are the most universally lost data in any team — regardless of size, industry, or toolstack. Every company has this problem. The solution is measurable, immediately useful, and directly demonstrates **Priority Definition Ability**: knowing what matters, extracting it, ranking it, and delivering it in a format that drives execution.

This is not a tool for documenting meetings. It is a tool for eliminating the gap between decision and action.

---

## 📌 The Problem

After every meeting, the same thing happens:

- Action items get buried in messy notes
- Teams spend the next meeting re-discussing what was already decided
- The person taking notes captures *what was said* — not *what matters most*
- Nobody knows who owns what or when it's due

**This agent eliminates that friction in under 2 minutes.**

Instead of a plain summary, you get a ranked execution plan — with owners, deadlines, priority scores, and reasoning for every decision.

---

## ⚙️ How It Works
Raw Transcript → [EXTRACT] → [PRIORITIZE] → [FORMAT] → Action Plan

The pipeline has 3 dedicated LLM steps, each with its own focused prompt:

### Step 1 — Extract
A targeted LLM call pulls every action item, decision, person, and topic from the transcript. Returns structured JSON — no loose text.

### Step 2 — Prioritize
Each task is scored using the formula:
Priority Score = (Impact × 10) − (Effort × 3)

- **Impact** = Business value if completed (1–10)
- **Effort** = Time and resources required (1–10)
- Tasks with **same-day deadlines** are always elevated to the top 2

### Step 3 — Format
The ranked data is compiled into a clean Markdown report and a JSON artifact — both saved to the `outputs/` folder with a timestamp.

---

## 📄 Sample Output

Running on `tests/sample_meeting.txt` produces:
MEETING ACTION PLAN
MEETING SUMMARY
The meeting covered Q3 Product Launch, analytics dashboard, marketing site,
press release timing, and pricing tiers. Key participants: Sarah, Marcus, Elena, David.
KEY DECISIONS

Press release pushed to Thursday to avoid Apple event clash
Pricing tiers named Basic, Pro, and Enterprise

TOP PRIORITY
🚨 TOP PRIORITY: Notify PR firm about press release delay (Owner: Marcus)

Reason: Same-day deadline — must be done today (Impact: 8/10, Effort: 1/10)

ACTION ITEMS
#TaskOwnerDeadlinePriority ScoreReason1Notify PR firm about delayMarcusToday77Urgent, low effort2Supply hero images to ElenaDavidWednesday67Blocks site deploy3Finish dashboard UIMarcusFriday64Core launch blocker4Deploy marketing site updateElenaMonday58Depends on images5Write app store release notesDavidFriday52Launch requirement6Update pricing page copyElenaThursday49Decision just made

---

## 🚀 Quick Start
```bash
# 1. Clone the repo
git clone https://github.com/VILAS07/Meeting-Agent.git
cd Meeting-Agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your OpenRouter API key
# Get a free key at https://openrouter.ai → Keys → Create
copy .env.example .env
# Open .env and set: OPENROUTER_API_KEY=your_key_here

# 4. Run on a sample transcript
python main.py --input tests/sample_meeting.txt

# 5. Or run on your own text directly
python main.py --text "Sarah will handle the deployment by Friday. Marcus needs to update the docs."
```

---

## 📊 Performance Scoring

The agent is evaluated on a 1–10,000 scale across 5 metrics:

| Metric | Max Score | What It Measures |
|---|---|---|
| Extraction Accuracy | 2500 | Are all action items captured? |
| Priority Correctness | 2500 | Are impact/effort scores consistent? |
| Owner Detection | 2000 | Are task owners correctly identified? |
| Deadline Quality | 1500 | Are deadlines inferred correctly? |
| Output Clarity | 1500 | Is the report clean and structured? |
| **Total** | **10,000** | |

Run the benchmark yourself to generate real scores:
```bash
python tests/run_benchmark.py
```

Results are saved to `outputs/benchmark_results.json`.

---

## 🏆 Benchmark: Agent vs Plain LLM

Same transcript. Same model. Different approach.

The pipeline is benchmarked against a plain single-prompt LLM call on the same input. Run it yourself:
```bash
python tests/run_benchmark.py
```

**Why the pipeline wins:**
A plain LLM call returns conversational output — readable, but unstructured. No priority scores. No consistent JSON. No guaranteed owner assignment. The pipeline forces structured reasoning at every step, making the output reliable and actionable every single time.

---

## 📁 Project Structure
Meeting-Agent/
├── agent/
│   ├── llm.py            # All LLM calls go through here (OpenRouter)
│   ├── extractor.py      # Step 1 — Extract action items from transcript
│   ├── prioritizer.py    # Step 2 — Score and rank by impact/effort
│   └── formatter.py      # Step 3 — Generate Markdown + JSON report
├── prompts/
│   ├── extract.txt       # Extraction prompt template
│   └── prioritize.txt    # Prioritization prompt template
├── tests/
│   ├── sample_meeting.txt         # Demo transcript
│   ├── transcript_startup.txt     # Benchmark transcript 1
│   ├── transcript_sales.txt       # Benchmark transcript 2
│   ├── transcript_technical.txt   # Benchmark transcript 3
│   ├── scorer.py                  # 1–10,000 scoring system
│   └── run_benchmark.py           # Agent vs Plain LLM comparison
├── outputs/              # Generated reports (gitignored)
├── main.py               # Entry point — runs full pipeline
├── .cursorrules          # Cursor AI configuration
├── .env.example          # API key template
├── requirements.txt
└── README.md

---

## 🔧 Free Models Used (OpenRouter)

| Step | Model | Why |
|---|---|---|
| Extract | `stepfun/step-3.5-flash:free` | Fast, accurate at structured extraction |
| Prioritize | `stepfun/step-3.5-flash:free` | Reliable reasoning for scoring |
| Fallback 1 | `google/gemma-2-9b-it:free` | Automatic fallback if primary fails |
| Fallback 2 | `microsoft/phi-3-mini-128k-instruct:free` | Final fallback model |

No paid API required. All models are free tier on OpenRouter.

---

## 🖥️ Cursor Setup

The `.cursorrules` file configures Cursor AI to follow the project's architecture:

- All LLM calls go through `agent/llm.py` — never called directly elsewhere
- API keys always loaded from `.env` — never hardcoded
- All prompts stored as `.txt` files in `prompts/` — never inlined
- Every function uses type hints and docstrings
- Functions kept under 30 lines for readability
- Output always returns valid JSON when processing meeting data

Open this project in Cursor and the AI assistant will automatically follow these rules.

---

## 🧠 Design Decisions

**Why a 3-step pipeline instead of one prompt?**
Splitting extraction from prioritization eliminates a core LLM failure mode — when you ask a single prompt to extract AND rank simultaneously, it hallucinates rankings or misses items. Separating the steps forces focused, verifiable reasoning at each stage.

**Why free models?**
To prove that architecture matters more than expensive models. Intelligence comes from prompt design and pipeline structure — not from throwing GPT-4 at every problem.

**Why this scoring formula?**
`Priority = (Impact × 10) − (Effort × 3)` mirrors how real engineering and product teams actually make prioritization decisions. High impact, low effort tasks always rise to the top. Same-day deadlines override the formula — urgency trumps optimization.

**Why store prompts as `.txt` files?**
Keeping prompts outside code makes them easy to test, swap, and improve without touching the pipeline logic. It also forces clean separation between the AI layer and the application layer.

---

## ⚠️ Known Limitations

| Limitation | Detail | Fix |
|---|---|---|
| Speed | ~90s on free tier due to OpenRouter queue limits | Zero code changes needed — sub-10s on paid tier |
| Consistency | Priority ranking can vary slightly between runs | Addressed with deterministic deadline rules in prompt |
| Language | Optimized for English transcripts | Prompt templates can be translated for other languages |

---

## 📬 Contact

Built by [Vilas](https://github.com/VILAS07) as part of the MUST Company FDE/APO Quest.

---

*Built with free LLMs. Powered by structured thinking.*
