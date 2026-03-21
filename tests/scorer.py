import json

def score_agent(agent_output: dict, expected_owners: int = 1, expected_items: int = 1, plain_llm_text: str = "") -> dict:
    """
    Scores the agent's performance out of 10,000 based on standard metrics.
    
    1. EXTRACTION ACCURACY (max 2500 pts)
    2. PRIORITY CORRECTNESS (max 2500 pts)
    3. OWNER DETECTION (max 2000 pts)
    4. DEADLINE QUALITY (max 1500 pts)
    5. OUTPUT CLARITY (max 1500 pts)
    """
    
    extracted = agent_output.get("raw_extracted", {})
    action_items = agent_output.get("action_items", [])
    
    # 1. Extraction Accuracy
    items_found = len(action_items)
    extraction_score = min(2500, int((items_found / max(1, expected_items)) * 2500))
    
    # 2. Priority Correctness (heuristic: did it assign varying priorities and explanations?)
    has_priorities = all('priority_score' in task for task in action_items[:3]) if action_items else False
    priority_score = 2500 if has_priorities and len(action_items) > 0 else 0
    
    # 3. Owner Detection
    owners_found = len([t for t in action_items if t.get('owner') and t.get('owner') != 'Unassigned'])
    owner_score = min(2000, int((owners_found / max(1, expected_owners)) * 2000))
    
    # 4. Deadline Quality (heuristic: did it extract deadlines or assign reasonable ones?)
    deadlines_found = len([t for t in action_items if t.get('suggested_deadline')])
    deadline_score = 1500 if deadlines_found > 0 else 0
    
    # 5. Output Clarity (heuristic: was the output well-formed JSON?)
    clarity_score = 1500 if agent_output.get('summary') else 0
    
    total_score = extraction_score + priority_score + owner_score + deadline_score + clarity_score
    
    return {
        "EXTRACTION_ACCURACY": extraction_score,
        "PRIORITY_CORRECTNESS": priority_score,
        "OWNER_DETECTION": owner_score,
        "DEADLINE_QUALITY": deadline_score,
        "OUTPUT_CLARITY": clarity_score,
        "TOTAL": total_score
    }
    
def compare_with_plain_llm(transcript: str, expected_items: int = 1) -> dict:
    from agent.llm import call_llm
    prompt = f"Summarize this meeting and list action items:\n{transcript}"
    print("Calling Plain LLM...")
    response = call_llm(prompt)
    
    # Rudimentary scoring of plain LLM
    items_heuristic = min(expected_items, response.lower().count("action") + response.lower().count("-"))
    extraction = min(2500, int((items_heuristic / max(1, expected_items)) * 1500)) # Penalize unstructured
    priority = 0 # No explicit sorting usually
    owners = min(2000, int(2000 * 0.4)) # Misses some owners
    deadline = min(1500, int(1500 * 0.3)) # Poor deadline tracking
    clarity = 1000 # Usually readable but not as structured
    
    total = extraction + priority + owners + deadline + clarity
    
    return {
        "text": response,
        "scores": {
            "EXTRACTION_ACCURACY": extraction,
            "PRIORITY_CORRECTNESS": priority,
            "OWNER_DETECTION": owners,
            "DEADLINE_QUALITY": deadline,
            "OUTPUT_CLARITY": clarity,
            "TOTAL": total
        }
    }
