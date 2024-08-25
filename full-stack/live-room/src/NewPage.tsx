import React, { useState , useEffect} from 'react';
import { ipcRenderer } from 'electron';

const NewPage: React.FC = () => {
    const [accid, setAccid] = useState('');
    const [pwd, setPwd] = useState('');
    const [roomid, setRoomid] = useState('');
    const [appdir, setAppdir] = useState('');
    const [liveList, setLiveList] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    
    useEffect(() => {

        // 加载配置
        const loadConfig = async () => {
         try {
                const config = await ipcRenderer.invoke('load-config');
                console.log('加载的配置:', config);
                // 使用加载的配置更新您的状态
    
                setAccid(config.accid || '');
                setPwd(config.pwd || '');
                setRoomid(config.roomid || '');
                setAppdir(config.appdir || '');
            } catch (error) {
                console.error('加载配置时出错:', error);
              }
            };

    
        loadConfig();
      }, []);
    
      const saveConfig = () => {
        const newConfig = { accid, pwd, roomid, appdir };
        ipcRenderer.send('save-config', newConfig);
        console.log('已发送保存配置请求');
      };

      const openDanmuWindow = () => {
        if (accid && pwd && roomid && appdir) {
            saveConfig(); // 保存配置
            ipcRenderer.send('open-danmu-window', { accid, pwd, roomid, appdir });
        } else {
            alert('请填写所有必要的信息。');
        }
    };

    const getLiveList = async() => {
        setIsLoading(true);
        try {
            const RawliveList = await ipcRenderer.invoke('get-live-list');
            console.log('获取到的直播列表raw:', RawliveList);
            console.log('获取到的直播列表:', RawliveList.data.region_count);
            const liveList = RawliveList.data.region_count;
            setLiveList(liveList);
            setIsLoading(false);
        } catch (error) {
            console.error('获取直播列表时出错:', error);
            setIsLoading(false);
        } finally {
            setIsLoading(false);
        }
    }
      
      
  return (
<div>
      {/* 输入框 */}
      <div>accid: 
      <input
        type="text"
        placeholder="输入 accid"
        value={accid}
        onChange={(e) => setAccid(e.target.value)}
      />
      pwd: 
      <input
        type="password"
        placeholder="输入 pwd"
        value={pwd}
        onChange={(e) => setPwd(e.target.value)}
      />
      roomid: 
      <input
        type="text"
        placeholder="输入 roomid"
        value={roomid}
        onChange={(e) => setRoomid(e.target.value)}
      />
      appdir: 
      <input
        type="text"
        placeholder="输入 appdir"
        value={appdir}
        onChange={(e) => setAppdir(e.target.value)}
      />
      </div>
      <button onClick={saveConfig}>保存配置</button>

      {/* 按钮 */}
      <button onClick={openDanmuWindow}>确认并打开弹幕</button>

      <button onClick={getLiveList} disabled={isLoading} >{isLoading ? '加载中...' : '获取当前直播清单'}</button>
      {Object.keys(liveList).length > 0 && (
        <ul>
          {Object.entries(liveList).map(([key, value]) => (
            <li key={key}>{key}: {value}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default NewPage;