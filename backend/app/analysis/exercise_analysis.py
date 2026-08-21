from typing import Any, Dict, List

def _numeric_values(
    feature_series: List[Dict[str, Any]],
    feature_name: str,
) -> List[float]:
    return [
        record[feature_name]
        for record in feature_series
        if isinstance(record.get(feature_name), (int, float))
    ]

def _feature_statistics(
    feature_series: List[Dict[str, Any]],
    feature_name: str,
) -> Dict[str, Any]:
    values = _numeric_values(feature_series, feature_name)

    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None, "range": None}

    minimum = min(values)
    maximum = max(values)
    mean = sum(values) / len(values)

    return {
        "count": len(values),
        "minimum": minimum,
        "maximum": maximum,
        "mean": mean,
        "range": maximum - minimum,
    }

def analyze_feature_series(
    feature_series: List[Dict[str, Any]],
    required_features: tuple[str, ...],
) -> Dict[str, Any]:
    if not feature_series:
        return {"frame_count": 0, "duration_ms": 0, "features": {}}

    first_timestamp = feature_series[0]["timestamp_ms"]
    last_timestamp = feature_series[-1]["timestamp_ms"]

    statistics = {
        feature_name: _feature_statistics(feature_series, feature_name) for feature_name in required_features
    }

    return {
        "frame_count": len(feature_series),
        "duration_ms": last_timestamp - first_timestamp,
        "features": statistics}