import pyxel

from srcs.sudoku import SudokuData

INITIAL_POS = (-1, -1)
RESOLUTION = (320, 240)
CELL_SIZE = 24
class App():
    def __init__(self):
        self.sudoku = SudokuData()

        self.position = INITIAL_POS
        self.log = True 

        pyxel.init(*RESOLUTION, title="Pyxel Sudoku")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # NOTE: cell check
            pos_x = (pyxel.mouse_x - 12) // CELL_SIZE
            pos_y = (pyxel.mouse_y - 12) // CELL_SIZE
            if pos_x >= 0 and pos_x < 9 and \
               pos_y >= 0 and pos_y < 9:
                self.position = (pos_x, pos_y)

    def draw(self):
        pyxel.cls(0)

        # NOTE: draw cell
        for i in range(9):
            for j in range(9):
                if self.position[0] == i and self.position[1] == j:
                    rect_func = pyxel.rect
                else:
                    rect_func = pyxel.rectb
                rect_func(12 + i * CELL_SIZE,
                          12 + j * CELL_SIZE,
                          CELL_SIZE,
                          CELL_SIZE,
                          1)
                pyxel.text(12 + i * CELL_SIZE + 10,
                           12 + j * CELL_SIZE + 10,
                           f"{self.sudoku.problem_array[j][i]}", 3)

        if self.log:
            pyxel.text(0, 0, f"mouse clicked {self.position}", 3)

if __name__ == "__main__":
    App()
