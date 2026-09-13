import { useState, useEffect, useRef } from 'react'
import { useGame } from '../hooks/useGame'
import { useParams, useNavigate } from 'react-router-dom'
import styles from './GamePage.module.css'
import { getPlayerColor, getOpponentColor } from '../data/colors'

import { PiecePanel } from '../components/PiecePanel'
import { GameBoard } from '../components/GameBoard'
import { GameTimer }    from '../components/GameTimer'
import { MoveHistory }  from '../components/MoveHistory'
import { GameControls } from '../components/GameControls'
import { WinnerPopup }  from '../components/WinnerPopup'
import { rotateCell } from '../utils/pieceUtils'
import { PIECE_CATALOG } from '../data/pieceCatalog'

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
)
const EMPTY_DRAG = { 
    active: false,
    piece_id: null,
    cells: [], 
    rotation: 0,
    boardPos: null
}

export default function GamePage() {
    const navigate = useNavigate()
    const { gameId } = useParams()
    const game = useGame(gameId)

    const PLAYER_COLOR = getPlayerColor(game.playerColor)
    const OPPONENT_COLOR = getOpponentColor(game.playerColor)

    const [drag, setDrag] = useState(EMPTY_DRAG)
    const [showPopup, setShowPopup] = useState(false)
    
    const gameOver = game.status === 'finished'
    console.log(game.status, gameOver)
    let winner = null
    switch (game.result) {
        case 'white_wins':
            winner = 'White'; break
        case 'red_wins':
            winner = 'Red'; break
    }

    const boardRef = useRef(null)

    useEffect(() => {
        if (gameOver) setShowPopup(true)
    }, [gameOver])

    // ------ Drag helpers

    function getBoardPos(e) {
        const rect = boardRef.current?.getBoundingClientRect()
        if (!rect) return null

        const col = Math.floor((e.clientX - rect.left) / CELL_SIZE)
        const row = Math.floor((e.clientY - rect.top)  / CELL_SIZE)

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
        setDrag(prev => ({ ...prev, boardPos: getBoardPos(e) }))
    }

    function handleBoardMouseUp(e) {
        if (!drag.active || e.button !== 0) return
        
        const boardPos = getBoardPos(e)

        if (boardPos) {
            const { row, col } = boardPos
            const cells = rotateCell(drag.cells, drag.rotation)

            const isOnBoard = cells.every(([dx, dy]) => {
                const c = col + dx
                const r = row + dy
                return 0 <= r && r < BOARD_SIZE && 0 <= c && c < BOARD_SIZE
            })

            if (isOnBoard) {
                game.makeMove(drag.piece_id, [col, row], drag.rotation)
            }

            console.log('Place piece:', {
                piece_id: drag.piece_id,
                anchor:   [col, row],
                rotation: drag.rotation,
                name: PIECE_CATALOG[drag.piece_id].name
            })
        }

        setDrag(EMPTY_DRAG)
    }

    function handleBoardContextMenu(e) {
        e.preventDefault()
        if (!drag.active) return
        setDrag(prev => ({ ...prev, rotation: (prev.rotation + 1) % 4 }))
    }

    //-------------

    function handleNewGame() {
        navigate('/', { state: { openCreateModal: true }})
    }

    useEffect(() => {
        const handleKey = (e) => { if (e.key === 'Escape') setDrag(EMPTY_DRAG) }
        const handleGlobalMouseUp  = (e) => { if (e.button === 0 && drag.active) setDrag(EMPTY_DRAG) }
        window.addEventListener('keydown', handleKey)
        window.addEventListener('mouseup', handleGlobalMouseUp)
        
        return () => {
            window.removeEventListener('keydown', handleKey)
            window.removeEventListener('mouseup', handleGlobalMouseUp)
        }
    }, [drag.active])

    {console.log(game)}
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
                        onDragStart={game.isPlayerTurn ? handleDragStart : () => {}}
                        isFirstMove={game.history.length === 0 && game.isPlayerTurn}
                        collapsible ={false}
                    />

                    <PiecePanel
                        title="Opponent's hand"
                        pieces={game.oppPieces}
                        color={OPPONENT_COLOR}
                        compact
                        dragPieceId={null}
                        onDragStart={() => {}}
                        isFirstMove={false}
                        collapsible ={true}
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
                        serverTime={game.playerTime}
                        label="You"
                        active={game.isPlayerTurn}
                        gameOver={gameOver}
                        onTimeout={game.resign}
                    />

                    <MoveHistory
                        entries={game.history}
                        playerColor={game.playerColor}
                    />

                    <GameTimer 
                        serverTime={game.oppTime}
                        label="Opponent"
                        active={!game.isPlayerTurn}
                        gameOver={gameOver}
                        onTimeout={() => {}}
                    />

                    <GameControls
                        gameOver={gameOver}
                        onProposeDraw={game.proposeDraw}
                        drawOffered={game.drawOffered}
                        onAcceptDraw={game.acceptDraw}
                        onRejectDraw={game.rejectDraw}
                        onResign={game.resign}
                        onRematch={() => {}} //TODO
                        onNewGame={handleNewGame}
                        onAnalyze={() => {}} //TODO
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
                    <button onClick={() => { setWinner('Opponent'); setGameOver(true); setShowPopup(true) }}>
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
