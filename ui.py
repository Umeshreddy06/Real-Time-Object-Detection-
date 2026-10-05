import time
import cv2
import streamlit as st
from .config import settings
from .detector import ObjectDetector
from .database import initialize_database, insert_detection, fetch_recent_logs, fetch_summary

COCO_CLASSES = [
    "person","bicycle","car","motorcycle","airplane","bus","train","truck","boat",
    "traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat",
    "dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
    "umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball",
    "kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket",
    "bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple",
    "sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair",
    "couch","potted plant","bed","dining table","toilet","tv","laptop","mouse",
    "remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator",
    "book","clock","vase","scissors","teddy bear","hair drier","toothbrush"
]

def run_app():
    st.title("🎯 Real-Time Object Detection & Logging Platform")
    st.caption("Python + OpenCV + Ultralytics YOLO + MySQL + Streamlit")

    with st.sidebar:
        st.header("⚙️ Detection Settings")
        confidence = st.slider("Confidence threshold", 0.10, 0.95, 0.70, 0.05)
        selected = st.multiselect(
            "Objects to detect",
            COCO_CLASSES,
            default=["person", "cell phone"]
        )
        log_interval = st.slider("Minimum log interval per class (seconds)", 0.5, 10.0, 2.0, 0.5)
        camera_index = st.number_input("Camera index", min_value=0, max_value=5, value=settings.camera_index)

    col1, col2, col3 = st.columns(3)
    try:
        total, classes, avg_conf = fetch_summary()
    except Exception:
        total, classes, avg_conf = 0, 0, 0
        st.warning("MySQL is not connected yet. Start MySQL and create the database, then refresh.")

    col1.metric("Total Logged Events", total)
    col2.metric("Object Classes", classes)
    col3.metric("Average Confidence", f"{avg_conf:.1%}")

    if "running" not in st.session_state:
        st.session_state.running = False

    c1, c2 = st.columns(2)
    if c1.button("▶ Start Camera", use_container_width=True):
        st.session_state.running = True
    if c2.button("⏹ Stop Camera", use_container_width=True):
        st.session_state.running = False

    frame_slot = st.empty()
    metrics_slot = st.empty()

    if st.session_state.running:
        try:
            initialize_database()
        except Exception as e:
            st.error(f"MySQL connection failed: {e}")
            st.info("Run database_schema.sql first and check your .env credentials.")
            st.session_state.running = False
            return

        detector = ObjectDetector(
            model_name=settings.model_name,
            confidence=confidence,
            allowed_classes=selected,
        )
        cap = cv2.VideoCapture(int(camera_index))
        last_logged = {}

        if not cap.isOpened():
            st.error("Could not open the camera. Check permissions and camera index.")
            st.session_state.running = False
            return

        while st.session_state.running:
            ok, frame = cap.read()
            if not ok:
                st.error("Could not read a frame from the camera.")
                break

            annotated, detections = detector.detect(frame)

            now = time.time()
            for d in detections:
                key = d["object_class"]
                if now - last_logged.get(key, 0) >= log_interval:
                    try:
                        insert_detection(d["object_class"], d["confidence"], d["bbox"])
                        last_logged[key] = now
                    except Exception as e:
                        st.warning(f"Logging error: {e}")

            count, avg, by_class = detector.metrics(detections)
            metrics_slot.info(
                f"**Live detections:** {count}  |  **Average confidence:** {avg:.1%}  |  "
                f"**Classes:** {by_class or 'None'}"
            )

            frame_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            frame_slot.image(frame_rgb, channels="RGB", use_container_width=True)

            time.sleep(0.01)

        cap.release()

    st.divider()
    st.subheader("🗃️ Recent MySQL Detection Logs")
    try:
        logs = fetch_recent_logs(20)
        st.dataframe(logs, use_container_width=True)
    except Exception as e:
        st.info(f"Logs will appear here after MySQL is connected: {e}")
