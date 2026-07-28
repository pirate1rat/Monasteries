import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import styles from './LoginPage.module.css'

export default function LoginPage() {
    const { login, loginAnonymous } = useAuth()
    const navigate = useNavigate()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState(null)

    async function handleLogin() {
        try {
            await login(email, password)
            navigate('/')
        } catch {
            setError('Wrong email or password')
        }
    }

    function handleAnonymous() {
        navigate('/')
    }

    return (
        <div className={styles.container}>
            <h1>Sign in</h1>
            <div className={styles.form}>
                <input type='email' placeholder='Email' value={email} onChange={e => setEmail(e.target.value)}/>
                <input type='password' placeholder='Password' value={password} onChange={e => setPassword(e.target.value)}/>
                {error && <p className={styles.error}>{error}</p>}
                <button onClick={handleLogin}>Sign in</button>
                <button onClick={handleAnonymous}>Play as a guest</button>
                <Link to="/register">Sign up</Link>
            </div>
        </div>
    )
}