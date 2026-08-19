import styles from './GameTimer.module.css'

export function GameTimer({ time, label, active }) {
    return (
        <div className={`${styles.timer} ${active ? styles.timerActive : ''}`}>
            <span className={styles.timerLabel}>{label}</span>
            <span className={styles.timerValue}>{time ?? '--:--'}</span>
        </div>
    )
}
