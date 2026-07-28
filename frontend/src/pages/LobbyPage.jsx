import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import styles from './LobbyPage.module.css'
import logo from '../assets/cathedral-logo.png'

const DUMMY_LOBBIES = [
    { id: 'abc', host: 'gracz123', color: 'Losowy',   time: '5 min' },
    { id: 'def', host: 'anna_k',   color: 'Biały',    time: '15 min + 10 s' },
    { id: 'ghi', host: 'tomek99',  color: 'Czerwony', time: '3 min' },
]

export default function LobbyPage() {
    const { player, logout } = useAuth()
    const navigate = useNavigate()
    const isGuest = player?.anonymous

    return (
        <div className={styles.page}>
            <nav className={styles.nav}>
                <img src={logo} alt="Logo" className={styles.logo} />
                <div className={styles.menu}>
                    <button className={styles.menuBtn}>Tutorials</button>
                    <button className={styles.menuBtn}>Tools</button>
                    <button className={styles.menuBtn}>User</button>
                </div>

                <div className={styles.navRight}>
                    {isGuest ? (
                        <>
                            <span className={styles.guestBadge}>Guest</span>
                            <Link to="/login">
                                <button className={styles.btnOutline}>Sign in</button>
                            </Link>
                            <Link to="/register">
                                <button className={styles.btnPrimary}>Sign up</button>
                            </Link>
                        </>
                    ) : (
                        <>
                            <span className={styles.username}>{player?.username ?? 'Player'}</span>
                            <button className={styles.btnOutline} onClick={logout}>Logout</button>
                        </>
                    ) }
                </div>
            </nav>

            <main className={styles.main}>
                <div className={styles.tableWrapper}>
                    <div className={styles.topBar}>
                        <h2 className={styles.title}>Lobbies</h2>
                        <button className={styles.btnNew} onClick={() => navigate('/game/new')}>Create lobby</button>
                    </div>

                    <table className={styles.table}>
                        <thead>
                            <tr>
                                <th>Player</th>
                                <th>Color</th>
                                <th>Tempo</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr className={styles.myRow}>
                                <td>You ({isGuest ? "Guest" : player?.username})</td>
                                <td>Red</td>
                                <td>10min + 5s</td>
                                <td><span className={styles.pillWait}>Waiting for opponent</span></td>
                                <td></td>
                            </tr>

                            {DUMMY_LOBBIES.map(l => (
                                <tr key={l.id} className={styles.row}>
                                    <td>{l.host}</td>
                                    <td>{l.color}</td>
                                    <td>{l.time}</td>
                                    <td><span className={styles.pillOpen}>Open</span></td>
                                    <td><button className={styles.joinBtn}>Join</button></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    )
}