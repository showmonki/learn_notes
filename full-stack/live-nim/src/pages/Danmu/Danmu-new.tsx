import React from 'react';

interface DanmuProps {
    accid: string;
    pwd: string;
    roomId: number;
    appDataDir: string;
}

const Danmu: React.FC<DanmuProps> = ({ accid, pwd, roomId, appDataDir }) => {
    console.log('Danmu props:', { accid, pwd, roomId, appDataDir }); // 添加调试信息

    return (
        <div>
            <h2>弹幕组件</h2>
            <p>Accid: {accid}</p>
            <p>房间ID: {roomId}</p>
            <p>App Data Dir: {appDataDir}</p>
        </div>
    );
};

export default Danmu;