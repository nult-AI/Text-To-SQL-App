from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import inspect
from .database import ENGINE, run_query
from .openai_utils import text_to_sql

app = FastAPI(title="Text-to-SQL Demo")

class NLRequest(BaseModel):
    question: str

@app.on_event("startup")
def capture_schema() -> None:
    insp = inspect(ENGINE)
    global SCHEMA_STR
    SCHEMA_STR = "\n".join(
        f"CREATE TABLE {t} ({', '.join(c['name'] for c in insp.get_columns(t))});"
        for t in insp.get_table_names()
    )

@app.post("/query")
def query(req: NLRequest):
    try:
        sql = text_to_sql(req.question, SCHEMA_STR)
        if not sql.lstrip().lower().startswith("select"):
            raise ValueError("Only SELECT statements are allowed")
        return {"sql": sql, "result": run_query(sql)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
