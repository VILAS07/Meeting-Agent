import json
import os
import datetime

def format_report(prioritized: list, extracted: dict) -> str:
    """
    Takes prioritized tasks and original extracted data to generate a markdown report.
    Saves the report and a JSON version to outputs/.
    
    Args:
        prioritized (list): List of prioritized tasks.
        extracted (dict): Original extraction results.
        
    Returns:
        str: Formatted report as text.
    """
    # Create outputs folder if not exists
    outputs_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    # 1. Provide a quick summary of the meeting topics
    topics = ", ".join(extracted.get('topics', [])) if extracted.get('topics') else "various projects"
    people = ", ".join(extracted.get('people_mentioned', [])) if extracted.get('people_mentioned') else "the team"
    summary = f"Summary: The meeting covered updates regarding {topics}. Key participants included {people}."
    
    # 2. Key Decisions
    decisions = extracted.get('decisions', [])
    decisions_text = "\n".join([f"- {d}" for d in decisions]) if decisions else "- None recorded."
    
    # 3. Action Items
    action_table = "| # | Task | Owner | Deadline | Priority Score | Reason |\n"
    action_table += "|---|---|---|---|---|---|\n"
    for idx, task in enumerate(prioritized, 1):
        action_table += f"| {idx} | {task.get('task')} | {task.get('owner')} | {task.get('suggested_deadline')} | {task.get('priority_score')} | {task.get('reason')} |\n"
        
    # 4. Top Priority
    top_priority_text = "No action items identified."
    if prioritized:
        top_task = prioritized[0]
        top_priority_text = f"🚨 **TOP PRIORITY**: {top_task.get('task')} (Owner: {top_task.get('owner')})\n"
        top_priority_text += f"> **Reason**: {top_task.get('reason')} (Impact: {top_task.get('impact_score')}/10, Effort: {top_task.get('effort_score')}/10)"

    report = f"""# MEETING ACTION PLAN

## MEETING SUMMARY
{summary}

## KEY DECISIONS
{decisions_text}

## TOP PRIORITY
{top_priority_text}

## ACTION ITEMS
{action_table}
"""

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = os.path.join(outputs_dir, f'report_{timestamp}.md')
    json_path = os.path.join(outputs_dir, f'report_{timestamp}.json')
    
    # Save Report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    # Save JSON version
    full_data = {
        "summary": summary,
        "decisions": decisions,
        "top_priority": prioritized[0] if prioritized else None,
        "action_items": prioritized,
        "raw_extracted": extracted
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, indent=2)
        
    print(f"Report saved to outputs/report_{timestamp}.md")
    
    return report
