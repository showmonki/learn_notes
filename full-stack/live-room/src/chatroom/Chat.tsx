import React, { useState, useEffect } from 'react';
import { ipcRenderer } from 'electron';

function Chat() {
  useEffect(() => {
    const handleDanmuParams = (event, params) => {
      console.log('接收到弹幕参数:', params);
      // 处理接收到的参数
    };

    ipcRenderer.on('danmu-params', handleDanmuParams);

    return () => {
      ipcRenderer.removeListener('danmu-params', handleDanmuParams);
    };
  }, []);

  return (
    <div>
      <h1>Danmu page</h1>
    </div>
  );
}

export default Chat;
