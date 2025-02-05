import requests
import time
import sqlite3
import json

class ChatRoom:
    def __init__(self, db_name='chatroom.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.create_views()
        self.next_time = 0

    def create_tables(self):
        # 创建表结构，如果表不存在则创建
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatroom_all (
            msgIdClient varchar(255) NOT NULL,
            msg_time DATETIME NOT NULL,
            msgIdServer varchar(255),
            msgType varchar(255),
            bodys varchar(500),
            extInfo varchar(500),
            userId varchar(255),
            nickName varchar(255),
            UNIQUE (msgIdClient),
            PRIMARY KEY(msgIdClient)
        )''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatroom_gift
        (
        msgIdClient varchar(255) NOT NULL,
        giftId varchar(100)  NOT NULL,
        giftName varchar(50) NOT NULL,
        giftNum int  NOT NULL,
        money int,
        UNIQUE (msgIdClient),
        PRIMARY KEY(msgIdClient)
        )''')
        self.conn.commit()

    def create_views(self):
        # 创建视图
        self.cursor.execute('''
        CREATE VIEW IF NOT EXISTS gift_room_view AS
        SELECT pcg.*, pca.msg_time, pca.userId, pca.nickName
        FROM chatroom_gift pcg
        LEFT JOIN chatroom_all pca ON pcg.msgIdClient = pca.msgIdClient
        where pcg.giftName like '%name%'
        ''')
        self.conn.commit()


    def save_chatroom_data(self, res_json):
        resp_content = res_json['content']
        self.next_time = resp_content['nextTime']
        msgs = resp_content['message']
        # 保存聊天记录数据
        for message in msgs:
            msg_time = convert_timestamp_to_timestr(message["msgTime"], with_k=True, timezone_offset=tz_offset)
            msgType = message['msgType']
            bodys = message['bodys']
            extInfo = message['extInfo']
            extRaw = json.loads(extInfo)
            msgIdClient = message['msgIdClient']
            msgIdServer = message['msgIdServer']
            userId = extRaw['user']['userId']
            nickName = extRaw['user']['nickName']
            sql = f'''
            INSERT OR IGNORE INTO chatroom_all (msgIdClient, msg_time, msgIdServer, msgType, bodys, extInfo, userId, nickName)
            VALUES ('{msgIdClient}', '{msg_time}', 
            '{msgIdServer}', '{msgType}', '{bodys}', 
            '{extInfo}', '{userId}', '{nickName}')
            '''
            basic_sql_exe(self.conn, self.cursor, sql)
            if msgType in ['GIFT_TEXT']:
                body_json = json.loads(bodys)
                self.save_gift_info(body_json,msgIdClient,self.conn)

    def save_gift_info(self, msg,msgId, connect):
        gift_info = msg['giftInfo']
        giftId = gift_info['giftId']
        giftName = gift_info['giftName']
        giftNum = gift_info['giftNum']

        sql = "INSERT INTO chatroom_gift (msgIdClient,giftId, giftName, giftNum) \
                                VALUES ('%s','%s','%s',  %s)" % (
            msgId, giftId, giftName, giftNum)
        basic_sql_exe(self.conn, self.cursor, sql)

    def run(self, _id, serverid, limit_num=200, start_time=None):
        next_time = 0
        start_timestamp = convert_time_str_to_timestamp(start_time)  # 将start_time转换为时间戳
        while True:
            res_json = self.post_request(_id, serverid, next_time, limit_num)
            next_time = res_json['content'].get('nextTime', 0)
            print(convert_timestamp_to_timestr(next_time, with_k=True, timezone_offset=tz_offset))
            self.save_chatroom_data(res_json)

            # 检查获取的消息时间戳是否达到start_time
            if res_json['content'] and res_json['content']['message'][-1]['msgTime'] < start_timestamp:
                break

    def post_request(self, _id, serverid, nextTime, limit_num):
        url = ''  # 替换为实际URL
        token_headers = {
            "Connection": "keep-alive",
        }
        params = {
            "nextTime": nextTime,
            "serverId": serverid,
            "channelId": _id,
            "limit": limit_num
        }
        try:
            response = requests.post(url, headers=token_headers, json=params)
        except requests.exceptions.JSONDecodeError as e:
            print(e)
        return response.json()

def basic_sql_exe(conn, cursor, sql):
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print('Error:', e)
        conn.rollback()

def convert_timestamp_to_timestr(timestamp, with_k=True, timezone_offset=0):
    """
    将时间戳转换为字符串，并考虑时区偏移
    :param timestamp: 时间戳（毫秒）
    :param with_k: 是否将时间戳除以1000
    :param timezone_offset: 时区偏移（小时）
    :return: 格式化的时间字符串
    """
    if with_k:
        timestamp /= 1000  # 转换为秒
    # 计算时区偏移（秒）
    offset_seconds = timezone_offset * 3600
    timestamp += offset_seconds  # 调整时间戳
    timeArray = time.localtime(timestamp)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return time_str

def convert_time_str_to_timestamp(time_str):
    """将标准时间字符串转换为时间戳"""
    timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray) * 1000)

if __name__ == "__main__":
    tz_offset = 0  # 服务器部署时 会有时区问题
    start_time = "2025-01-01 00:00:00"  # 替换为实际的起始时间
    chat_room = ChatRoom()
    while True:
        chat_room.run(_id=111, serverid=11, start_time=start_time)         
        print(time.ctime())
        time.sleep(30)
    # 定时刷新数据