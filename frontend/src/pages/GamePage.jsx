import { useState, useEffect, useRef, useCallback } from 'react'
import { useGame } from '../hooks/useGame'
import { useParams } from 'react-router-dom'
import { PIECE_CATALOG } from '../data/pieceCatalog'
import styles from './GamePage.module.css'

import { PiecePanel } from '../components/PiecePanel'

const CELL_SIZE = 64
const BOARD_SIZE = 10
const DEV = import.meta.env.DEV
const images = import.meta.glob(
    '/src/assets/pieces/*.png',
    {
        eager: true,
        query: '?url',
        import: 'default',
    }
);

function rotateCell(cells, times) {
    let result = cells
    for(let i = 0; i < times; i++){
        result = result.map(([r, c]) => [-c, r])
    }
    const minR = Math.min(...result.map(([r]) => r))
    const minC = Math.min(...result.map(([, c]) => c))
    return result.map(([r, c]) => [r - minR, c - minC])
}

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

function GameBoard({ boardData, drag, onBoardMouseUp, onBoardMouseMove, onBoardContextMenu, boardRef}) {
    const previewCells = new Set()
    const invalidCells = new Set()

    if (drag.active && drag.boardPos) {
        const { row, col } = drag.boardPos
        const cells = rotateCell(drag.cells, drag.rotation)
        cells.forEach(([dr, dc]) => {
            const r = row + dr
            const c = col + dc
            const key = `${r},${c}`
            if (r < 0 || BOARD_SIZE <= r || c < 0 || BOARD_SIZE <= c) {
                invalidCells.add(key)
            } else {
                const cell = boardData[r * BOARD_SIZE + c]
                if (cell && cell.piece_id !== -1) {
                    invalidCells.add(key)
                } else {
                    previewCells.add(key)
                }
            }
        })
    }

    const isValid = invalidCells.size === 0 && previewCells > 0

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
                <div 
                    ref={boardRef} 
                    className={styles.board}
                    onMouseMove={onBoardMouseMove}
                    onMouseUp={onBoardMouseUp}
                    onContextMenu={onBoardContextMenu}
                >    
                    {Array.from({ length: BOARD_SIZE * BOARD_SIZE }, (_, i) => {
                        const r = Math.floor(i / BOARD_SIZE)
                        const c = i % BOARD_SIZE
                        const key = `${r},${c}`
                        const isLight = (r + c) % 2 === 0
                        const cell = boardData[i]

                        const isPreview = previewCells.has(key)
                        const isInvalid = invalidCells.has(key)
                        const isOccupied = cell && cell.piece_id !== -1

                        let bgColor = isLight ? 'var(--gp-cell-light)' : 'var(--gp-cell-dark)'
                        if (isOccupied) {
                            const isPlayerColor = (game.playerColor === 'WHITE' && cell.color === 1)
                                                || (game.playerColor === 'RED'   && cell.color === 2)
                            bgColor = isPlayerColor
                                ? 'rgba(200,169,110,0.8)'
                                : cell.color === 3
                                    ? 'rgba(180,180,180,0.6)'   // NEUTRAL
                                    : 'rgba(110,141,200,0.8)'
                        }
                        if (isPreview) bgColor = isValid
                            ? 'rgba(100,200,120,0.55)'
                            : 'rgba(200,80,80,0.45)'
                        if (isInvalid) bgColor = 'rgba(200,80,80,0.45)'

                        return (
                            <div
                                key={i}
                                className={styles.cell}
                                style={{ backgroundColor: bgColor }}
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
    const { gameId } = useParams()
    const game = useGame(gameId)

    const [gameOver, setGameOver] = useState(false)
    const [winner, setWinner] = useState(null)
    const [showPopup, setShowPopup] = useState(false)

    const playerName   = 'Player'
    const opponentName = 'Opponent'
    const playerTime   = '08:42'
    const opponentTime = '09:15'

    function handleOfferDraw() {
        //TODO
    }

    const [drag, setDrag] = useState({
        active: false,
        piece_id: null,
        cells: [],
        rotation: 0,
        boardPos: null,
    })

    const boardRef = useRef(null)

    function getBoardPos(e, cells, rotation) {
        const rect = boardRef.current?.getBoundingClientRect()
        if (!rect) return null
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top

        const rotated = rotateCell(cells, rotation)
        const maxR = Math.max(...rotated.map(([r]) => r))
        const maxC = Math.max(...rotated.map(([, c]) => c))

        const col = Math.floor(x / CELL_SIZE) - Math.floor(maxC / 2)
        const row = Math.floor(y / CELL_SIZE) - Math.floor(maxR / 2)

        return { row, col }
    }

    function handleDragStart(pieceId) {
        // console.log(pieceId)
        if (game.history.length === 0 && pieceId !== 0) return //forces to play cathedral 1st move

        const prefab = PIECE_CATALOG[pieceId]
        if (!prefab) return
        setDrag({
            active: true,
            piece_id: pieceId,
            cells: prefab.cells,
            rotation: 0,
            boardPos: null,
        })
        // console.log("drag start")
    }

    function handleBoardMouseMove(e) {
        if (!drag.active) return
        const pos = getBoardPos(e, drag.cells, drag.rotation)
        setDrag(prev => ({...prev, boardPos: pos}))
    }

    function handleBoardMouseUp(e) {
        if (!drag.active || e.button !== 0) return
        if (drag.boardPos) {
            const {row, col} = drag.boardPos
            const cells = rotateCell(drag.cells, drag.rotation)
            
            console.log('Place piece:', {
                piece_id: drag.piece_id,
                anchor:   [col, row],
                rotation: drag.rotation,
            })

            const isOnBoard = cells.every(([dr, dc]) => {
                const r = row + dr
                const c = col + dc
                return 0 <= r && r <BOARD_SIZE && 0 <= c && c < BOARD_SIZE
            })

            if (isOnBoard) {
                game.makeMove(drag.piece_id, [col, row], drag.rotation)
            }

        }
        setDrag({ active: false, piece_id: null, cells: [], rotation: 0, boardPos: null })
    }

    function handleBoardContextMenu(e) {
        e.preventDefault()
        if (!drag.active) return
        setDrag(prev => ({ ...prev, rotation: (prev.rotation + 1) % 4 }))
    }

    useEffect(() => {
        function handleKey(e) {
            if (e.key === 'Escape') {
               setDrag({ active: false, piece_id: null, cells: [], rotation: 0, boardPos: null }) 
            }
        }
        window.addEventListener('keydown', handleKey)

        function handleGlobalMouseUp(e) {
            if (e.button === 0 && drag.active) {
                setDrag({ active: false, piece_id: null, cells: [], rotation: 0, boardPos: null })
            }
        }
        window.addEventListener('mouseup', handleGlobalMouseUp)
        
        return () => {
            window.removeEventListener('keydown', handleKey)
            window.removeEventListener('mouseup', handleGlobalMouseUp)
        }
    }, [drag.active])

    const PLAYER_COLOR = game.playerColor === 'white' ? '#C8A96E' : '#6E8DC8'
    const OPPONENT_COLOR = game.playerColor === 'white' ? '#6E8DC8' : '#C8A96E'

    return (
        <div className={styles.page} style={{ cursor: drag.active ? 'grabbing' : 'default' }}>
            <div className={styles.layout}>

                {/* ── Left column ── */}
                <aside className={styles.leftCol}>
                    <PiecePanel 
                        title="Your hand"
                        pieces={game.playerPieces}
                        color={PLAYER_COLOR}
                        compact
                        dragPieceId={drag.piece_id}
                        onDragStart={game.isPlayerTurn ? handleDragStart : undefined}
                        isFirstMove={game.history.length === 0 && game.isPlayerTurn}
                    />

                    <PiecePanel
                        title="Opponent's hand"
                        pieces={game.oppPieces}
                        color={OPPONENT_COLOR}
                        compact
                        dragPieceId={null}
                        onDragStart={() => {}}
                        isFirstMove={false}
                    />
                </aside>

                {/* ── Center column ── */}
                <main className={styles.centerCol}>
                    <GameBoard
                        boardData={game.board}
                        drag={drag}
                        boardRef={boardRef}
                        onBoardMouseMove={handleBoardMouseMove}
                        onBoardMouseUp={handleBoardMouseUp}
                        onBoardContextMenu={handleBoardContextMenu}
                    />
                    {drag.active && (
                        <p style={{ textAlign: 'center', color: '#888', fontSize: 12, marginTop: 8 }} >
                            RMB or scroll — rotate | ESC — cancel
                        </p>
                    )}
                </main>

                {/* ── Right column ── */}
                <aside className={styles.rightCol}>
                    <Timer time={opponentTime} label={opponentName} active={!game.isPlayerTurn} />

                    <section className={styles.historyPanel}>
                        <h3 className={styles.panelTitle}>Move history</h3>
                        <MoveHistory entries={SAMPLE_HISTORY} />
                    </section>

                    <Timer time={playerTime} label={playerName} active={game.isPlayerTurn} />

                    <div className={styles.actionButtons}>
                        {!gameOver ? (
                            <>
                                <button className={styles.btnDraw} onClick={() => game.proposeDraw()}>Offer Draw</button>
                                <button className={styles.btnSurrender} onClick={() => game.resign()}>Surrender</button>
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

            {DEV && (
                <div style={{
                    position: 'fixed', bottom: 16, left: 16,
                    background: 'rgba(0,0,0,0.8)', padding: '8px 12px',
                    borderRadius: 8, display: 'flex', gap: 8, zIndex: 200
                }}>
                    <button onClick={() => { setWinner('You'); setGameOver(true); setShowPopup(true) }}>
                        [DEV] Win
                    </button>
                    <button onClick={() => { setWinner(opponentName); setGameOver(true); setShowPopup(true) }}>
                        [DEV] Lose
                    </button>
                    <button onClick={() => setShowPopup(false)}>
                        [DEV] Hide popup
                    </button>
                </div>
            )}
        </div>
    )
}
