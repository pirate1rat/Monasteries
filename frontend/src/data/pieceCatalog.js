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
'neutral',
"Cathedral",
),

1: new PiecePrefab(
    [[0, 0]],
    1,
    'white',
    "Tavern_white",
),

2: new PiecePrefab(
    [[0, 0]],
    1,
    'red',
    "Tavern_red",
),

3: new PiecePrefab(
    [[0, 0], [0, 1]],
    2,
    'white',
    "Stable_white",
),

4: new PiecePrefab(
    [[0, 0], [0, 1]],
    2,
    'red',
    "Stable_red",
),

5: new PiecePrefab(
    [[0, 0], [1, 0], [0, 1]],
    3,
    'white',
    "Inn_white",
),

6: new PiecePrefab(
    [[0, 0], [1, 0], [0, 1]],
    3,
    'red',
    "Inn_red",
),

7: new PiecePrefab(
    [[0, 0], [0, -1], [0, 1]],
    3,
    'white',
    "Bridge_white",
),

8: new PiecePrefab(
    [[0, 0], [0, -1], [0, 1]],
    3,
    'red',
    "Bridge_red",
),

9: new PiecePrefab(
    [[0, 0], [1, 0], [1, 1], [0, 1]],
    4,
    'white',
    "Square_white",
),

10: new PiecePrefab(
    [[0, 0], [1, 0], [1, 1], [0, 1]],
    4,
    'red',
    "Square_red",
),

11: new PiecePrefab(
    [[0, 0], [1, 0], [0, 1], [-1, 0]],
    4,
    'white',
    "Manor_white",
),

12: new PiecePrefab(
    [[0, 0], [1, 0], [0, 1], [-1, 0]],
    4,
    'red',
    "Manor_red",
),

13: new PiecePrefab(
    [[0, 0], [1, 0], [0, 1], [-1, 1]],
    4,
    'white',
    "Abbey_white",
),

14: new PiecePrefab(
    [[0, 0], [1, 1], [0, 1], [1, 0]],
    4,
    'red',
    "Abbey_red",
),

15: new PiecePrefab(
    [[0, 0], [1, 0], [0, 1], [-1, -1], [0, -1]],
    5,
    'white',
    "Academy_white",
),

16: new PiecePrefab(
    [[0, 0], [0, -1], [1, -1], [0, 1], [-1, 0]],
    5,
    'red',
    "Academy_red",
),

17: new PiecePrefab(
    [[0, 0], [0, -1], [1, 0], [0, 1], [-1, 0]],
    5,
    'white',
    "Infirmary_white",
),

18: new PiecePrefab(
    [[0, 0], [0, -1], [1, 0], [0, 1], [-1, 0]],
    5,
    'red',
    "Infirmary_red",
),

19: new PiecePrefab(
    [[0, 0], [1, 0], [1, 1], [-1, 1], [-1, 0]],
    5,
    'white',
    "Castle_white",
),

20: new PiecePrefab(
    [[0, 0], [1, 0], [1, 1], [-1, 1], [-1, 0]],
    5,
    'red',
    "Castle_red",
),

21: new PiecePrefab(
    [[0, 0], [0, -1], [1, -1], [-1, 1], [-1, 0]],
    5,
    'white',
    "Tower_white",
),

22: new PiecePrefab(
    [[0, 0], [0, -1], [1, -1], [-1, 1], [-1, 0]],
    5,
    'red',
    "Tower_red",
),
};

Object.freeze(PIECE_CATALOG);