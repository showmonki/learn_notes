import { useRef, useEffect } from 'react';
import NodeNimChatroomSocket from '../pages/chatroom/sdk/NodeNimChatroomSocket'; // 更新路径
import getConfig from '../utils/config';

function Danmu() {
    const nimRef = useRef<NodeNimChatroomSocket | null>(null);
    const { accid, pwd, roomId, appDataDir } = getConfig(); // 从配置中获取值

    function handleNewMessage(messages: Array<ChatRoomMessage>) {
        // 处理新消息
        console.log('新消息:', messages);
    }

    async function danmuOpen(): Promise<void> {
        if (!nimRef.current) {
            try {
                console.log('正在初始化 NodeNimChatroomSocket...');
                nimRef.current = new NodeNimChatroomSocket(
                    accid,
                    pwd,
                    roomId,
                    appDataDir,
                    handleNewMessage
                );

                const apiUrl = `${window.location.origin}/api/nimLogin`; // 构建 API URL
                console.log('NodeNimChatroomSocket 初始化成功，正在调用 init()...');
                await nimRef.current.init(apiUrl); // 传递 API URL
                console.log('init() 调用成功');

                // 等待 WebSocket 连接成功
                nimRef.current.websocket.onopen = async () => {
                    console.log('WebSocket 连接成功，正在获取历史消息...');
                    await getHistoryMessages();
                };
            } catch (error) {
                console.error('danmuOpen 函数出错:', error);
            }
        }
    }

    const getHistoryMessages = async () => {
        if (nimRef.current && nimRef.current.websocket.readyState === WebSocket.OPEN) {
            const timeTag = 0; // 设置时间标签，0表示获取所有历史消息
            nimRef.current.websocket.send(JSON.stringify({
                action: 'getHistoryMessage',
                roomId,
                timeTag,
            }));
        } else {
            console.warn('WebSocket 尚未打开，无法获取历史消息');
        }
    };

    useEffect(() => {
        // 组件卸载时关闭连接
        return () => {
            nimRef.current?.close();
        };
    }, []);

    return (
        <div>
            <button onClick={danmuOpen}>打开弹幕</button>
        </div>
    );
}

export default Danmu;