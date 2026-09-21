import { useLocation, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import styles from './LobbyPage.module.css'
import logo from '../assets/cathedral-logo.png'
import { useState } from 'react'
import CreateGameModal from '../components/CreateGameModal'
import { useLobby } from '../hooks/useLobby'
import { NavBar } from '../components/NavBar'

export default function LobbyPage() {
    const location = useLocation()
    const [showModal, setShowModal] = useState(
        location.state?.openCreateModal ?? false
    )
    const { player, logout } = useAuth()
    const { lobbies, loading, error, joinLobby, createLobby, cancelLobby } = useLobby()
    const isGuest = player?.anonymous

    if (!player) {
        return <div className={styles.page}>Loading...</div>
    }
    console.log(player, isGuest, player.playerId)

    return (
        <>
            <NavBar/>
            <div className={styles.page}>
                <main className={styles.main}>
                    <div className={styles.tableWrapper}>
                        <div className={styles.topBar}>
                            <h2 className={styles.title}>Lobbies</h2>
                            <button className={styles.btnNew} onClick={() => setShowModal(true)}>Create lobby</button>
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
                                {lobbies.filter(Boolean).map(l => (
                                    <tr key={l.lobby_id} className={l.host_id === player?.playerId ? styles.myRow : styles.row}>
                                        <td>{l.host_id === player.playerId ? `You (${player?.username ?? 'Guest'})` : l.host_name}</td>
                                        <td>{l.host_color === 'neutral' ? 'random' : l.host_color}</td>
                                        <td>
                                        {l.time_control.base / 60} min
                                        {l.time_control.increment > 0 ? ` + ${l.time_control.increment}s` : ''}
                                        </td>
                                        <td><span className={styles.pillOpen}>Open</span></td>
                                        <td>
                                            {l.host_id === player?.playerId ?
                                            <button className={styles.cancelBtn}
                                                    onClick={() => cancelLobby(l.lobby_id)}>
                                                Cancel
                                            </button>
                                            : <button className={styles.joinBtn}
                                                    onClick={() => joinLobby(l.lobby_id)}>
                                                Join
                                            </button>
                                        }
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </main>

                {showModal && (
                    <CreateGameModal onClose={() => setShowModal(false)}
                    onCreate={createLobby} />
                )}
            </div>
        </>
    )
}