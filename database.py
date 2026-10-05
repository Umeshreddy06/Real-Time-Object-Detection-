from datetime import datetime
import mysql.connector
from mysql.connector import Error
from .config import settings

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS detection_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    object_class VARCHAR(100) NOT NULL,
    confidence DECIMAL(6,4) NOT NULL,
    bbox_x INT NOT NULL,
    bbox_y INT NOT NULL,
    bbox_w INT NOT NULL,
    bbox_h INT NOT NULL
);
"""

def get_connection():
    return mysql.connector.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
    )

def initialize_database():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
    finally:
        cur.close()
        conn.close()

def insert_detection(object_class, confidence, bbox):
    conn = get_connection()
    try:
        cur = conn.cursor()
        x, y, w, h = bbox
        cur.execute(
            """INSERT INTO detection_logs
               (timestamp, object_class, confidence, bbox_x, bbox_y, bbox_w, bbox_h)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (datetime.now(), object_class, float(confidence), int(x), int(y), int(w), int(h)),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def fetch_recent_logs(limit=20):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """SELECT log_id, timestamp, object_class, confidence,
                      bbox_x, bbox_y, bbox_w, bbox_h
               FROM detection_logs
               ORDER BY log_id DESC LIMIT %s""",
            (int(limit),),
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def fetch_summary():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM detection_logs")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT object_class) FROM detection_logs")
        classes = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(AVG(confidence),0) FROM detection_logs")
        avg_conf = float(cur.fetchone()[0] or 0)
        return total, classes, avg_conf
    finally:
        cur.close()
        conn.close()
