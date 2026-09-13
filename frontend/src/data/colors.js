export const PIECE_COLOR = {
    'white': '#e6cfa7',
    'red': '#6d0870',
    'neutral': '#B0B0B0'
}

const COLOR_CELL_ALPHA = 0.8

function hexToRgba(hex, alpha) {
    const value = hex.replace('#', '')
    const r = parseInt(value.slice(0, 2), 16)
    const g = parseInt(value.slice(2, 4), 16)
    const b = parseInt(value.slice(4, 6), 16)
    return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

export const BOARD_CELL_COLOR = {
    'white': hexToRgba(PIECE_COLOR.white, COLOR_CELL_ALPHA),
    'red': hexToRgba(PIECE_COLOR.red, COLOR_CELL_ALPHA),
    'neutral': hexToRgba(PIECE_COLOR.neutral, COLOR_CELL_ALPHA),
    'valid': 'rgba(61, 255, 100, 0.55)', //'rgba(100,200,120,0.55)',
    'invalid': 'rgba(255, 0, 0, 0.45)'
}

export function getPlayerColor(color) {
    return PIECE_COLOR[color]
}

export function getOpponentColor(color) {
    return color === 'white' ? PIECE_COLOR.red : PIECE_COLOR.white
}