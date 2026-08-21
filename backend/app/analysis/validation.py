from typing import Any, Dict, List


def validate_feature_series(
    feature_series: List[Dict[str, Any]],
    required_features: tuple[str, ...],
) -> Dict[str, Any]:
    if not feature_series:
        return {
            "valid": False,
            "reason": "empty_feature_series",
            "missing_features": list(required_features),
        }

    available_features = set()

    for record in feature_series:
        available_features.update(record.keys())

    missing_features = [feature for feature in required_features if feature not in available_features]

    if missing_features:
        return {"valid": False, "reason": "missing_required_features", "missing_features": missing_features}

    return {"valid": True, "reason": None, "missing_features": []}

def validate_exercise_feature_series(
    feature_series: List[Dict[str, Any]],
    exercise_definition,
) -> Dict[str, Any]:
    return validate_feature_series(feature_series, exercise_definition.required_features)