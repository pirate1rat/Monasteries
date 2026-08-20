import styles from './PiecePanel.module.css'

const images = import.meta.glob(
    '/src/assets/pieces/*.png', { 
        eager: true, 
        query: '?url', 
        import: 'default' 
    }
)

function PieceImage({ name, rotation, size = 48 }) {
    const src = images[`/src/assets/pieces/${name}.png`]
    return (
        <img
            src={src}
            alt={name}
            style={{
                width: size,
                height: size,
                objectFit: 'contain',
                transform: `rotate(${rotation * 90}deg)`,
                transition: 'transform 0.1s ease',
                userSelect: 'none',
                pointerEvents: 'none',
            }}
        />
    )
}

function PieceGrid({ cells, color, cellSize = 16 }) {
    const minX = Math.min(...cells.map(([x]) => x))
    const minY = Math.min(...cells.map(([, y]) => y))
    const maxX = Math.max(...cells.map(([x]) => x))
    const maxY = Math.max(...cells.map(([, y]) => y))
    const rows = maxY - minY + 1
    const cols = maxX - minX + 1
    const filled = new Set(cells.map(([x, y]) => `${y - minY},${x - minX}`))

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

export function PieceSlot({ piece, quantity, color, compact, onDragStart, isSelected, style }) {
    const cellSize = compact ? 16 : 48
    
    function handleMouseDown(e) {
        if (e.button !== 0) return
        e.preventDefault()
        onDragStart?.(piece.piece_id)
    }

    return (
        <div
            className={`${styles.pieceSlot} ${compact ? styles.pieceSlotCompact : ''} ${isSelected ? styles.pieceSlotSelected : ''}`}
            onMouseDown={handleMouseDown}
            style={{ cursor: 'grab', ...style }}
        >
            <div className={styles.pieceShape}>
                {/* <PieceImage name={piece.name} rotation={piece.rotation}/> */}
                <PieceGrid cells={piece.cells} color={color} cellSize={cellSize}/>
            </div>
            <span className={styles.pieceCount} style={{ color }}>×{quantity}</span>
        </div>
    )
}

export function PiecePanel({ title, pieces, color, compact, dragPieceId, onDragStart, isFirstMove }) {
    return (
        <section className={compact ? styles.panelSmall : styles.panelLarge}>
            <h3 className={styles.panelTitle}>{title}</h3>
            <div className={compact ? styles.piecesGridCompact : styles.piecesGrid}>
                {pieces.map((p, i) => {
                    const isCathedral = p.piece_id === 0
                    const disabled = isFirstMove && !isCathedral
                    return (
                        <PieceSlot
                            key={`${p.piece_id}_${i}`}
                            piece={p}
                            quantity={p.quantity}
                            color={color}
                            compact={compact}
                            isSelected={dragPieceId === p.piece_id}
                            onDragStart={!disabled ? onDragStart : undefined}
                            style={{ opacity: disabled ? 0.2 : 1, pointerEvents: disabled ? 'none' : 'auto' }}
                        />
                    )
                })}
            </div>
        </section>
    )
}
