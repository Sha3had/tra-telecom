import os
import pandas as pd
from sqlalchemy import create_engine

from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:1234@mysql:3306/telecom_db"
)
# =========================
# DATABASE CONNECTION
# =========================

DB_USER = "root"
DB_PASSWORD = "1234"
DB_HOST = "telecom_mysql"
DB_PORT = "3306"
DB_NAME = "telecom_db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# =========================
# FILE PATHS
# =========================

RAW_FILE = "data/raw/telecom_data.csv"
PROCESSED_FILE = "data/processed/telecom_processed.csv"


# =========================
# EXTRACT
# =========================

def extract():
    print("🔹 Extract started")

    df = pd.read_csv(
        RAW_FILE,
        comment="#",
        skiprows=[1, 2, 3]  # يتجاهل العناوين العربية + الفراغات
    )

    print(f"✅ Loaded: {len(df)} rows")
    return df


def transform(df):
    print("🔹 Transform started")

    # تنظيف أسماء الأعمدة
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # تنظيف الأرقام اللي فيها commas
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(",", "")

    # تحويل الأعمدة الرقمية
    numeric_cols = [
        "year", "quarter",
        "fiber_optic", "adsl",
        "fixed_4g", "fixed_5g",
        "satellite", "other",
        "total_fixed_broadband"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # rename
    if "other" in df.columns:
        df = df.rename(columns={"other": "other_service"})

    # حذف فقط بعد التنظيف
    df = df.dropna().reset_index(drop=True)

    # ترتيب
    df = df.sort_values(["year", "quarter"])

    # =========================
    # Features
    # =========================

    df["growth_rate"] = df["total_fixed_broadband"].pct_change() * 100
    df["usage_per_service"] = df["total_fixed_broadband"] / 6
    df["quarterly_change"] = df["total_fixed_broadband"].diff()

    min_val = df["total_fixed_broadband"].min()
    max_val = df["total_fixed_broadband"].max()

    df["normalized_traffic_index"] = (
        (df["total_fixed_broadband"] - min_val) /
        (max_val - min_val)
    )

    # حفظ
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_FILE, index=False)

    print("✅ Transform done - rows:", len(df))
    return df

# =========================
# LOAD
# =========================

import os
import sqlite3

def load(df, engine):
    print("🔹 Load started")

    # Create local db folder
    os.makedirs("db", exist_ok=True)

    # -----------------------------
    # MySQL columns
    # -----------------------------
    raw_columns = [
        "year",
        "quarter",
        "fiber_optic",
        "adsl",
        "fixed_4g",
        "fixed_5g",
        "satellite",
        "other_service",
        "total_fixed_broadband"
    ]

    analytics_columns = [
        "year",
        "quarter",
        "total_fixed_broadband",
        "growth_rate",
        "usage_per_service",
        "quarterly_change",
        "normalized_traffic_index"
    ]

    # -----------------------------
    # MySQL LOAD
import os
import sqlite3

def load(df, engine):
    print("🔹 Load started")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "db", "telecom.db")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    raw_columns = [
        "year","quarter","fiber_optic","adsl","fixed_4g",
        "fixed_5g","satellite","other_service","total_fixed_broadband"
    ]

    analytics_columns = [
        "year","quarter","total_fixed_broadband",
        "growth_rate","usage_per_service",
        "quarterly_change","normalized_traffic_index"
    ]

    # MySQL
    df[raw_columns].to_sql("raw_telecom_data", engine, if_exists="replace", index=False)
    df[analytics_columns].to_sql("telecom_analytics", engine, if_exists="replace", index=False)

    print("✅ Data loaded into MySQL")

    # SQLite (FIXED PATH)
    conn = sqlite3.connect(db_path)

    df[raw_columns].to_sql("raw_telecom_data", conn, if_exists="replace", index=False)
    df[analytics_columns].to_sql("telecom_analytics", conn, if_exists="replace", index=False)

    conn.close()

    print("📁 SQLite DB created at:", db_path)

# =========================
# RUN PIPELINE
# =========================

def run_pipeline():
    df = extract()
    df = transform(df)
    load(df, engine)   # ✅ FIXED

    print("🎉 Pipeline finished")


if __name__ == "__main__":
    run_pipeline()