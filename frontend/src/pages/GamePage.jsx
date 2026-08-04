import { useState } from 'react'
import styles from './GamePage.module.css'

function PieceGrid({ cells, color, cellSize }) {
    const minR = Math.min(...cells.map(c => c[0]))
    const minC = Math.min(...cells.map(c => c[1]))
    const maxR = Math.max(...cells.map(c => c[0]))
    const maxC = Math.max(...cells.map(c => c[1]))
    const rows = maxR - minR + 1
    const cols = maxC - minC + 1
    const filled = new Set(cells.map(([r, c]) => `${r - minR},${c - minC}`))

    return (
        <div style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
            gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
            gap: 2,
        }}>
            {Array.from({ length: rows * cols }, (_, i) => {
                const r = Math.floor(i / cols)
                const c = i % cols
                return (
                    <div key={i} style={{
                        width: cellSize,
                        height: cellSize,
                        backgroundColor: filled.has(`${r},${c}`) ? color : 'transparent',
                        borderRadius: 3,
                        boxShadow: filled.has(`${r},${c}`) ? `inset 0 1px 0 rgba(255,255,255,0.15)` : 'none',
                    }} />
                )
            })}
        </div>
    )
}

function PieceSlot({ piece, count, color, compact }) {
    const cellSize = compact ? 7 : 13
    return (
        <div className={`${styles.pieceSlot} ${compact ? styles.pieceSlotCompact : ''}`}>
            <div className={styles.pieceShape}>
                <PieceGrid cells={piece.cells} color={color} cellSize={cellSize} />
            </div>
            <span className={styles.pieceCount} style={{ color }}>×{count}</span>
        </div>
    )
}

const PLAYER_COLOR = '#C8A96E'
const OPPONENT_COLOR = '#6E8DC8'

const PLAYER_PIECES = [
    { id: 'mono',      cells: [[0,0]],                                   count: 2 },
    { id: 'duo',       cells: [[0,0],[0,1]],                             count: 2 },
    { id: 'trio_i',    cells: [[0,0],[0,1],[0,2]],                       count: 1 },
    { id: 'trio_l',    cells: [[0,0],[1,0],[1,1]],                       count: 1 },
    { id: 'quad_sq',   cells: [[0,0],[0,1],[1,0],[1,1]],                 count: 1 },
    { id: 'quad_l',    cells: [[0,0],[1,0],[2,0],[2,1]],                 count: 1 },
    { id: 'long',      cells: [[0,0],[0,1],[0,2],[0,3]],                 count: 1 },
    { id: 'cathedral', cells: [[0,1],[1,0],[1,1],[1,2],[2,1]],           count: 1 },
]

const OPPONENT_PIECES = [
    { id: 'mono',    cells: [[0,0]],                         count: 1 },
    { id: 'duo',     cells: [[0,0],[0,1]],                   count: 1 },
    { id: 'trio_l',  cells: [[0,0],[1,0],[1,1]],             count: 2 },
    { id: 'quad_sq', cells: [[0,0],[0,1],[1,0],[1,1]],       count: 1 },
]

const SAMPLE_HISTORY = [
    { move: 1,  player: 'Opponent', action: 'Cathedral → D5'    },
    { move: 2,  player: 'You',      action: 'Long → B2–B5'      },
    { move: 3,  player: 'Opponent', action: 'Square → G3'       },
    { move: 4,  player: 'You',      action: 'Trio-L → H6'       },
    { move: 5,  player: 'Opponent', action: 'Mono → A1'         },
    { move: 6,  player: 'You',      action: 'Duo → C8'          },
    { move: 7,  player: 'Opponent', action: 'Trio-I → F4–F6'    },
    { move: 8,  player: 'You',      action: 'Quad-L → I2'       },
]

const BOARD_SIZE = 10

