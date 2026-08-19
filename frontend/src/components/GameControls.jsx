import styles from './GameControls.module.css'

export function GameControls({ gameOver, onProposeDraw, onResign, onRematch, onNewGame, onAnalyze }) {
    if (gameOver) {
        return (
            <div className={styles.actionButtons}>
                <button className={styles.btnAction} onClick={onRematch}>Rematch</button>
                <button className={styles.btnAction} onClick={onNewGame}>New Game</button>
                <button className={styles.btnAnalyze} onClick={onAnalyze}>Analyze</button>
            </div>
        )
    }

    return (
        <div className={styles.actionButtons}>
            <button className={styles.btnDraw} onClick={onProposeDraw}>Offer Draw</button>
            <button className={styles.btnSurrender} onClick={onResign}>Surrender</button>
        </div>
    )
}
