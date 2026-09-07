import json
import logging
import os
import sqlite3
import time
from typing import Any

import pandas as pd

logger = logging.getLogger("CacheManager")

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cache.db")


class CacheManager:
    """
    Lightweight, persistent SQLite cache with TTL and Stale-While-Revalidate semantics.
    Supports Python primitives/dicts and pandas DataFrames.
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=15.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS data_cache (
                        key TEXT PRIMARY KEY,
                        namespace TEXT NOT NULL,
                        data_json TEXT NOT NULL,
                        is_dataframe INTEGER NOT NULL DEFAULT 0,
                        expires_at REAL NOT NULL,
                        updated_at REAL NOT NULL
                    )
                    """
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_namespace_key ON data_cache (namespace, key)"
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize SQLite cache at {self.db_path}: {e}")

    def _serialize(self, value: Any) -> tuple[str, int]:
        if isinstance(value, pd.DataFrame):
            return value.to_json(orient="split", date_format="iso"), 1
        return json.dumps(value, default=str), 0

    def _deserialize(self, raw_json: str, is_dataframe: int) -> Any:
        if is_dataframe:
            import io
            return pd.read_json(io.StringIO(raw_json), orient="split")
        return json.loads(raw_json)

    def set(self, namespace: str, key: str, value: Any, ttl_seconds: int = 900) -> bool:
        """
        Stores a value in the cache with a specified TTL (default 15 minutes).
        """
        composite_key = f"{namespace}:{key}"
        now = time.time()
        expires_at = now + ttl_seconds
        try:
            raw_data, is_df = self._serialize(value)
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO data_cache (key, namespace, data_json, is_dataframe, expires_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET
                        data_json = excluded.data_json,
                        is_dataframe = excluded.is_dataframe,
                        expires_at = excluded.expires_at,
                        updated_at = excluded.updated_at
                    """,
                    (composite_key, namespace, raw_data, is_df, expires_at, now),
                )
                conn.commit()
            return True
        except Exception as e:
            logger.warning(f"Cache set error for [{composite_key}]: {e}")
            return False

    def get(self, namespace: str, key: str, default: Any = None) -> Any:
        """
        Retrieves a non-expired cached value. Returns `default` if expired or missing.
        """
        composite_key = f"{namespace}:{key}"
        now = time.time()
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT data_json, is_dataframe, expires_at FROM data_cache WHERE key = ?",
                    (composite_key,),
                )
                row = cursor.fetchone()
                if row and row["expires_at"] > now:
                    return self._deserialize(row["data_json"], row["is_dataframe"])
        except Exception as e:
            logger.warning(f"Cache get error for [{composite_key}]: {e}")
        return default

    def get_stale(self, namespace: str, key: str, default: Any = None) -> Any:
        """
        Retrieves the last known cached value regardless of expiration (Stale-While-Revalidate).
        Ideal for fallback when live network fetches fail.
        """
        composite_key = f"{namespace}:{key}"
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT data_json, is_dataframe FROM data_cache WHERE key = ?",
                    (composite_key,),
                )
                row = cursor.fetchone()
                if row:
                    return self._deserialize(row["data_json"], row["is_dataframe"])
        except Exception as e:
            logger.warning(f"Cache get_stale error for [{composite_key}]: {e}")
        return default

    def clear(self, namespace: str | None = None) -> int:
        """
        Clears cache items. If namespace is provided, clears only items in that namespace.
        """
        try:
            with self._get_connection() as conn:
                if namespace:
                    cursor = conn.execute(
                        "DELETE FROM data_cache WHERE namespace = ?", (namespace,)
                    )
                else:
                    cursor = conn.execute("DELETE FROM data_cache")
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return 0


# Global singleton instance
cache_manager = CacheManager()
