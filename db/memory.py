import json
import sqlite3
import threading
from datetime import datetime
from typing import Any, Dict, List


class MemoryDB:
    def __init__(self, db_file: str = "memory.db"):
        self.db_file = db_file
        self.lock = threading.Lock()
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS jd_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    summary_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cv_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    cv_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS match_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jd_id INTEGER NOT NULL,
                    cv_id INTEGER NOT NULL,
                    score REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS shortlisted (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match_id INTEGER,
                    jd_id INTEGER NOT NULL,
                    cv_id INTEGER NOT NULL,
                    score REAL NOT NULL,
                    email_sent INTEGER DEFAULT 0,
                    email_sent_at TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            self.conn.commit()

    def insert_jd_summary(self, job_title: str, summary: Dict[str, Any]) -> int:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO jd_summaries (job_title, summary_json, created_at) VALUES (?, ?, ?)",
                (job_title, json.dumps(summary), datetime.now().isoformat()),
            )
            self.conn.commit()
            return int(cursor.lastrowid)

    def insert_cv_data(self, filename: str, cv_data: Dict[str, Any]) -> int:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO cv_data (filename, cv_json, created_at) VALUES (?, ?, ?)",
                (filename, json.dumps(cv_data), datetime.now().isoformat()),
            )
            self.conn.commit()
            return int(cursor.lastrowid)

    def insert_match_score(self, jd_id: int, cv_id: int, score: float) -> int:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO match_scores (jd_id, cv_id, score, created_at) VALUES (?, ?, ?, ?)",
                (jd_id, cv_id, score, datetime.now().isoformat()),
            )
            self.conn.commit()
            return int(cursor.lastrowid)

    def insert_shortlisted(self, match_id: int, jd_id: int, cv_id: int, score: float) -> int:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO shortlisted (match_id, jd_id, cv_id, score, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (match_id, jd_id, cv_id, score, datetime.now().isoformat()),
            )
            self.conn.commit()
            return int(cursor.lastrowid)

    def get_all_jds(self) -> List[Dict[str, Any]]:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, job_title, summary_json, created_at FROM jd_summaries ORDER BY id DESC")
            rows = cursor.fetchall()

        result: List[Dict[str, Any]] = []
        for row in rows:
            summary = json.loads(row["summary_json"]) if row["summary_json"] else {}
            item = {
                "id": row["id"],
                "job_title": row["job_title"],
                "created_at": row["created_at"],
            }
            if isinstance(summary, dict):
                item.update(summary)
            result.append(item)
        return result

    def get_all_cvs(self) -> List[Dict[str, Any]]:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, filename, cv_json, created_at FROM cv_data ORDER BY id DESC")
            rows = cursor.fetchall()

        result: List[Dict[str, Any]] = []
        for row in rows:
            cv_data = json.loads(row["cv_json"]) if row["cv_json"] else {}
            item = {
                "id": row["id"],
                "filename": row["filename"],
                "created_at": row["created_at"],
            }
            if isinstance(cv_data, dict):
                item.update(cv_data)
            result.append(item)
        return result

    def get_shortlisted_candidates(self) -> List[Dict[str, Any]]:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT s.id, s.score, s.created_at, s.email_sent, s.email_sent_at,
                       j.job_title,
                       c.filename,
                       c.cv_json
                FROM shortlisted s
                JOIN jd_summaries j ON j.id = s.jd_id
                JOIN cv_data c ON c.id = s.cv_id
                ORDER BY s.id DESC
                """
            )
            rows = cursor.fetchall()

        result: List[Dict[str, Any]] = []
        for row in rows:
            cv_data = json.loads(row["cv_json"]) if row["cv_json"] else {}
            result.append(
                {
                    "id": row["id"],
                    "job_title": row["job_title"],
                    "filename": row["filename"],
                    "score": row["score"],
                    "email_sent": bool(row["email_sent"]),
                    "email_sent_at": row["email_sent_at"],
                    "created_at": row["created_at"],
                    "name": cv_data.get("name", "Unknown"),
                    "email": cv_data.get("email", ""),
                }
            )
        return result

    def close(self) -> None:
        with self.lock:
            self.conn.close()
