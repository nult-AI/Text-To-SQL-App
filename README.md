# This example run at 10/2025:
Mô hình này sẽ work với gemini của google. chưa thử với openai
Project sẽ work tren poetry

Khi clone project về cần thêm 1 số file:
.env
 - file này sẽ lưu API Key của openai hoac gemini. Vì file này cần bao mât nên khong public

Chạy lênh bên dưới để khơi tạo sqlite database (demo.db). Tất nhiên phải down sqlite3 và tạo biến môi trường để chạy lệnh. Sau lệnh này sẽ tạo demo.db
 - sqlite3 demo.db < init_db.sql 

# Chạy application trên local:
Step 1: Cài các package cho ứng dụng với poetry
- poetry install
Step 2: run ưng dụng
- poetry run uvicorn app.main:app --reload
Step 3: Test với curl
-  curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"question\":\"How many customers?\"}"
- curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"question\":\"What is the number of orders placed by each customer\"}"

# Chạy application trên container:
Step 1: build image
- docker compose build --no-cache  hoặc
- podman compose build --no-cache 
Step 2: run container
- docker compose up -d  hoac
- podman compose up -d 
Step 3: Test vơi curl
- Tương tự với chạy local
