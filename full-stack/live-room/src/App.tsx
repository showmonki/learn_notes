import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NewPage from './NewPage';
import Chat from './chatroom/Chat';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<NewPage />} />
        <Route path="/danmu" element={<Chat />} />
      </Routes>
    </Router>
  );
}

export default App;