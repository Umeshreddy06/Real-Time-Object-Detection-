from collections import Counter
import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_name="yolov8n.pt", confidence=0.70, allowed_classes=None):
        self.model = YOLO(model_name)
        self.confidence = confidence
        self.allowed_classes = set(allowed_classes or [])

    def detect(self, frame):
        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False
        )
        detections = []
        annotated = frame.copy()

        for result in results:
            names = result.names
            if result.boxes is None:
                continue

            for box in result.boxes:
                cls_id = int(box.cls[0])
                class_name = names[cls_id]
                conf = float(box.conf[0])

                if self.allowed_classes and class_name not in self.allowed_classes:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                w, h = x2 - x1, y2 - y1
                detections.append({
                    "object_class": class_name,
                    "confidence": conf,
                    "bbox": (x1, y1, w, h)
                })

                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name} {conf:.0%}"
                cv2.putText(
                    annotated, label, (x1, max(20, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                )

        return annotated, detections

    @staticmethod
    def metrics(detections):
        counts = Counter(d["object_class"] for d in detections)
        avg_conf = (
            sum(d["confidence"] for d in detections) / len(detections)
            if detections else 0
        )
        return len(detections), avg_conf, dict(counts)
