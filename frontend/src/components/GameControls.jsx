import { useNavigate } from 'react-router-dom'
import styles from './GameControls.module.css'

export function GameControls({
    gameOver, 
    drawOffered, 
    onProposeDraw, 
    onAcceptDraw, 
    onRejectDraw, 
    onResign, 
    rematchOffered, 
    onProposeRematch, 
    onAcceptRematch,
    onRejectRematch,
    onNewGame,
    onAnalyze, 
    onBackToLobby 
}) {
    if (gameOver) {
        return (
            <div className={styles.actionButtons}>
                <div className={styles.buttonRow}>
                    {rematchOffered
                    ? <>
                        <p>Opponent offers a rematch</p>
                        <button onClick={onAcceptRematch}>Accept Rematch</button>
                    </> 
                    : <>
                        <button
                            onClick={onProposeRematch}
                            disabled={rematchOffered}
                        > {rematchOffered ? 'Rematch offered...' : 'Rematch'}
                        </button>
                    </>
                    }
                    <button className={styles.btnAction} onClick={onNewGame}>New Game</button>
                    <button className={styles.btnAnalyze} onClick={onAnalyze}>Analyze</button>
                </div>
                <button className={styles.btnLobby} onClick={onBackToLobby}>Back to Lobby</button>
            </div>
        )
    }

    if (drawOffered) {
        return (
            <div className={styles.drawOffer}>
                <p className={styles.drawOfferText}>Opponent offers a draw</p>
                <div className={styles.actionButtons}>
                    <button className={styles.btnDraw} onClick={onAcceptDraw}>Accept</button>
                    <button className={styles.btnSurrender} onClick={onRejectDraw}>Decline</button>
                </div>
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
