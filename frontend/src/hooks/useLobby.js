import { useState, useEffect } from 'react'
import api from '../services/api'

export function useLobby() {
    const [lobbies, setLobbies] = useState([])
    const [loading, setLoading] = useState(true)
    const [error,   setError] = useState(null)

    useEffect(() => {
        fetchLobbies()
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
            setLobbies(prev => [...prev, res.data.lobby])
            return res.data
        } catch (e) {
            setError('Unable to create lobby')
            return null
        }
    }

    return { lobbies, loading, error, createLobby, fetchLobbies }
}