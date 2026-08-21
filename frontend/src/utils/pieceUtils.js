export const CELL_SIZE  = 64
export const BOARD_SIZE = 10

export function rotateCell(cells, times) {
    let result = cells.map(([x, y]) => [x, y])
    for (let i = 0; i < times % 4; i++) {
        result = result.map(([x, y]) => [-y, x])
    }
    return result
}
