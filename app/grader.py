from app.models import Action, Task
def grade_action(action: Action, task: Task) -> float:
    score = 0.0

    # Issue type
    if action.issue_type.lower() == task.issue_type.lower():
        score += 0.4

    # Description scoring
    desc = action.description.lower()
    desc_len = len(task.description_keywords)

    if desc_len > 0:
        desc_matches = sum(1 for kw in task.description_keywords if kw in desc)
        score += 0.3 * (desc_matches / desc_len)

    # Fix scoring
    fix = action.fix.lower()
    fix_len = len(task.fix_keywords)

    if fix_len > 0:
        fix_matches = sum(1 for kw in task.fix_keywords if kw in fix)
        score += 0.3 * (fix_matches / fix_len)

    # Penalty
    if score == 0:
        score -= 0.1

    return max(0.0, min(score, 1.0))