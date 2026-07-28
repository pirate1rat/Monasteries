import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage    from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import LobbyPage    from './pages/LobbyPage'
// import GamePage     from './pages/GamePage'
// import TutorialPage from './pages/TutorialPage'
import { useAuth }  from './hooks/useAuth'

export default function App() {
    const { player } = useAuth()

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginPage/>} />
                <Route path="/register" element={<RegisterPage/>} />
                {/* <Route path="/rules" element={<TutorialPage/>} /> */}
                {/* <Route path="/" element={player ? <LobbyPage/> : <Navigate to="/login" />} /> */}
                <Route path="/" element={<LobbyPage/>} />
                {/* <Route path="/game/gameId" element={player ? <GamePage/> : <Navigate to="/login" />} /> */}
            </Routes>
        </BrowserRouter>
    )
}