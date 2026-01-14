from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
import pathlib, io
import numpy as np
from PIL import Image
from ultralytics import YOLO

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent

# Load models once
hzrd_model = YOLO("HZRD_fire_detection_best.pt")
smoke_fire_model = YOLO("smokenfire.pt")
ppe_model = YOLO("PPE.pt")

PPE_ACTIVE = False


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return (BASE_DIR / "index.html").read_text()


def box_area(box):
    x1, y1, x2, y2 = box
    return max(0, x2 - x1) * max(0, y2 - y1)


@app.post("/infer")
async def infer(file: UploadFile = File(...)):
    global PPE_ACTIVE

    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    frame = np.array(img)
    frame_bgr = frame[..., ::-1]

    h, w = frame.shape[:2]
    frame_area = h * w

    detections = []
    alerts = []
    area = {"HZRD": 0.0, "smoke": 0.0}

    # ---------- HZRD ----------
    hzrd_results = hzrd_model(frame_bgr, conf=0.4)[0]
    hzrd_present = False

    if hzrd_results.boxes:
        for box, cls, conf in zip(
            hzrd_results.boxes.xyxy,
            hzrd_results.boxes.cls,
            hzrd_results.boxes.conf,
        ):
            label = hzrd_model.names[int(cls)]
            detections.append({
                "class": label,
                "confidence": float(conf),
                "bbox": box.tolist(),
            })

            if label == "HZRD":
                hzrd_present = True
                x1, y1, x2, y2 = box.tolist()
                area["HZRD"] += ((x2 - x1) * (y2 - y1)) / frame_area

    if hzrd_present:
        alerts.append("🚨 HAZARDOUS ZONE DETECTED")
        PPE_ACTIVE = True
    else:
        PPE_ACTIVE = False

    # ---------- SMOKE (fire omitted) ----------
    smoke_results = smoke_fire_model(frame_bgr, conf=0.4)[0]

    if smoke_results.boxes:
        for box, cls, conf in zip(
            smoke_results.boxes.xyxy,
            smoke_results.boxes.cls,
            smoke_results.boxes.conf,
        ):
            label = smoke_fire_model.names[int(cls)]

            if label.lower() == "smoke":
                x1, y1, x2, y2 = box.tolist()
                area["smoke"] += ((x2 - x1) * (y2 - y1)) / frame_area

                detections.append({
                    "class": "smoke",
                    "confidence": float(conf),
                    "bbox": box.tolist(),
                })

                alerts.append("⚠️ Smoke detected")

    # ---------- PPE (conditional) ----------
    if PPE_ACTIVE:
        ppe_results = ppe_model(frame_bgr, conf=0.4)[0]
        if ppe_results.boxes:
            for box, cls, conf in zip(
                ppe_results.boxes.xyxy,
                ppe_results.boxes.cls,
                ppe_results.boxes.conf,
            ):
                label = ppe_model.names[int(cls)]
                detections.append({
                    "class": label,
                    "confidence": float(conf),
                    "bbox": box.tolist(),
                })

                if label.lower() == "firefighter":
                    alerts.append("🟢 Response team in sight")

    return JSONResponse({
        "detections": detections,
        "alerts": list(set(alerts)),
        "area_coverage": {
            "HZRD": round(area["HZRD"] * 100, 2),
            "smoke": round(area["smoke"] * 100, 2),
        }
    })
