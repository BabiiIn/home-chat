import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Chat from './pages/Chat.jsx'
import Rooms from './pages/Rooms.jsx'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/rooms" element={<Rooms />} />
    </Routes>
  )
}

export default App

