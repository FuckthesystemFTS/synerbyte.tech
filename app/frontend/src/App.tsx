import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ChatProvider } from './contexts/ChatContext'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { ChatPage } from './pages/ChatPage'

function App() {
  return (
    <Router>
      <AuthProvider>
        <ChatProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/" element={<Navigate to="/login" replace />} />
          </Routes>
        </ChatProvider>
      </AuthProvider>
    </Router>
  )
}

export default App
