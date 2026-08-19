import { useState, useEffect, useRef, useCallback } from 'react'
import { useGame } from '../hooks/useGame'
import { useParams } from 'react-router-dom'
import { PIECE_CATALOG } from '../data/pieceCatalog'
import styles from './GamePage.module.css'

import { PiecePanel } from '../components/PiecePanel'
import { GameBoard } from '../components/GameBoard'
import { GameTimer }    from '../components/GameTimer'
import { MoveHistory }  from '../components/MoveHistory'
import { GameControls } from '../components/GameControls'
import { WinnerPopup }  from '../components/WinnerPopup'
import { rotateCell } from '../utils/pieceUtils'

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
                        playerColor={game.playerColor}
                        onBoardMouseMove={handleBoardMouseMove}
                        onBoardMouseUp={handleBoardMouseUp}
                        onBoardContextMenu={handleBoardContextMenu}
                    />
                    {drag.active && (
                        <p className={styles.dragHint}>
                            RMB — rotate &nbsp;|&nbsp; ESC — cancel
                        </p>
                    )}
                </main>

                {/* ── Right column ── */}
                <aside className={styles.rightCol}>
                    <GameTimer 
                        time={opponentTime}
                        label={opponentName}
                        active={!game.isPlayerTurn} 
                    />

                    <MoveHistory
                        entries={SAMPLE_HISTORY}
                        playerColor={game.playerColor}
                    />

                    <GameTimer
                        time={game.playerTime}
                        label="You"
                        active={game.isPlayerTurn}
                    />

                    <GameControls
                        gameOver={gameOver}
                        onProposeDraw={game.proposeDraw}
                        onResign={game.resign}
                        onRematch={() => {}}
                        onNewGame={() => {}}
                        onAnalyze={() => {}}
                    />
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
