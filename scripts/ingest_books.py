# scripts/ingest_books.py
"""
Hardened multi-book ingest with retry, DQ checks, and audit logging.
Simulates bookmaker feed ingestion (Pinnacle, SBO, ISN, Betfair).
"""

import os
import json
import random
import time
from datetime import datetime, timezone

ARTIFACTS_DIR = "artifacts"
AUDIT_PATH = os.path.join(ARTIFACTS_DIR, "ingest_audit.json")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

BOOKS = ["Pinnacle", "SBO", "ISN", "Betfair"]

def simulate_fetch(book: str):
    """Simulated feed fetch with possible failure/delay."""
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)
    if random.random() < 0.1:  # 10% chance of transient failure
        raise ConnectionError(f"{book} feed timeout.")
    rows = random.randint(80, 150)
    return {"book": book, "rows": rows, "delay": delay}

def fetch_with_retry(book, retries=3, backoff=1.5):
    """Attempt fetch with exponential backoff retry."""
    attempt = 1
    while attempt <= retries:
        try:
            result = simulate_fetch(book)
            result["status"] = "OK"
            return result
        except Exception as e:
            print(f"[WARN] {book}: {e} (attempt {attempt}/{retries})")
            if attempt == retries:
                return {"book": book, "status": "FAIL", "error": str(e)}
            time.sleep(backoff ** attempt)
            attempt += 1

def dq_check(result):
    """Basic data-quality check."""
    if result.get("status") != "OK":
        return "FAILED_FETCH"
    if result["rows"] < 50:
        return "LOW_ROWCOUNT"
    return "PASS"

def main():
    print("=== Starting Multi-Book Ingest ===")
    results = []
    for book in BOOKS:
        result = fetch_with_retry(book)
        dq_status = dq_check(result)
        result["dq_status"] = dq_status
        results.append(result)

    audit = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_books": len(BOOKS),
            "successful": sum(1 for r in results if r["status"] == "OK"),
            "dq_pass": sum(1 for r in results if r["dq_status"] == "PASS"),
        },
        "details": results,
    }

    with open(AUDIT_PATH, "w") as f:
        json.dump(audit, f, indent=2)

    print(f"[INFO] Audit written → {AUDIT_PATH}")
    print(json.dumps(audit, indent=2))
    print("=== Ingest Complete ===")

    # Fail fast if ingestion quality too low
    if audit["summary"]["dq_pass"] < len(BOOKS) // 2:
        raise SystemExit("[ERROR] Too few clean ingests. Aborting pipeline.")

if __name__ == "__main__":
    main()
