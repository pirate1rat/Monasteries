import { useState, useEffect } from 'react'
import api from '../services/api'

class Player {
    constructor({ player_id = null, username = null, email = null, anonymous = false } = {}) {
        this.player_id = player_id
        this.username = username
        this.email = email
        this.anonymous = anonymous
    }
}

let _player = null
const _listeners = new Set()

function setPlayer(p) {
    _player = p
    _listeners.forEach(fn => fn(p))
}

async function loginAnonymous() {
    const res = await api.post('auth/anonymous')
    if(res.data.status === 'ok') {
        setPlayer(new Player({anonymous: true, player_id: res.data.player_id}))
    }
    return res
}

export function useAuth() {
    const [player, setLocalPlayer] = useState(_player)

    useEffect(() => {
        _listeners.add(setLocalPlayer)

        if (!_player) {
            loginAnonymous()
        }

        return () => _listeners.delete(setLocalPlayer)
    },  [])

    async function login(email, password) {
        const res = await api.post('/auth/login', {email, password})
        if(res.data.status === 'ok') {
            setPlayer(new Player({username: res.data.username, email, anonymous: false}))
        }
        return res
    }

    async function logout() {
        await api.post('auth/logout')
        await loginAnonymous()
    }

    async function register(username, email, password) {
        const res = await api.post('/auth/register', {username, email, password})
        if(res.data.status === 'ok') {
            setPlayer(new Player({username, email, anonymous: false}))
        }
        return res
    }

    return { player, login, logout, register }
}