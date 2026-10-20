import sqlite3, json, time, os
DB = os.getenv("DB_PATH", "plans.db")

def init_db():
    with sqlite3.connect(DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created REAL, brief TEXT, plan TEXT
        )""")

def save_plan(brief: dict, plan: dict) -> int:
    with sqlite3.connect(DB) as c:
        cur = c.execute("INSERT INTO plans (created, brief, plan) VALUES (?,?,?)",
                        (time.time(), json.dumps(brief), json.dumps(plan)))
        return cur.lastrowid

def list_plans():
    with sqlite3.connect(DB) as c:
        rows = c.execute("SELECT id, created, brief FROM plans ORDER BY created DESC").fetchall()
    return [{"id": r[0], "created": r[1], "brief": json.loads(r[2])} for r in rows]

def get_plan(pid: int):
    with sqlite3.connect(DB) as c:
        row = c.execute("SELECT id, created, brief, plan FROM plans WHERE id=?", (pid,)).fetchone()
    if not row: return None
    return {"id": row[0], "created": row[1],
            "brief": json.loads(row[2]), "plan": json.loads(row[3])}