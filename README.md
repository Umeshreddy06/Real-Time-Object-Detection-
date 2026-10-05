# Real-Time Object Detection & Logging Platform

Assignment 5 — Python, OpenCV, Ultralytics YOLO, MySQL and Streamlit.

## Features

- Real-time webcam object detection
- YOLO pre-trained model (`yolov8n.pt`)
- Adjustable confidence threshold
- Object-class filtering
- Bounding boxes with class and confidence
- MySQL event logging
- Modular architecture
- Streamlit dashboard
- Recent detection log table
- Secure `.env` configuration
- GitHub-ready project structure

## Project Structure

```text
Real-Time-Object-Detection-Assignment5/
├── main.py
├── requirements.txt
├── database_schema.sql
├── .env.example
├── .gitignore
├── README.md
└── src/
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── detector.py
    └── ui.py
```

## 1. Install Python

Use Python 3.10 or 3.11 for a smooth local setup.

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure MySQL

Start MySQL using XAMPP, WAMP or MySQL Server.

Open MySQL Workbench/phpMyAdmin and run:

```sql
CREATE DATABASE vision_platform;
```

Then run the complete `database_schema.sql` file.

## 5. Configure environment variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Edit the values for your MySQL installation.

Example:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=vision_platform
CAMERA_INDEX=0
YOLO_MODEL=yolov8n.pt
```

**Never upload `.env` to GitHub.**

## 6. Run the application

```bash
streamlit run main.py
```

A browser page will open. Allow camera access if requested.

## 7. Demonstration flow

For the 1–2 minute demo:

1. Show the project folder.
2. Show `main.py`, `detector.py`, `database.py`, and `ui.py`.
3. Start MySQL.
4. Start Streamlit.
5. Show the webcam feed.
6. Show YOLO bounding boxes around a person/cell phone.
7. Change the confidence threshold.
8. Change the object filter.
9. Show the recent detection logs in the dashboard.
10. Open MySQL and show new rows being inserted.

## 8. GitHub

Create a repository named:

`Real-Time-Object-Detection`

Then:

```bash
git init
git add .
git commit -m "Initial Assignment 5 project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Real-Time-Object-Detection.git
git push -u origin main
```

Before pushing, verify:

```bash
git status
```

Make sure `.env` is NOT listed.

## 9. Medium article

Suggested title:

**Building a Real-Time Object Detection and Logging Platform with YOLO, OpenCV, Streamlit and MySQL**

Include:
- Introduction
- What I learned about OpenCV
- YOLO object detection
- Modular architecture
- MySQL event logging
- Streamlit dashboard
- Challenges and solutions
- Screenshots
- GitHub link
- Demo video link
- Final result

## 10. Submission links

Submit these three links in the assignment form:

- GitHub repository URL
- Google Drive/YouTube unlisted demo URL
- Medium article URL

## Troubleshooting

### Camera does not open
- Allow camera permission.
- Close other apps using the webcam.
- Try `CAMERA_INDEX=1` in `.env`.

### MySQL connection error
- Make sure MySQL is running.
- Confirm database name is `vision_platform`.
- Check username/password in `.env`.

### YOLO model download
The first run downloads the selected YOLO model automatically. Internet access is required for the first model download.

### Streamlit stops unexpectedly
Run the command again:

```bash
streamlit run main.py
```

## Security

Credentials belong only in `.env`. The `.gitignore` file excludes `.env` from Git.
