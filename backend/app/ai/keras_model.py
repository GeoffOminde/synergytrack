import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Minimal model that maps a fixed-length feature vector -> forecast + anomaly score
model = models.Sequential([
    layers.Input((5,)),
    layers.Dense(16, activation="relu"),
    layers.Dense(8, activation="relu"),
    layers.Dense(2)  # [forecast, anomaly_score]
])
model.compile(optimizer="adam", loss="mse")

def infer_kpi(metrics_vec: list[float]):
    # Pad/trim to 5 for MVP consistency
    x = np.array((metrics_vec + [0]*5)[:5], dtype=np.float32)[None, ...]
    y = model.predict(x, verbose=0)[0]
    forecast = float(y[0])
    anomaly = float(max(0.0, min(1.0, y[1])))
    return {"forecast": forecast, "anomaly": anomaly}
