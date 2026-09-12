import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage    from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import LobbyPage    from './pages/LobbyPage'
import TutorialPage from './pages/TutorialPage'
import { useAuth }  from './hooks/useAuth'
import GamePage from './pages/GamePage'

export default function App() {
    const { player } = useAuth()

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LobbyPage/>} />
                <Route path="/login" element={<LoginPage/>} />
                <Route path="/register" element={<RegisterPage/>} />
                <Route path="/rules" element={<TutorialPage/>} />
                <Route path="/game/:gameId" element={<GamePage/>} />
                <Route path="/test" element={<GamePage/>} />
            </Routes>
        </BrowserRouter>
    )
}