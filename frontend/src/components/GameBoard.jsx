import { BOARD_SIZE, rotateCell } from '../utils/pieceUtils'
import styles from './GameBoard.module.css'

export function GameBoard({ boardData, drag, onBoardMouseUp, onBoardMouseMove, onBoardContextMenu, boardRef, playerColor}) {
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

    const isValid = invalidCells.size === 0 && previewCells.size > 0

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
                            const isPlayerColor = (playerColor === 'white' && cell.color === 1)
                                                || (playerColor === 'red'   && cell.color === 2)
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
