def _smooth(values, window=7):
    if not values:
        return []

    smoothed = []

    for i in range(len(values)):
        start = max(0, i - window // 2)
        end = min(len(values), i + window // 2 + 1)

        section = values[start:end]
        smoothed.append(sum(section) / len(section))

    return smoothed

def estimate_cycle_length(movement_signal, min_lag=20, max_lag=80):
    if not movement_signal:
        return None

    values = [record["value"] for record in movement_signal]

    if len(values) < max_lag * 2:
        return None

    mean = sum(values) / len(values)
    centered = [value - mean for value in values]

    best_lag = None
    best_score = float("-inf")

    for lag in range(min_lag, max_lag + 1):
        score = sum(centered[i] * centered[i - lag] for i in range(lag, len(centered)))

        if score > best_score:
            best_score = score
            best_lag = lag

    return best_lag


def detect_repetitions(movement_signal, cycle_length=None, smoothing_window=7,):
    if not movement_signal:
        return []

    values = [record["value"] for record in movement_signal]

    smoothed = _smooth(values, smoothing_window)

    if cycle_length is None:
        cycle_length = estimate_cycle_length(movement_signal)

    if cycle_length is None:
        return []

    min_distance = max(10, int(cycle_length * 0.65))

    value_range = max(smoothed) - min(smoothed)

    if value_range <= 0:
        return []

    prominence_threshold = value_range * 0.10

    candidates = []

    for i in range(1, len(smoothed) - 1):
        if smoothed[i] <= smoothed[i - 1] and smoothed[i] < smoothed[i + 1]:
            left_max = max(smoothed[max(0, i - cycle_length):i + 1])
            right_max = max(smoothed[i:min(len(smoothed), i + cycle_length + 1)])

            prominence = min(left_max - smoothed[i], right_max - smoothed[i])

            if prominence >= prominence_threshold:
                candidates.append(i)

    minima = []

    for candidate in candidates:
        if not minima:
            minima.append(candidate)
            continue

        if candidate - minima[-1] >= min_distance:
            minima.append(candidate)
        elif smoothed[candidate] < smoothed[minima[-1]]:
            minima[-1] = candidate

    repetitions = []

    for index in minima:
        record = movement_signal[index]

        repetitions.append({
            "rep": len(repetitions) + 1,
            "bottom_frame": record["frame"],
            "bottom_timestamp_ms": record["timestamp_ms"],
            "bottom_value": smoothed[index],
        })

    return repetitions