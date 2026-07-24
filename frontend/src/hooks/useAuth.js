import { useState, useEffect } from 'react'
import api from '../services/api'

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
        return () => _listeners.delete(setLocalPlayer)
    },  [])

    async function login(email, password) {
        const res = await api.post('/auth/login', {email, password})
        if(res.data.status === 'ok') {
            setPlayer({email})
        }
        return res
    }

    async function logout() {
        await api.post('auth/logout')
        setPlayer(null)
    }

    async function loginAnonymous() {
        const res = await api.post('auth/anonymous')
        if(res.data.status === 'ok') {
            setPlayer({anonymous: true, player_id: res.data.player_id})
        }
        return res
    }

    return { player, login, logout, loginAnonymous }
}