import json
import os
from .llm import call_llm

def prioritize_items(extracted: dict) -> list:
    """
    Takes extracted items, particularly action_items, and scores them by impact and effort.
    
    Args:
        extracted (dict): Dictionary from extract_items output.
        
    Returns:
        list: List of prioritized items, sorted by highest priority_score.
    """
    action_items = extracted.get("action_items", [])
    if not action_items:
        return []
        
    # Simplify input: only send necessary fields to save tokens while retaining deadline data
    simplified_tasks = [{"task": item.get("task", ""), "owner": item.get("owner", "Unassigned"), "deadline": item.get("mentioned_deadline", "Unknown")} for item in action_items]
        
    # Load the prompt
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'prioritize.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
        
    # Inject tasks
    tasks_json_str = json.dumps(simplified_tasks, indent=2)
    prompt = prompt_template.replace('{tasks}', tasks_json_str)
    
    # Call the LLM
    print("Prioritizing tasks...")
    response_text = call_llm(prompt, model='stepfun/step-3.5-flash:free')
    
    # Extract JSON array safely
    start_idx = response_text.find('[')
    end_idx = response_text.rfind(']')
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        response_text = response_text[start_idx:end_idx+1]
        
    response_text = response_text.strip()
    
    # Parse as JSON
    try:
        prioritized = json.loads(response_text)
        
        # If the LLM returned a dict instead of a list, try to extract the list
        if isinstance(prioritized, dict):
            for k, v in prioritized.items():
                if isinstance(v, list):
                    prioritized = v
                    break
            else:
                prioritized = [prioritized] # Fallback to single-item list
                
        # Sort by priority_score descending
        prioritized.sort(key=lambda x: x.get('priority_score', 0) if isinstance(x, dict) else 0, reverse=True)
        return prioritized
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from prioritizer: {e}")
        print(f"Raw response: {response_text}")
        return []
