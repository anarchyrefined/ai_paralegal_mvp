import sqlite3
import json
import uuid
from datetime import datetime
from celery import Celery
from .main import run_langgraph_workflow  # Import the workflow function

# Initialize Celery (optional, can be disabled for simple setups)
try:
    celery_app = Celery('ai_paralegal', broker='redis://localhost:6379/0')
    CELERY_ENABLED = True
except Exception as e:
    logger.warning(f"Celery not available: {e}. Running synchronously.")
    CELERY_ENABLED = False
    celery_app = None

# Database setup
def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        task TEXT,
        persona TEXT,
        status TEXT,
        result TEXT,
        created_at TEXT,
        updated_at TEXT
    )''')
    conn.commit()
    conn.close()

def create_job(task: str, persona: str):
    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('INSERT INTO jobs (id, task, persona, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
              (job_id, task, persona, 'pending', created_at, created_at))
    conn.commit()
    conn.close()
    # Queue the job or run synchronously
    if CELERY_ENABLED:
        process_job.delay(job_id, task, persona)
    else:
        # Run synchronously for simple setups
        process_job_sync(job_id, task, persona)
    return job_id

def get_job_status(job_id: str):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('SELECT status, result FROM jobs WHERE id = ?', (job_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'status': row[0], 'result': row[1]}
    return None

def update_job_status(job_id: str, status: str, result: str = None):
    updated_at = datetime.utcnow().isoformat()
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('UPDATE jobs SET status = ?, result = ?, updated_at = ? WHERE id = ?',
              (status, result, updated_at, job_id))
    conn.commit()
    conn.close()

@celery_app.task
def process_job(job_id: str, task: str, persona: str):
    try:
        update_job_status(job_id, 'running')
        result = run_langgraph_workflow(task, persona)
        update_job_status(job_id, 'completed', json.dumps(result))
    except Exception as e:
        update_job_status(job_id, 'failed', str(e))

def process_job_sync(job_id: str, task: str, persona: str):
    """Synchronous job processing for setups without Celery."""
    try:
        update_job_status(job_id, 'running')
        result = run_langgraph_workflow(task, persona)
        update_job_status(job_id, 'completed', json.dumps(result))
    except Exception as e:
        update_job_status(job_id, 'failed', str(e))

# Initialize DB on import
init_db()
