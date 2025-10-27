from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from sqlalchemy import inspect
from app.database import ENGINE, run_query
from app.genai_utils import text_to_sql

#app = FastAPI(title="Text-to-SQL Demo")

class NLRequest(BaseModel):
    question: str

# 1. Định nghĩa Lifespan Handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # --- PHẦN STARTUP (Tương đương với @app.on_event("startup")) ---
    print("Application starting up: Capturing Database Schema...")
    
    # Logic của hàm capture_schema() cũ
    global SCHEMA_STR
    insp = inspect(ENGINE)
    SCHEMA_STR = "\n".join(
        f"CREATE TABLE {t} ({', '.join(c['name'] for c in insp.get_columns(t))});"
        for t in insp.get_table_names()
    )
    
    # In ra schema để kiểm tra (tùy chọn)
    print("Schema captured successfully.")
    # print(SCHEMA_STR) 
    
    yield  # Ứng dụng sẵn sàng nhận request từ đây

    # --- PHẦN SHUTDOWN (Dọn dẹp nếu có) ---
    print("Application shutting down...")
    # Thêm code đóng kết nối DB, giải phóng tài nguyên tại đây nếu cần thiết
 
 # 2. Khởi tạo FastAPI và Gán Lifespan
# Gán hàm lifespan đã định nghĩa ở trên cho tham số lifespan
app = FastAPI(lifespan=lifespan)
   
@app.post("/query")
def query(req: NLRequest):
    try:
        sql = text_to_sql(req.question, SCHEMA_STR)
        if not sql.lstrip().lower().startswith("select"):
            raise ValueError("Only SELECT statements are allowed")
        return {"sql": sql, "result": run_query(sql)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
