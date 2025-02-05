from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from fastapi import Request

app = FastAPI()

# 设置模板目录
templates = Jinja2Templates(directory="templates")

# 静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db_connection():
    conn = sqlite3.connect('chatroom.db')
    conn.row_factory = sqlite3.Row  # 使得返回的行可以通过列名访问
    return conn

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gift_room_view")
    rows = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "rows": rows})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=1111)
        while True:
        chat_room.run(_id=23892101, serverid=17863211, start_time=start_time) 
        
        print(time.ctime())
        time.sleep(30)
    # 实际部署环境下 需要调整为本地host，127.0.0.1 无法访问 