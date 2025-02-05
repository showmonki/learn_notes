# ChatRoom 数据抓取项目

## 项目简介
该项目用于循环发送POST请求以获取聊天记录和礼物信息，并将数据存储到SQLite数据库中。

## 功能
- 循环发送POST请求，获取聊天记录和礼物信息。
- 将获取的数据存储到SQLite数据库中。
- 支持根据时间戳判断何时停止请求。

## 数据库结构
- `chatroom_all` 表：存储聊天记录。
- `room_gift` 表：存储礼物信息。

## 使用方法
1. 确保安装了 `requests` 和 `sqlite3` 库。
2. 修改代码中的 `YOUR_TOKEN` 和请求的 URL。
3. 运行 `main.py` 文件，传入相应的 `_id` 和 `serverid`。

## 运行
```
python app.py
```

```
python team_gift.py
```
