import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import styles from './LoginPage.module.css'

export default function RegisterPage() {
    const { register, loginAnonymous } = useAuth()
    const navigate = useNavigate()
    
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState(null)

    async function handleRegister() {
        try {
            await register(username, email, password)
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
            <h1>Sign up</h1>
            <div className={styles.form}>
                <input type='username' placeholder='Username' value={username} onChange={e => setUsername(e.target.value)}/>
                <input type='email' placeholder='Email' value={email} onChange={e => setEmail(e.target.value)}/>
                <input type='password' placeholder='Password' value={password} onChange={e => setPassword(e.target.value)}/>
                {error && <p className={styles.error}>{error}</p>}
                <button onClick={handleRegister}>Sign up</button>
                <button onClick={handleAnonymous}>Play as a guest</button>
                <Link to="/login">Sign in</Link>
            </div>
        </div>
    )
}