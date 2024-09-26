import React, { useState } from 'react';

const NimComponent: React.FC = () => {
    const [account, setAccount] = useState('20220710203046_tm3o5zbf8qc1eiv');
    const [token, setToken] = useState('834bdkfzzg');
    const [roomId, setRoomId] = useState('3868298');

    const handleLogin = async () => {
        const response = await fetch('/api/nimLogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                appKey: 'NjMyZmVmZjFmNGM4Mzg1NDFhYjc1MTk1ZDFjZWIzZmE=', // 替换为实际的 appKey
                account,
                token,
                roomId,
                appDataDir: 'your_app_data_dir', // 替换为实际的 appDataDir
            }),
        });

        const data = await response.json();
        console.log(data.message || data.error);
    };

    return (
        <div>
            <h1>NIM 测试页面</h1>
            <input type="text" placeholder="账号" value={account} onChange={(e) => setAccount(e.target.value)} />
            <input type="text" placeholder="Token" value={token} onChange={(e) => setToken(e.target.value)} />
            <input type="text" placeholder="聊天室 ID" value={roomId} onChange={(e) => setRoomId(e.target.value)} />
            <button onClick={handleLogin}>登录</button>
        </div>
    );
};

export default NimComponent;