function GameBoard() {
    const [hovered, setHovered] = useState(null)

    return (
        <div className={styles.boardWrapper}>
            <div className={styles.boardLabelsTop}>
                {Array.from({ length: BOARD_SIZE }, (_, i) =>
                    <span key={i}>{String.fromCharCode(65 + i)}</span>
                )}
            </div>
            <div className={styles.boardRow}>
                <div className={styles.boardLabelsLeft}>
                    {Array.from({ length: BOARD_SIZE }, (_, i) =>
                        <span key={i}>{i + 1}</span>
                    )}
                </div>
                <div className={styles.board}>
                    {Array.from({ length: BOARD_SIZE * BOARD_SIZE }, (_, i) => {
                        const r = Math.floor(i / BOARD_SIZE)
                        const c = i % BOARD_SIZE
                        const isLight = (r + c) % 2 === 0
                        return (
                            <div
                                key={i}
                                className={`${styles.cell} ${isLight ? styles.cellLight : styles.cellDark} ${hovered === i ? styles.cellHovered : ''}`}
                                onMouseEnter={() => setHovered(i)}
                                onMouseLeave={() => setHovered(null)}
                            />
                        )
                    })}
                </div>
            </div>
        </div>
    )
}

function Timer({ time, label, active }) {
    return (
        <div className={`${styles.timer} ${active ? styles.timerActive : ''}`}>
            <span className={styles.timerLabel}>{label}</span>
            <span className={styles.timerValue}>{time}</span>
        </div>
    )
}

function MoveHistory({ entries }) {
    return (
        <div className={styles.historyList}>
            {entries.map((h) => (
                <div key={h.move} className={`${styles.historyEntry} ${h.player === 'You' ? styles.historyYou : styles.historyOpponent}`}>
                    <span className={styles.historyIndex}>{h.move}.</span>
                    <span className={styles.historyPlayer}>{h.player}</span>
                    <span className={styles.historyAction}>{h.action}</span>
                </div>
            ))}
        </div>
    )
}

function WinnerPopup({ winner, onClose }) {
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

export default function GamePage() {
    const [gameOver, setGameOver] = useState(false)
    const [winner, setWinner]     = useState(null)
    const [showPopup, setShowPopup] = useState(false)

    const playerName   = 'Player'
    const opponentName = 'Opponent'
    const playerTime   = '08:42'
    const opponentTime = '09:15'
    const playerTurn   = true

    function handleSurrender() {
        setWinner(opponentName)
        setGameOver(true)
        setShowPopup(true)
    }

    function handleOfferDraw() {
        //TODO
    }

    return (
        <div className={styles.page}>
            <div className={styles.layout}>

                {/* ── Left column ── */}
                <aside className={styles.leftCol}>
                    <section className={styles.panelSmall}>
                        <h3 className={styles.panelTitle}>Opponent's hand</h3>
                        <div className={styles.piecesGridCompact}>
                            {OPPONENT_PIECES.map(p => (
                                <PieceSlot key={p.id} piece={p} count={p.count} color={OPPONENT_COLOR} compact />
                            ))}
                        </div>
                    </section>

                    <section className={styles.panelLarge}>
                        <h3 className={styles.panelTitle}>Your hand</h3>
                        <div className={styles.piecesGrid}>
                            {PLAYER_PIECES.map(p => (
                                <PieceSlot key={p.id} piece={p} count={p.count} color={PLAYER_COLOR} />
                            ))}
                        </div>
                    </section>
                </aside>

                {/* ── Center column ── */}
                <main className={styles.centerCol}>
                    <GameBoard />
                </main>

                {/* ── Right column ── */}
                <aside className={styles.rightCol}>
                    <Timer time={opponentTime} label={opponentName} active={!playerTurn} />

                    <section className={styles.historyPanel}>
                        <h3 className={styles.panelTitle}>Move history</h3>
                        <MoveHistory entries={SAMPLE_HISTORY} />
                    </section>

                    <Timer time={playerTime} label={playerName} active={playerTurn} />

                    <div className={styles.actionButtons}>
                        {!gameOver ? (
                            <>
                                <button className={styles.btnDraw} onClick={handleOfferDraw}>Offer Draw</button>
                                <button className={styles.btnSurrender} onClick={handleSurrender}>Surrender</button>
                            </>
                        ) : (
                            <>
                                <button className={styles.btnAction}>Rematch</button>
                                <button className={styles.btnAction}>New Game</button>
                                <button className={styles.btnAnalyze}>Analyze</button>
                            </>
                        )}
                    </div>
                </aside>
            </div>

            {showPopup && (
                <WinnerPopup winner={winner} onClose={() => setShowPopup(false)} />
            )}
        </div>
    )
}
