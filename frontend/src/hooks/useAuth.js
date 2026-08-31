import { useState, useEffect } from 'react'
import api from '../services/api'
import { getSocket } from '../services/socket'

class Player {
    constructor({ player_id = null, username = null, anonymous = false } = {}) {
        this.playerId = player_id
        this.username = username
        this.anonymous = anonymous
    }
}

let _player = null
const _listeners = new Set()

function setPlayer(p) {
    _player = p
    _listeners.forEach(fn => fn(p))
}

api.get('auth/me').then(res => {
    console.log('auth/me response:', res.data)
    console.log('listeners count:', _listeners.size)
    setPlayer(new Player(res.data))
    console.log('player after set:', _player)
})

export function useAuth() {
    const [player, setLocalPlayer] = useState(() => _player)

    useEffect(() => {
        _listeners.add(setLocalPlayer)
        if (_player !== player) {
            setLocalPlayer(_player)
        }
        return () => _listeners.delete(setLocalPlayer)
    }, [])

    async function login(email, password) {
        const res = await api.post('/auth/login', {email, password})
        if(res.data.status === 'ok') {
            const me = await api.get('/auth/me')
            setPlayer(new Player(me.data))  
        }
        return res
    }

    async function logout() {
        await api.post('auth/logout')
        const res = await api.post('/auth/anonymous')
        setPlayer(new Player({
            player_id: res.data.player_id,
            anonymous: true,
        }))
    }

    async function register(username, email, password) {
        const res = await api.post('/auth/register', { username, email, password })
        return res
    }

    return { player, login, logout, register }
}