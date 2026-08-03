import { useState, useEffect } from 'react'
import api from '../services/api'

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

export function useAuth() {
    const [player, setLocalPlayer] = useState(_player)

    useEffect(() => {
        _listeners.add(setLocalPlayer)

        if (_player === null) {
            api.get('auth/me')
            .then(res => setPlayer(new Player(res.data)))
            .catch(() => {
                api.post('/auth/anonymous')
                    .then(res => setPlayer(new Player({
                            player_id: res.data.player_id,
                            username:  null,
                            anonymous: true,
                    })))
            })
        }

        return () => _listeners.delete(setLocalPlayer)
    },  [])

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