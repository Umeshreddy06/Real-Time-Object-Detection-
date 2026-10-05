# Building a Real-Time Object Detection and Logging Platform with YOLO, OpenCV, Streamlit and MySQL

## Introduction

For Assignment 5, I built a real-time computer vision platform that detects objects from a webcam and records detection events in a MySQL database.

The project combines Python, OpenCV, Ultralytics YOLO, Streamlit and MySQL.

## Computer Vision and YOLO Learning

I learned how OpenCV can capture webcam frames, convert image formats and display real-time video. I used the Ultralytics YOLO model to detect objects and obtain class names, confidence scores and bounding-box coordinates.

The application allows the user to select which object classes should be detected and to adjust the minimum confidence threshold.

## Modular Application Development

I separated the project into modules:

- `detector.py` — YOLO detection and bounding-box processing
- `database.py` — MySQL connection and event logging
- `config.py` — environment-based configuration
- `ui.py` — Streamlit dashboard
- `main.py` — application entry point

This structure makes the application easier to test, maintain and extend.

## Database Integration

I created a MySQL database named `vision_platform`.

The `detection_logs` table stores:

- log ID
- timestamp
- object class
- confidence
- bounding-box X and Y
- bounding-box width and height

Whenever a qualifying detection is made, the application inserts an event into MySQL.

## User Interface

The Streamlit dashboard displays:

- live annotated camera feed
- confidence threshold
- object selection
- live detection count
- average confidence
- total database events
- recent MySQL logs

## Challenges and Solutions

### Camera access

One challenge was ensuring that the application could access the webcam. I handled this with OpenCV's `VideoCapture` and included a configurable camera index.

### Too many database records

Logging every detection in every frame could create an unnecessarily large number of database records. I therefore added a configurable minimum logging interval for each object class.

### Security

Database credentials are stored in `.env` rather than being hardcoded. The `.gitignore` file prevents `.env` from being uploaded to GitHub.

## Final Result

The completed platform demonstrates a complete pipeline:

**Webcam → OpenCV → YOLO → Bounding Boxes → MySQL Logging → Streamlit Dashboard**

### GitHub

Add your repository link here:

`YOUR_GITHUB_LINK`

### Demo Video

Add your Google Drive or YouTube unlisted link here:

`YOUR_DEMO_VIDEO_LINK`

### Screenshots

Add screenshots of the Streamlit dashboard, YOLO detection and MySQL detection table here.

## Conclusion

This project helped me understand how computer vision, object detection, databases and user interfaces can be combined into a practical real-time application. I also learned the importance of modular code organization and keeping credentials secure.
