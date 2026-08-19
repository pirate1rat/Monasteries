import styles from './WinnerPopup.module.css'

export function WinnerPopup({ winner, onClose }) {
    return (
        <div className={styles.overlay} onClick={onClose}>
            <div className={styles.popup} onClick={e => e.stopPropagation()}>
                <div className={styles.popupGlow} />
                <p className={styles.popupEyebrow}>Game over</p>
                <h2 className={styles.popupTitle}>{winner} wins</h2>
                <button className={styles.popupClose} onClick={onClose}>Continue</button>
            </div>
        </div>
    )
}
