import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import optimzer from 'vite-plugin-optimizer';


export default defineConfig({
  base: './',
  plugins: [
    react(), 
    optimzer(
        {electron: 'const { ipcRenderer } = require("electron"); export { ipcRenderer }'}
    )],
  server: {
    port: 3000
  },
  // 确保这里指定了正确的入口文件
  build: {
    rollupOptions: {
      input: {
        main: './index.html',
      },
    },
  },
});