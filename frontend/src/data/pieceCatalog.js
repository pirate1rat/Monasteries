export class PiecePrefab {
    constructor(shape, size, color, name, startingAmount) {
        this.shape = shape;
        this.size = size;
        this.color = color;
        this.name = name;

        Object.freeze(this);
    }
}

export const PIECE_CATALOG = {
    0: new PiecePrefab(
        [[0, 0], [0, -1], [1, 0], [0, 1], [0, 2], [-1, 0]],
        6,
        PlayerColor.NEUTRAL,
        "Cathedral",
    ),

    1: new PiecePrefab(
        [[0, 0]],
        1,
        PlayerColor.WHITE,
        "Tavern_white",
    ),

    2: new PiecePrefab(
        [[0, 0]],
        1,
        PlayerColor.RED,
        "Tavern_red",
    ),

    3: new PiecePrefab(
        [[0, 0], [0, 1]],
        2,
        PlayerColor.WHITE,
        "Stable_white",
    ),

    4: new PiecePrefab(
        [[0, 0], [0, 1]],
        2,
        PlayerColor.RED,
        "Stable_red",
    ),

    5: new PiecePrefab(
        [[0, 0], [1, 0], [0, 1]],
        3,
        PlayerColor.WHITE,
        "Inn_white",
    ),

    6: new PiecePrefab(
        [[0, 0], [1, 0], [0, 1]],
        3,
        PlayerColor.RED,
        "Inn_red",
    ),

    7: new PiecePrefab(
        [[0, 0], [0, -1], [0, 1]],
        3,
        PlayerColor.WHITE,
        "Bridge_white",
    ),

    8: new PiecePrefab(
        [[0, 0], [0, -1], [0, 1]],
        3,
        PlayerColor.RED,
        "Bridge_red",
    ),

    9: new PiecePrefab(
        [[0, 0], [1, 0], [1, 1], [0, 1]],
        4,
        PlayerColor.WHITE,
        "Square_white",
    ),

    10: new PiecePrefab(
        [[0, 0], [1, 0], [1, 1], [0, 1]],
        4,
        PlayerColor.RED,
        "Square_red",
    ),

    11: new PiecePrefab(
        [[0, 0], [1, 0], [0, 1], [-1, 0]],
        4,
        PlayerColor.WHITE,
        "Manor_white",
    ),

    12: new PiecePrefab(
        [[0, 0], [1, 0], [0, 1], [-1, 0]],
        4,
        PlayerColor.RED,
        "Manor_red",
    ),

    13: new PiecePrefab(
        [[0, 0], [1, 0], [0, 1], [-1, 1]],
        4,
        PlayerColor.WHITE,
        "Abbey_white",
    ),

    14: new PiecePrefab(
        [[0, 0], [1, 1], [0, 1], [1, 0]],
        4,
        PlayerColor.RED,
        "Abbey_red",
    ),

    15: new PiecePrefab(
        [[0, 0], [1, 0], [0, 1], [-1, -1], [0, -1]],
        5,
        PlayerColor.WHITE,
        "Academy_white",
    ),

    16: new PiecePrefab(
        [[0, 0], [0, -1], [1, -1], [0, 1], [-1, 0]],
        5,
        PlayerColor.RED,
        "Academy_red",
    ),

    17: new PiecePrefab(
        [[0, 0], [0, -1], [1, 0], [0, 1], [-1, 0]],
        5,
        PlayerColor.WHITE,
        "Infirmary_white",
    ),

    18: new PiecePrefab(
        [[0, 0], [0, -1], [1, 0], [0, 1], [-1, 0]],
        5,
        PlayerColor.RED,
        "Infirmary_red",
    ),

    19: new PiecePrefab(
        [[0, 0], [1, 0], [1, 1], [-1, 1], [-1, 0]],
        5,
        PlayerColor.WHITE,
        "Castle_white",
    ),

    20: new PiecePrefab(
        [[0, 0], [1, 0], [1, 1], [-1, 1], [-1, 0]],
        5,
        PlayerColor.RED,
        "Castle_red",
    ),

    21: new PiecePrefab(
        [[0, 0], [0, -1], [1, -1], [-1, 1], [-1, 0]],
        5,
        PlayerColor.WHITE,
        "Tower_white",
    ),

    22: new PiecePrefab(
        [[0, 0], [0, -1], [1, -1], [-1, 1], [-1, 0]],
        5,
        PlayerColor.RED,
        "Tower_red",
    ),
};

Object.freeze(PIECE_CATALOG);