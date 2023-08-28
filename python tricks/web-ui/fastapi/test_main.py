import json

import pytest
from fastapi.testclient import TestClient
from fastapi_demo import app  # 导入你的 FastAPI 应用

# 创建一个测试客户端
client = TestClient(app)

def test_process_dataframe():
    # 准备测试数据，这里的数据应该是符合接口预期的 JSON 数据
    test_data = {
        "data": [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "San Francisco"},
            {"name": "Charlie", "age": 28, "city": "Los Angeles"}
        ]
    }

    # 发送 POST 请求进行测试
    response = client.post("/process_dataframe/", json=test_data)

    # 检查响应状态码是否为 200 OK
    assert response.status_code == 200

    # 解析响应内容为 JSON
    result = response.json()

    # 在这里可以编写更多的断言来检查接口的输出是否符合预期
    assert "dataframe_shape" in result
    assert result["dataframe_shape"] == [3, 3]  # 这里的示例断言可以根据你的实际情况修改



if __name__ == '__main__':
    pytest.main()
