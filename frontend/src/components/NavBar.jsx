import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import logo from '../assets/cathedral-logo.png'
import styles from './NavBar.module.css'

export function NavBar() {
    const { player, logout } = useAuth()
    const isGuest = player?.anonymous

    return (
        <nav className={styles.nav}>
            <Link to="/">
                <img src={logo} alt="Logo" className={styles.logo} />
            </Link>

            <div className={styles.menu}>
                <Link to="/">
                    <button className={styles.menuBtn}>Play</button>
                </Link>
                <Link to="/rules">
                    <button className={styles.menuBtn}>Tutorials</button>
                </Link>
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
                )}
            </div>
        </nav>
    )
}