import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import yaml from 'js-yaml';
import axios from 'axios';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const configPath = path.join(__dirname, '..', 'config.yaml');

let mainWindow;

ipcMain.handle('get-base-path', () => {
  return basePath;
});

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  mainWindow.loadURL('http://localhost:3000');
  mainWindow.webContents.openDevTools()

    // 添加窗口关闭事件监听器
    mainWindow.on('closed', () => {
      mainWindow = null;
    });
}


app.whenReady().then(() => {
    createWindow();
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
          createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});



ipcMain.handle('load-config', () => {
  try {
    const fileContents = fs.readFileSync(configPath, 'utf8');
    const config = yaml.load(fileContents);
    console.log('加载的配置:', config);
    return config;
  } catch (error) {
    console.error('加载配置时出错:', error);
    return {};
  }
});

ipcMain.on('save-config', (event, newConfig) => {
  try {
    const yamlStr = yaml.dump(newConfig);
    fs.writeFileSync(configPath, yamlStr, 'utf8');
    console.log('保存的配置:', newConfig);
  } catch (error) {
    console.error('保存配置时出错:', error);
  }
});

ipcMain.on('open-danmu-window', (event, { accid, pwd, roomid, appdir }) => {
  if (!mainWindow || mainWindow.isDestroyed()) {
    console.error('主窗口未创建或已销毁，正在重新创建主窗口');
    createWindow();
  }

  const danmuWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });
  
  danmuWindow.loadURL(`http://localhost:3000/danmu`);
  // // 打开弹幕窗的开发者工具
  danmuWindow.webContents.openDevTools()
    
  // 可以通过webContents.send方法将参数传递给新窗口
  danmuWindow.webContents.on('did-finish-load', () => {
    danmuWindow.webContents.send('danmu-params', { accid, pwd, roomid, appdir });
  });
});

ipcMain.handle('get-live-list', async () => {
  try {
    const response = await axios.get('https://api.bilibili.com/x/web-interface/online');
    return response.data;
  } catch (error) {
    console.error('获取直播列表时出错:', error);
    return [];
  }
});