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

```
MEETING ACTION PLAN

MEETING SUMMARY
The meeting covered Q3 Product Launch, analytics dashboard, marketing site,
press release timing, and pricing tiers. Key participants: Sarah, Marcus, Elena, David.

KEY DECISIONS
- Press release pushed to Thursday to avoid Apple event clash
- Pricing tiers named Basic, Pro, and Enterprise

TOP PRIORITY
🚨 TOP PRIORITY: Notify PR firm about press release delay (Owner: Marcus)

Reason: Same-day deadline — must be done today (Impact: 8/10, Effort: 1/10)

ACTION ITEMS

# | Task | Owner | Deadline | Priority Score | Reason
1 | Notify PR firm about delay | Marcus | Today | 77 | Urgent, low effort
2 | Supply hero images to Elena | David | Wednesday | 67 | Blocks site deploy
3 | Finish dashboard UI | Marcus | Friday | 64 | Core launch blocker
4 | Deploy marketing site update | Elena | Monday | 58 | Depends on images
5 | Write app store release notes | David | Friday | 52 | Launch requirement
6 | Update pricing page copy | Elena | Thursday | 49 | Decision just made
```

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

Run the benchmark yourself:

```bash
python tests/run_benchmark.py
```

Results are saved to `outputs/benchmark_results.json`.

---

## 🏆 Benchmark: Agent vs Plain LLM

Same transcript. Same model. Different approach.

Run:

```bash
python tests/run_benchmark.py
```

**Why the pipeline wins:**

A plain LLM call returns conversational output — readable, but unstructured.  
No priority scores. No consistent JSON. No guaranteed owner assignment.  

The pipeline forces structured reasoning at every step.

---

## 📁 Project Structure

```
Meeting-Agent/
├── agent/
│   ├── llm.py
│   ├── extractor.py
│   ├── prioritizer.py
│   └── formatter.py
├── prompts/
│   ├── extract.txt
│   └── prioritize.txt
├── tests/
│   ├── sample_meeting.txt
│   ├── transcript_startup.txt
│   ├── transcript_sales.txt
│   ├── transcript_technical.txt
│   ├── scorer.py
│   └── run_benchmark.py
├── outputs/
├── main.py
├── .cursorrules
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔧 Free Models Used (OpenRouter)

| Step | Model |
|---|---|
| Extract | stepfun/step-3.5-flash:free |
| Prioritize | stepfun/step-3.5-flash:free |
| Fallback 1 | google/gemma-2-9b-it:free |
| Fallback 2 | microsoft/phi-3-mini-128k-instruct:free |

---

## 🖥️ Cursor Setup

- All LLM calls → `agent/llm.py`
- API keys → `.env`
- Prompts → `prompts/*.txt`
- Functions → type hints + docstrings
- Output → always valid JSON

---

## 🧠 Design Decisions

**Why 3-step pipeline?**  
Prevents hallucination and improves accuracy.

**Why free models?**  
Shows architecture > expensive models.

**Why this formula?**  
Real-world prioritization logic.

**Why `.txt` prompts?**  
Easy to edit without touching code.

---

## ⚠️ Known Limitations

| Limitation | Detail |
|---|---|
| Speed | ~90s (free tier) |
| Consistency | Slight variation |
| Language | English optimized |

---

## 📬 Contact

Built by [Vilas](https://github.com/VILAS07)

---

*Built with free LLMs. Powered by structured thinking.*
