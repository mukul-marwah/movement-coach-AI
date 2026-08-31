import numpy as np


def _smooth(values,window=3):
    values=np.asarray(values,dtype=float)

    if values.size==0:
        return []

    if values.size<window:
        return values.tolist()

    kernel=np.ones(window)/window
    smoothed=np.convolve(values,kernel,mode="same")

    half=window//2
    for i in range(half):
        smoothed[i]=np.mean(values[:i+half+1])
        smoothed[-i-1]=np.mean(values[-i-half-1:])

    return smoothed.tolist()


def detect_repetitions(movement_signal,cycle_length=None,smoothing_window=3):
    if movement_signal is None or len(movement_signal)<5:
        return []

    values=np.asarray(
        [record["value"] for record in movement_signal],
        dtype=float,
    )

    if not np.all(np.isfinite(values)):
        values=np.nan_to_num(values)

    smoothed=_smooth(values,smoothing_window)

    if len(smoothed)<5:
        return []

    value_range=float(np.max(smoothed)-np.min(smoothed))

    if value_range<10:
        return []

    minimum=float(np.min(smoothed))
    maximum=float(np.max(smoothed))

    bottom_threshold=minimum+value_range*0.45
    rise_threshold=minimum+value_range*0.15

    repetitions=[]
    bottom_index=None

    for i in range(1,len(smoothed)-1):
        current=smoothed[i]
        previous=smoothed[i-1]
        next_value=smoothed[i+1]

        if current<=previous and current<=next_value and current<=bottom_threshold:
            if bottom_index is None:
                bottom_index=i
            elif i-bottom_index>=2 and current<smoothed[bottom_index]:
                bottom_index=i

        elif bottom_index is not None:
            rise=smoothed[i]-smoothed[bottom_index]

            if rise>=value_range*0.15:
                record=movement_signal[bottom_index]

                repetitions.append({
                    "rep":len(repetitions)+1,
                    "bottom_frame":record["frame"],
                    "bottom_timestamp_ms":record["timestamp_ms"],
                    "bottom_value":float(smoothed[bottom_index]),
                })

                bottom_index=None

    if bottom_index is not None and len(repetitions)<8:
        rise=maximum-smoothed[bottom_index]

        if rise>=value_range*0.15:
            record=movement_signal[bottom_index]

            repetitions.append({
                "rep":len(repetitions)+1,
                "bottom_frame":record["frame"],
                "bottom_timestamp_ms":record["timestamp_ms"],
                "bottom_value":float(smoothed[bottom_index]),
            })

    return repetitions[:8]