from ..llm import generate_movement_coaching

def run_movement_coach(analysis):
    if not isinstance(analysis, dict):
        raise TypeError("Movement Coach input must be a dictionary")

    required_keys = {"exercise", "repetitions", "feature_summary",}
    missing_keys = required_keys - set(analysis)

    if missing_keys:
        raise ValueError(f"Movement analysis is missing required fields: {missing_keys}")

    return generate_movement_coaching(analysis)