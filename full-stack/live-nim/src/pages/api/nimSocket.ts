import { NextApiRequest, NextApiResponse } from 'next';
import appKey from '../chatroom/sdk/appKey';

const WebSocket = require('ws');
import * as NodeNim from 'node-nim';

let chatroom: NodeNim.ChatRoom | null = null;
let chatroomRequestLoginResult: string | null = null;

export default (req: NextApiRequest, res: NextApiResponse) => {
    const { appKey, account, token, roomId, appDataDir } = req.body;
    console.log('检查nimSocket body：',appKey, account, token, roomId, appDataDir)
    console.log(res)
    if (!res.socket.server.wss) {
        const wss = new WebSocket.Server({ noServer: true });

        res.socket.server.wss = wss;

        wss.on('connection', (ws) => {
            console.log('客户端连接成功');

            ws.on('message', async (message: string) => {
                const data = JSON.parse(message);

                if (data.action === 'login') {
                    const { account, token, roomId, appDataDir } = data;
                    try {
                        // 调用 nimLogin API 进行登录
                        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/nimLogin`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                appKey,
                                account,
                                token,
                                roomId,
                                appDataDir,
                            }),
                        });

                        const loginResult = await response.json();

                        if (!loginResult.success) {
                            return ws.send(JSON.stringify({ action: 'loginError', error: loginResult.error }));
                        }

                        chatroomRequestLoginResult = loginResult.roomEnterResult;
                        ws.send(JSON.stringify({ action: 'loginSuccess', result: chatroomRequestLoginResult }));

                        // 初始化聊天室
                        chatroom = new NodeNim.ChatRoom();
                        chatroom.init('', '');
                        chatroom.initEventHandlers();

                        chatroom.on('enter', (rid, status, status2, roomInfo, myInfo) => {
                            if (status === 5 && status2 === 200) {
                                ws.send(JSON.stringify({ action: 'chatroomConnected', roomInfo }));
                            }
                        });

                        chatroom.enter(roomId, chatroomRequestLoginResult, {}, '');
                    } catch (error) {
                        ws.send(JSON.stringify({ action: 'loginError', error }));
                    }
                }

                ws.on('close', () => {
                    console.log('客户端断开连接');
                    if (chatroom) {
                        chatroom.exit(data.roomId, '');
                        chatroom.cleanup('');
                    }
                });
            });

            res.socket.server.on('upgrade', (request, socket, head) => {
                wss.handleUpgrade(request, socket, head, (ws) => {
                    wss.emit('connection', ws, request);
                });
            });
        });
    } else {
        console.log('WebSocket 服务器已初始化，跳过初始化'); // 添加调试信息
    }

    res.end();
}