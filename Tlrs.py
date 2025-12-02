import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class TLRS:
    def __init__(self, db_path: str = "tlrs_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                keywords TEXT NOT NULL,        -- JSON list
                summary TEXT NOT NULL,
                full_content TEXT,
                metadata TEXT,                -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_memory(self, title: str, keywords: List[str], summary: str,
                   full_content: Optional[str] = None, metadata: Dict = None):
        """Add or update a memory"""
        metadata = json.dumps(metadata or {})
        keywords_json = json.dumps(keywords)

        self.conn.execute("""
            INSERT INTO memories(title, keywords, summary, full_content, metadata)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(title) DO UPDATE SET
                keywords=excluded.keywords,
                summary=excluded.summary,
                full_content=excluded.full_content,
                metadata=excluded.metadata
        """, (title.lower().replace(" ", "_"), keywords_json, summary, full_content, metadata))
        self.conn.commit()

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Fast symbolic + keyword match → returns tiny payloads"""
        query_lower = query.lower()
        words = query_lower.split()

        cursor = self.conn.execute("""
            SELECT title, keywords, summary, metadata FROM memories
            ORDER BY 
                CASE WHEN title LIKE ? THEN 0 ELSE 1 END,
                (SELECT COUNT(*) FROM json_each(keywords) WHERE value IN ("""+",".join("?"*len(words))+"""))
            LIMIT ?
        """, ["%"+query_lower+"%"] + words + [top_k])

        results = []
        for row in cursor.fetchall():
            results.append({
                "title": row["title"],
                "keywords": json.loads(row["keywords"]),
                "summary": row["summary"],
                "metadata": json.loads(row["metadata"])
            })
        return results

    def expand(self, title: str) -> Optional[str]:
        """Lazy-load full content when explicitly requested"""
        cursor = self.conn.execute("SELECT full_content FROM memories WHERE title = ?", (title,))
        row = cursor.fetchone()
        return row[0] if row else None]
