from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests

post_url = ''
host_url = ''
origin_url = ''
cookie_value = ''

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/frontend"), name="static")


@app.post("/bids")
async def get_bids(id: int = Form(...), numPerPage: int = Form(300), pageNum: int = Form(...), r: float = Form(0.37446488796774813)):
# async def get_bids(id: int = Form(...), numPerPage: int = Form(300), pageNum: int = Form(...), r: float = Form(0.37446488796774813)):
    try:
        print(f"Received: id={id}, num_per_page={numPerPage}, page_num={pageNum}, r={r}")
        response = requests.post(post_url, data={
            'id': id,
            'numPerPage': numPerPage,
            'pageNum': pageNum,
            'r': 0.37446488796774813
        },headers={
            'Host': host_url,
            'sec-ch-ua-platform': "macOS",
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua':'"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Fetch-Mode': 'cors',
            'Origin': origin_url,
            'Referer': f'{origin_url}/pai/item/{id}',
            'Cookie': cookie_value,
           
        })
        response.raise_for_status()  # 检查请求是否成功
        # print(f"External API response: {response.text}")
        data = response.json()
        
        # 检查返回的数据格式是否符合预期
        if "list" in data and "pageNum" in data and "PageCount" in data:
            return data
        else:
            raise HTTPException(status_code=400, detail="Invalid response format")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))  # 返回请求错误信息
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from external API")  # 处理 JSON 解析错误

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("src/frontend/index.html") as f:
        return f.read()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
