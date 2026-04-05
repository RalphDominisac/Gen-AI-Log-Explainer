from sqlalchemy import create_engine, text
import os
import time

# ================================
# 🔧 CONFIGURATION 
# ================================
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# ================================
# 🔌 CREATE DATABASE ENGINE
# ================================
def get_engine():

    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        raise ValueError("Database environment variables are not set properly.")

    return create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}",
        connect_args={
            "ssl": {
                "ssl": {}
            }
        },
        pool_pre_ping=True
    )


# ================================
# 💾 SAVE LOG + ANALYSIS
# ================================
def save_log(log_text, analysis, retries=3):
    engine = get_engine()

    for attempt in range(retries):
        try:
            with engine.connect() as conn:
                query = text("""
                    INSERT INTO logs (log_text, analysis)
                    VALUES (:log_text, :analysis)
                """)
                conn.execute(query, {
                    "log_text": log_text,
                    "analysis": analysis
                })
                conn.commit()
                return

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise e


# ================================
# 📜 FETCH RECENT LOGS (OPTIONAL)
# ================================
def fetch_logs(limit=5):
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM logs ORDER BY created_at DESC LIMIT :limit"),
            {"limit": limit}
        )

        return result.fetchall()