import pytest
import sqlite3
import os
from datetime import datetime
from api.service.jobs import create_job, get_job_status, update_job_status, process_job_sync

def setup_test_db():
    """Set up in-memory SQLite database for testing"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE jobs (
            id TEXT PRIMARY KEY,
            task TEXT NOT NULL,
            persona TEXT NOT NULL,
            status TEXT NOT NULL,
            result TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def test_create_job():
    conn = setup_test_db()
    job_id = create_job("Test task", "LegalAnalyst", conn)

    assert job_id is not None
    assert isinstance(job_id, str)

    # Verify job was created
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()

    assert job is not None
    assert job[1] == "Test task"
    assert job[2] == "LegalAnalyst"
    assert job[3] == "pending"

    conn.close()

def test_get_job_status():
    conn = setup_test_db()
    job_id = create_job("Test task", "LegalAnalyst", conn)

    status = get_job_status(job_id, conn)

    assert status is not None
    assert status["status"] == "pending"
    assert status["task"] == "Test task"
    assert status["persona"] == "LegalAnalyst"
    assert "created_at" in status
    assert "updated_at" in status

    conn.close()

def test_update_job_status():
    conn = setup_test_db()
    job_id = create_job("Test task", "LegalAnalyst", conn)

    update_job_status(job_id, "completed", "Test result", conn)

    status = get_job_status(job_id, conn)
    assert status["status"] == "completed"
    assert status["result"] == "Test result"

    conn.close()

def test_process_job_sync():
    conn = setup_test_db()
    job_id = create_job("Test task", "LegalAnalyst", conn)

    # Process the job
    result = process_job_sync(job_id, conn)

    # Verify job was processed
    status = get_job_status(job_id, conn)
    assert status["status"] in ["completed", "failed"]
    assert "result" in status

    conn.close()

def test_get_nonexistent_job():
    conn = setup_test_db()
    status = get_job_status("nonexistent_job", conn)

    assert status is None

    conn.close()

def test_job_timestamps():
    conn = setup_test_db()
    before_create = datetime.now().isoformat()

    job_id = create_job("Test task", "LegalAnalyst", conn)

    status = get_job_status(job_id, conn)

    assert status["created_at"] >= before_create
    assert status["updated_at"] >= status["created_at"]

    conn.close()

def test_job_status_progression():
    conn = setup_test_db()
    job_id = create_job("Test task", "LegalAnalyst", conn)

    # Initial status
    status = get_job_status(job_id, conn)
    assert status["status"] == "pending"

    # Update to processing
    update_job_status(job_id, "processing", None, conn)
    status = get_job_status(job_id, conn)
    assert status["status"] == "processing"

    # Update to completed
    update_job_status(job_id, "completed", "Final result", conn)
    status = get_job_status(job_id, conn)
    assert status["status"] == "completed"
    assert status["result"] == "Final result"

    conn.close()

def test_multiple_jobs():
    conn = setup_test_db()

    job1 = create_job("Task 1", "LegalAnalyst", conn)
    job2 = create_job("Task 2", "ContractReviewer", conn)

    assert job1 != job2

    status1 = get_job_status(job1, conn)
    status2 = get_job_status(job2, conn)

    assert status1["task"] == "Task 1"
    assert status2["task"] == "Task 2"

    conn.close()
