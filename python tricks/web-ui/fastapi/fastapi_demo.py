from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import uvicorn
from io import StringIO

app = FastAPI()


# 创建一个 Pydantic 模型，用于接收 JSON 数据
class DataFrameInput(BaseModel):
	data: list  # JSON 数据作为字符串传输

class JsonData(BaseModel):
	data: list

@app.post("/process_dataframe/")
async def process_dataframe(input_data: DataFrameInput):
	try:
		data = input_data.data
		df = pd.DataFrame(data)
		return {"dataframe_shape": df.shape}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.post("/process_json/")
async def process_json(input_data: JsonData):
	try:
		data = input_data.data
		return {"json": data}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


if __name__ == '__main__':
	uvicorn.run('fastapi_demo:app', reload=True, port=8000)
