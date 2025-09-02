from typing import List


class SudokuData:
    INITAL_SUDOKU = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    def __init__(self):
        self.solution_array = self._transform(SudokuData.INITAL_SUDOKU)
        self.problem_array = self._omit_number(self.solution_array)
        self.solve_array = [row[:] for row in self.problem_array]

    @staticmethod
    def _transform(array: List[List[int]]) -> List[List[int]]:
        """
        sudoku array를 카피하여, sudoku 패턴을 만족하는 array로 변환 후 리턴
        input: sudoku 2d array
        output: sudoku 2d array
        """
        new_arr = [row[:] for row in array]
        # TODO: must be implemented
        return new_arr

    @staticmethod
    def _omit_number(array: List[List[int]], omit_number: int = 2) -> List[List[int]]:
        """
        sudoku array를 카피하여, omit_number만큼 숫자가 빠진 풀 수 있는 sudoku array를 리턴
        """
        new_arr = [row[:] for row in array]
        # TODO: must be implemented
        new_arr[0][0] = 0
        new_arr[8][8] = 0
        return new_arr


