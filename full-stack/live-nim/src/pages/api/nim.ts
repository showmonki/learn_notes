import type { NextApiRequest, NextApiResponse } from 'next';
import * as NIM from 'node-nim';

const appkey = 'NjMyZmVmZjFmNGM4Mzg1NDFhYjc1MTk1ZDFjZWIzZmE=';
const accid = '20220710203046_tm3o5zbf8qc1eiv';
const token = '834bdkfzzg';
const roomid= '3868298';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        const { action } = req.body;

        switch (action) {
            case 'initIM':
                NIM.nim.client.init(appkey, accid, token, {});
                return res.status(200).json({ message: 'IM 初始化成功' });
            case 'cleanupIM':
                NIM.nim.client.cleanup('');
                return res.status(200).json({ message: 'IM 清理成功' });
            case 'initChatroom':
                NIM.chatroom.init(roomid, accid);
                return res.status(200).json({ message: 'chatroom 初始化成功' });
            case 'cleanupChatroom':
                NIM.chatroom.cleanup('');
                return res.status(200).json({ message: 'chatroom 清理成功' });
            case 'initQChat':
                NIM.qchat.instance.init({ appkey: appkey, app_data_path: 'qchat' });
                return res.status(200).json({ message: '圈组 初始化成功' });
            case 'cleanupQChat':
                NIM.qchat.instance.cleanup({});
                console.log('圈组清理成功');
                return res.status(200).json({ message: '圈组 清理成功' });
            default:
                return res.status(400).json({ message: '无效的操作' });
                
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}