export const CELL_SIZE  = 64
export const BOARD_SIZE = 10

export function rotateCell(cells, times) {
    let result = cells
    for (let i = 0; i < times; i++) {
        result = result.map(([r, c]) => [-c, r])
    }
    const minR = Math.min(...result.map(([r]) => r))
    const minC = Math.min(...result.map(([, c]) => c))
    return result.map(([r, c]) => [r - minR, c - minC])
}
