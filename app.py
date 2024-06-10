from fastapi import FastAPI #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from fastapi.responses import JSONResponse #type: ignore
from datetime import datetime
from decimal import Decimal
from psycopg2.extras import RealDictCursor
# import loc_database
import database
import logging
# import uvicorn

app = FastAPI()

# 허용할 origins 설정
# origins = [
#     "http://localhost",
#     "http://localhost:80",
#     "http://localhost:3000", # React 앱이 실행되는 도메인
#     "http://client",
#     "http://client:80",
#     "http://client:3000",
#     "http://40.82.144.200/",
#     "http://40.82.144.200:80",
#     "http://40.82.144.200:3000"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 origins 목록
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
    con = database.get_db_connetion()
    # con = loc_database.getCon()
    if con is None:
        # print("Error connecting to database")
        logging.error("Error connecting to database")

    try:
        # con = database.getCon()

        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("select * from gh_data_item limit 100;")
        data = cur.fetchall()
        data = serialize_data(data)
        cur.close()

        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e: 
        # print(f"Error connecting to database: {e}")
        logging.error(f"Error connecting to database: {e}")
        return JSONResponse(status_code=500, content={"message": "Error connecting to database"})
    finally:
        if con:
            con.close()    

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)