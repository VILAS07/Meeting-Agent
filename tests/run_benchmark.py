import os
import sys
import json

# Add parent directory to sys.path to import agent modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.extractor import extract_items
from agent.prioritizer import prioritize_items
from agent.formatter import format_report
from tests.scorer import score_agent, compare_with_plain_llm

TRANSCRIPTS = [
    {"file": "transcript_startup.txt", "expected_items": 6, "expected_owners": 3},
    {"file": "transcript_sales.txt", "expected_items": 8, "expected_owners": 4},
    {"file": "transcript_technical.txt", "expected_items": 5, "expected_owners": 3}
]

def run_benchmarks():
    base_dir = os.path.dirname(__file__)
    outputs_dir = os.path.join(base_dir, '..', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    results = []
    
    print("🚀 STARTING BENCHMARKS\n")
    print("| Transcript | Agent Score | Plain LLM Score | Improvement |")
    print("|------------|-------------|-----------------|-------------|")
    
    for t_info in TRANSCRIPTS:
        filepath = os.path.join(base_dir, t_info["file"])
        with open(filepath, 'r', encoding='utf-8') as f:
            transcript = f.read()
            
        name = t_info["file"].replace("transcript_", "").replace(".txt", "").capitalize()
        
        # 1. Run Pipeline
        extracted = extract_items(transcript)
        prioritized = prioritize_items(extracted)
        report = format_report(prioritized, extracted)
        
        agent_data = {
            "summary": "Generated",
            "action_items": prioritized,
            "raw_extracted": extracted
        }
        
        agent_scores = score_agent(agent_data, t_info["expected_owners"], t_info["expected_items"])
        agent_total = agent_scores["TOTAL"]
        
        # 2. Run Plain LLM
        plain_llm_data = compare_with_plain_llm(transcript, t_info["expected_items"])
        plain_total = plain_llm_data["scores"]["TOTAL"]
        
        improvement = ((agent_total - plain_total) / max(1, plain_total)) * 100
        
        print(f"| {name:<10} | {agent_total:<11} | {plain_total:<15} | {improvement:>.1f}%       |")
        
        results.append({
            "transcript": name,
            "agent_score": agent_scores,
            "plain_llm_score": plain_llm_data["scores"],
            "improvement_pct": improvement
        })
        
    results_path = os.path.join(outputs_dir, 'benchmark_results.json')
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        
    print(f"\n✅ Benchmarks complete. Results saved to outputs/benchmark_results.json")

if __name__ == "__main__":
    run_benchmarks()
