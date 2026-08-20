export const CELL_SIZE  = 64
export const BOARD_SIZE = 10

export function rotateCell(cells, times) {
    let result = cells.map(([x, y]) => [x, y])

    for (let i = 0; i < times % 4; i++) {
        result = result.map(([x, y]) => [-y, x])

        const minX = Math.min(...result.map(([x]) => x))
        const minY = Math.min(...result.map(([, y]) => y))
        result = result.map(([x, y]) => [x - minX, y - minY])
    }

    return result
}
