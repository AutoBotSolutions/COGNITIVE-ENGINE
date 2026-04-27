"""
Persistent memory system for the Cognitive Engine

Implements three-layer memory architecture:
1. Episodic Memory (raw events)
2. Pattern Memory (structure extraction)
3. Rule Memory (learned strategies)
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import sqlite3
import json
from pathlib import Path

from core.config import config


class MemoryBackend:
    """Base class for memory backends"""
    
    def store(self, key: str, value: Any) -> bool:
        raise NotImplementedError
    
    def retrieve(self, key: str) -> Optional[Any]:
        raise NotImplementedError
    
    def search(self, query: str) -> List[Any]:
        raise NotImplementedError


class SQLiteMemory(MemoryBackend):
    """SQLite-based memory implementation"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.memory_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Episodic memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                data JSON,
                metadata JSON
            )
        """)
        
        # Pattern memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_text TEXT,
                confidence REAL,
                frequency INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Rule memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_text TEXT,
                rule_type TEXT,
                confidence REAL,
                usage_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_episodic(self, event_type: str, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> bool:
        """Store an episodic memory event"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO episodic (event_type, data, metadata) VALUES (?, ?, ?)",
                (event_type, json.dumps(data), json.dumps(metadata or {}))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing episodic memory: {e}")
            return False
    
    def retrieve_episodic(self, limit: int = 100, event_type: str = None) -> List[Dict[str, Any]]:
        """Retrieve episodic memories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if event_type:
                cursor.execute(
                    "SELECT * FROM episodic WHERE event_type = ? ORDER BY timestamp DESC LIMIT ?",
                    (event_type, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM episodic ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": row[0],
                    "timestamp": row[1],
                    "event_type": row[2],
                    "data": json.loads(row[3]),
                    "metadata": json.loads(row[4])
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error retrieving episodic memory: {e}")
            return []
    
    def store_pattern(self, pattern_text: str, confidence: float) -> bool:
        """Store a pattern in pattern memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if pattern already exists
            cursor.execute(
                "SELECT id, frequency FROM patterns WHERE pattern_text = ?",
                (pattern_text,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing pattern
                cursor.execute(
                    "UPDATE patterns SET frequency = frequency + 1, confidence = ?, last_seen = CURRENT_TIMESTAMP WHERE id = ?",
                    (confidence, existing[0])
                )
            else:
                # Insert new pattern
                cursor.execute(
                    "INSERT INTO patterns (pattern_text, confidence, frequency) VALUES (?, ?, 1)",
                    (pattern_text, confidence)
                )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing pattern: {e}")
            return False
    
    def retrieve_patterns(self, min_confidence: float = 0.5, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve patterns above confidence threshold"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM patterns WHERE confidence >= ? ORDER BY frequency DESC LIMIT ?",
                (min_confidence, limit)
            )
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": row[0],
                    "pattern_text": row[1],
                    "confidence": row[2],
                    "frequency": row[3],
                    "created_at": row[4],
                    "last_seen": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error retrieving patterns: {e}")
            return []
    
    def store_rule(self, rule_text: str, rule_type: str, confidence: float) -> bool:
        """Store a rule in rule memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO rules (rule_text, rule_type, confidence) VALUES (?, ?, ?)",
                (rule_text, rule_type, confidence)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing rule: {e}")
            return False
    
    def retrieve_rules(self, rule_type: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve rules by type"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if rule_type:
                cursor.execute(
                    "SELECT * FROM rules WHERE rule_type = ? ORDER BY usage_count DESC LIMIT ?",
                    (rule_type, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM rules ORDER BY usage_count DESC LIMIT ?",
                    (limit,)
                )
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": row[0],
                    "rule_text": row[1],
                    "rule_type": row[2],
                    "confidence": row[3],
                    "usage_count": row[4],
                    "created_at": row[5],
                    "last_used": row[6]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error retrieving rules: {e}")
            return []
    
    def increment_rule_usage(self, rule_id: int) -> bool:
        """Increment usage count for a rule"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE rules SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP WHERE id = ?",
                (rule_id,)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error incrementing rule usage: {e}")
            return False


# Singleton memory instance
memory = SQLiteMemory()
