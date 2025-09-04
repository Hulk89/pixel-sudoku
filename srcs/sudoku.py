from typing import List, Tuple
import random
from srcs.solve import is_unique_solution


def shuffle_lines(array: List[List[int]]):
    box_num = random.choice([0, 1, 2])
    l1, l2 = random.sample([0, 1, 2], 2)
    l1 += box_num * 3
    l2 += box_num * 3
    array[l1], array[l2] = array[l2], array[l1]
    return



class SudokuData:
    BOARD_SIZE = 9
    SUBGRID_SIZE = 3
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

    def __init__(self, omit_number=15):
        self.solution_array = self._transform(SudokuData.INITAL_SUDOKU)
        self.problem_array = self._omit_number(self.solution_array, omit_number)
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
        for i in range(random.randint(1,8)):
            shuffle_lines(new_arr)

        return new_arr

    @staticmethod
    def _omit_number(array: List[List[int]], omit_number) -> List[List[int]]:
        """
        sudoku array를 카피하여, omit_number만큼 숫자가 빠진 풀 수 있는 sudoku array를 리턴
        """
        new_arr = [row[:] for row in array]

        positions = [(i, j) for i in range(SudokuData.BOARD_SIZE) 
                    for j in range(SudokuData.BOARD_SIZE)]
        
        random.shuffle(positions)
        
        for i in range(min(omit_number, len(positions))):
            row, col = positions[i]
            tmp_dat = new_arr[row][col]
            new_arr[row][col] = 0

            if not is_unique_solution(new_arr):
                print(f"i: {i}")
                new_arr[row][col] = tmp_dat
                break
            
        return new_arr

    @staticmethod
    def duplicate_pos(array: List[List[int]], pos_x: int, pos_y: int, value: int):
        """
        sudoku array의 pos_x, pos_y에 value가 들어갔을 떄 풀 수 있는 것인지 확인
        """
        for row in range(SudokuData.BOARD_SIZE):
            if array[row][pos_x] == value:
                return (pos_x, row)
        for col in range(SudokuData.BOARD_SIZE):
            if array[pos_y][col] == value:
                return (col, pos_y)
        
        # Check 3x3 box
        box_col_start = (pos_x // SudokuData.SUBGRID_SIZE) * SudokuData.SUBGRID_SIZE
        box_row_start = (pos_y // SudokuData.SUBGRID_SIZE) * SudokuData.SUBGRID_SIZE
        
        for row in range(box_row_start, box_row_start + SudokuData.SUBGRID_SIZE):
            for col in range(box_col_start, box_col_start + SudokuData.SUBGRID_SIZE):
                if array[row][col] == value:
                    return (col, row)
        
        return None

