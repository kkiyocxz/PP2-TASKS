# db.py — PostgreSQL integration via psycopg2

import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

_conn = None


def get_connection():
    global _conn
    if _conn is None or _conn.closed:
        try:
            _conn = psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError as e:
            print(f"[DB] Connection failed: {e}")
            _conn = None
    return _conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id       SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id            SERIAL PRIMARY KEY,
                    player_id     INTEGER REFERENCES players(id),
                    score         INTEGER   NOT NULL,
                    level_reached INTEGER   NOT NULL,
                    played_at     TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB] init_db error: {e}")
        conn.rollback()
        return False


def get_or_create_player(username: str) -> int | None:
    """Return player id, creating the row if needed."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) "
                "ON CONFLICT (username) DO NOTHING RETURNING id;",
                (username,)
            )
            row = cur.fetchone()
            if row:
                conn.commit()
                return row[0]
            # already existed
            cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
            return cur.fetchone()[0]
    except Exception as e:
        print(f"[DB] get_or_create_player error: {e}")
        conn.rollback()
        return None


def save_session(username: str, score: int, level: int) -> bool:
    """Save a completed game session."""
    conn = get_connection()
    if conn is None:
        return False
    pid = get_or_create_player(username)
    if pid is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) "
                "VALUES (%s, %s, %s);",
                (pid, score, level)
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB] save_session error: {e}")
        conn.rollback()
        return False


def get_personal_best(username: str) -> int:
    """Return the highest score for this player, or 0."""
    conn = get_connection()
    if conn is None:
        return 0
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT MAX(gs.score) "
                "FROM game_sessions gs "
                "JOIN players p ON p.id = gs.player_id "
                "WHERE p.username = %s;",
                (username,)
            )
            row = cur.fetchone()
            return row[0] if row and row[0] is not None else 0
    except Exception as e:
        print(f"[DB] get_personal_best error: {e}")
        return 0


def get_leaderboard(limit: int = 10) -> list[dict]:
    """Return top N all-time scores."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT p.username, gs.score, gs.level_reached, "
                "       TO_CHAR(gs.played_at, 'YYYY-MM-DD') "
                "FROM game_sessions gs "
                "JOIN players p ON p.id = gs.player_id "
                "ORDER BY gs.score DESC "
                "LIMIT %s;",
                (limit,)
            )
            rows = cur.fetchall()
            return [
                {"rank": i + 1, "username": r[0], "score": r[1],
                 "level": r[2], "date": r[3]}
                for i, r in enumerate(rows)
            ]
    except Exception as e:
        print(f"[DB] get_leaderboard error: {e}")
        return []
