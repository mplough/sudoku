from collections import Counter
from typing import Self


def is_invalid(vec: list[int | None]):
    c = Counter(vec)
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if c[i] > 1:
            return True
    return False


def is_done(vec: list[int | None]):
    c = Counter(vec)
    return all(c[i] == 1 for i in [1, 2, 3, 4, 5, 6, 7, 8, 9])


class Board:
    def __init__(self, nums: list[list[int | None]] | None) -> None:
        if nums is None:
            self.nums = [[None] * 9] * 9
        else:
            self.nums = nums

    def row(self, r: int) -> list[int | None]:
        return self.nums[r]

    @property
    def rows(self):
        for r in range(9):
            yield self.row(r)

    def column(self, c: int) -> list[int | None]:
        return [self.nums[r][c] for r in range(9)]

    @property
    def columns(self):
        for c in range(9):
            yield self.column(c)

    def sector_of(self, r: int, c: int):
        row_group = r // 3
        col_group = c // 3

        return 3 * row_group + col_group

    def sector(self, s: int) -> list[int | None]:
        """Return sector as list.

        0 1 2
        3 4 5
        6 7 8
        """
        row_start = s // 3
        row_indices = [3 * row_start + i for i in range(3)]

        col_start = 3 * (s % 3)
        col_indices = [col_start + i for i in range(3)]

        return [
            self.nums[r][c]
            for r in row_indices
            for c in col_indices
        ]

    @property
    def sectors(self):
        for s in range(9):
            yield self.sector(s)

    @property
    def is_invalid(self):
        return any(is_invalid(r) for r in self.rows) \
            or any(is_invalid(c) for c in self.columns) \
            or any(is_invalid(s) for s in self.sectors)

    @property
    def is_done(self):
        return all(is_done(r) for r in self.rows) \
            and all(is_done(c) for c in self.columns) \
            and all(is_done(s) for s in self.sectors)

    def __str__(self):
        return "\n".join(
            " ".join("x" if c is None else str(c) for c in row)
            for row in self.rows
        )

    def allowed_vals(self, r, c) -> set[int]:
        row_vals = {v for v in self.row(r) if v is not None}
        column_vals = {v for v in self.column(c) if v is not None}
        sector_vals = {v for v in self.sector(self.sector_of(r, c)) if v is not None}
        vals = row_vals | column_vals | sector_vals
        return set(sorted({1, 2, 3, 4, 5, 6, 7, 8, 9} - vals))

    def next(self, r: int, c: int) -> tuple[int, int]:
        if c % 9 == 8:
            return r + 1, 0
        return r, c + 1

    def solve(self, r=0, c=0):
        # check if we're done - if so, return
        # check if invalid - if so, return failure
        # determine what values are allowed in each cell
        # if no values are allowed, return failure
        print(self)
        print()

        if self.is_done:
            print("DONE")
            print(self)
            return True
        if self.is_invalid:
            print("invalid")
            return False

        if r > 8 or c > 8:
            return False

        if self.nums[r][c] is not None:
            # already filled in
            return self.solve(*self.next(r, c))
        else:
            vs = self.allowed_vals(r, c)

            if not vs and self.nums[r][c] is None:
                print("DEAD END")
                return False

            for v in vs:
                print(r, c, v)
                # try the value
                self.nums[r][c] = v
                if self.solve(*self.next(r, c)):
                    return True
            # back out
            self.nums[r][c] = None
            return False


invalid = Board(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [9, 1, 2, 3, 4, 5, 6, 7, 9],
    ]
)

b = Board(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9] + [None] * 8,
        [8] + [None] * 8,
        [7] + [None] * 8,
        [6] + [None] * 8,
        [5] + [None] * 8,
        [4] + [None] * 8,
        [3] + [None] * 8,
        [2] + [None] * 8,
    ]
)

b1 = Board(
    [
        [None, None, 1, None, 4, None, None, 7, None],
        [None, None, None, 5, 7, 2, 8, None, None],
        [None, None, None, 1, 3, None, 5, None, None],
        [7, None, None, None, None, 1, None, None, None],
        [None, None, 6, 3, None, None, None, 5, None],
        [2, 1, 8, 4, None, None, 3, None, None],
        [9, None, 2, 7, None, None, 4, 1, None],
        [None, 8, None, None, None, None, 7, 6, 3],
        [None, None, None, None, None, 5, None, None, None],
    ]
)

b2 = Board(
    [
        [None, 2, None, 3, None, None, None, None, 9],
        [5, None, None, 4, None, None, None, 2, 3],
        [None, 3, 6, 2, 1, None, None, None, 8],
        [None, 4, None, 7, None, None, None, None, None],
        [3, None, None, 9, None, None, 1, 6, 4],
        [9, 6, None, 5, 4, None, None, None, None],
        [2, None, None, None, None, None, None, 3, 1],
        [None, 5, None, None, None, 3, None, None, None],
        [6, 9, None, 1, 2, None, 5, 8, None],
    ]
)
