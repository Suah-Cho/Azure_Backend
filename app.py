from fastapi import FastAPI #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from fastapi.responses import JSONResponse #type: ignore
from datetime import datetime
from decimal import Decimal
from psycopg2.extras import RealDictCursor
# import loc_database
import database
import logging
import uvicorn


app = FastAPI()


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
        cur.execute("select * from gh_data_item_5min where (device_id, data_type_id) = ('397573ec-f29d-45c0-ad26-ec9caf28dd53', '4a57a105-b834-4358-9cb5-fde3b43305ae');")
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

@app.get("/test")
def test():
    logging.info("test log")
    return {"message": "Hello, FastAPI!"}

@app.get("/servererror/500")
def servererror():
    logging.error("TEST 500 Internal Server Error")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error0"})

@app.get("/servererror/501")
def servererror():
    logging.error("TEST 501 Internal Server Error")
    return JSONResponse(status_code=501, content={"message": "Internal Server Error1"})

@app.get("/servererror/502")
def servererror():
    logging.error
    return JSONResponse(status_code=502, content={"message": "Internal Server Error2"})

@app.get("/servererror/503")
def servererror():
    return JSONResponse(status_code=501, content={"message": "Internal Server Error"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

