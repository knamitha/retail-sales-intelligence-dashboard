"""
db.py — Shared database connection for the ETL pipeline.
"""

import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Did you set it in the previous cell?")

engine = create_engine(DATABASE_URL)
