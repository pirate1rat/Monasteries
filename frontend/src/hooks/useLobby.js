import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom' 
import api from '../services/api'
import { io } from 'socket.io-client'

const socket = io()

export function useLobby() {
    const [lobbies, setLobbies] = useState([])
    const [loading, setLoading] = useState(true)
    const [error,   setError] = useState(null)
    navigate = useNavigate()

    useEffect(() => {
        fetchLobbies()

        socket.on('lobby_created', (newLobby) => {
            setLobbies(prev => {
                if (prev.find(l => l.lobby_id === newLobby.lobby_id)) return prev
                return [...prev, newLobby]
            })
        })

        socket.on('lobby_canceled', (lobbyId) => {
            setLobbies(prev => prev.filter(l => l.lobby_id !== lobbyId))
        })

        socket.on('game_started', (data) => {
            navigate(`/game/${data.game_id}`)
        })

        return () => {
            socket.off('lobby_created')
            socket.off('lobby_cancelled')
            socket.off('game_started')
        }
    }, [])

    async function fetchLobbies() {
        setLoading(true)
        try{
            const res = await api.get('/lobbies/')
            setLobbies(res.data.lobbies)
        } catch (e) {
            setError('Unable to find lobbies')
        } finally {
            setLoading(false)
        }
    }

    async function createLobby(color, timeControl) {
        try {
            const res = await api.post('/lobbies/', {color, timeControl})
            return res.data.lobby
            socket.emit('watch_lobby', { lobby_id: newLobby.lobby_id })
        } catch (e) {
            setError('Unable to create lobby')
            return null
        }
    }

    async function joinLobby(lobbyId) {
        socket.emit('join_lobby', { lobby_id: lobbyId })
    }

    return { lobbies, loading, error, createLobby, joinLobby, fetchLobbies }
}