from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

ENGINE = create_engine("sqlite:///demo.db", future=True, echo=False)

def run_query(sql: str) -> list[dict]:
    with Session(ENGINE) as session:
        rows = session.execute(text(sql)).mappings().all()
    return [dict(r) for r in rows]
