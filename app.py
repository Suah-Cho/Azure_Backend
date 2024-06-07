from fastapi import FastAPI #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from fastapi.responses import JSONResponse #type: ignore
from datetime import datetime
from decimal import Decimal
from psycopg2.extras import RealDictCursor
import loc_database
import database

app = FastAPI()

# 허용할 origins 설정
origins = [
    "http://localhost:3000" # React 앱이 실행되는 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 origins 목록
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_data(data):
    """ 데이터에서 datetime 및 Decimal 객체를 문자열 또는 float로 변환 """
    if isinstance(data, list):
        for item in data:
            for key, value in item.items():
                if isinstance(value, datetime):
                    item[key] = value.isoformat()
                elif isinstance(value, Decimal):
                    item[key] = float(value)  # 또는 str(value)로 변환
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, Decimal):
                data[key] = float(value)  # 또는 str(value)로 변환
    return data

@app.get("/")
def main():

    try:
        con = loc_database.getCon()

        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("select * from gh_data_item limit 100;")
        data = cur.fetchall()
        data = serialize_data(data)
    except Exception as e: 
        print(f"Error connecting to database: {e}")
        return JSONResponse(status_code=500, content={"message": "Error connecting to database"})
    finally:
        if cur:
            cur.close()
        if con:
            con.close()    

    return JSONResponse(status_code=200, content={"data": data})