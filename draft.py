from typing import *


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        return self.is_valid_squares(board) and self.is_valid_columns(board) and self.is_valid_rows(board)

    def is_valid_rows(self, board: list[list[str]]):
        is_valid = True
        for row in board:
            is_valid &= self.is_valid_unit(row)
        return is_valid

    def is_valid_squares(self, board: list[list[str]]):
        is_valid = True
        for y in range(3, 10, 3):
            for x in range(3, 10, 3):
                is_valid &= self.is_valid_unit([num for line in board[y-3:y] for num in line[x-3:x]])
        return is_valid

    def is_valid_columns(self, board: list[list[str]]):
        is_valid = True
        for column in zip(*board):
            is_valid &= self.is_valid_unit(column)
        return is_valid

    def is_valid_unit(self, line: Iterable[Any]):
        return len(set(x for x in line if x != '.')) == len([x for x in line if x != '.'])


sol = Solution()
print(sol.isValidSudoku([["5", "3", ".", ".", "7", ".", ".", ".", "."],
                         ["6", ".", "3", "1", "9", "5", ".", ".", "."],
                         [".", "9", "8", ".", ".", ".", ".", "6", "."],
                         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
                         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                         [".", "6", ".", ".", ".", ".", "2", "8", "."],
                         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]))
