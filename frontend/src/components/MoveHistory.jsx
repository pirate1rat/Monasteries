import { useEffect, useRef } from 'react'
import styles from './MoveHistory.module.css'

export function MoveHistory({ entries, playerColor }) {
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [entries.length])

    return (
        <section className={styles.historyPanel}>
            <h3 className={styles.panelTitle}>Move history</h3>
            <div className={styles.historyList}>
                {entries.map((h) => {
                    const isMe = h.player === playerColor
                    return (
                        <div
                            key={h.move}
                            className={`${styles.historyEntry} ${isMe ? styles.historyYou : styles.historyOpponent}`}
                        >
                            <span className={styles.historyIndex}>{h.move}.</span>
                            <span className={styles.historyPlayer}>{isMe ? 'You' : 'Opp'}</span>
                            <span className={styles.historyAction}>{h.action}</span>
                        </div>
                    )
                })}
                <div ref={bottomRef} />
            </div>
        </section>
    )
}
