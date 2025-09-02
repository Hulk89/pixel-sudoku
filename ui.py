import pyxel

from srcs.sudoku import SudokuData

INITIAL_POS = (-1, -1)
RESOLUTION = (240, 320)
CELL_SIZE = 24
class App():
    def __init__(self):
        self.sudoku = SudokuData()
        self.position = INITIAL_POS

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
                prob_data = self.sudoku.problem_array[pos_y][pos_x]
                if prob_data != 0:
                    return
                self.position = (pos_x, pos_y)
                return
            # TODO: input check

    def draw(self):
        pyxel.cls(0)

        # NOTE: draw cell
        for i in range(9):
            for j in range(9):
                color = pyxel.COLOR_GRAY
                text_color = pyxel.COLOR_WHITE
                prob_data = self.sudoku.problem_array[j][i]

                if self.position[0] == i and self.position[1] == j:
                    # NOTE: position 안에 들어있으면
                    rect_func = pyxel.rect
                elif prob_data == 0:
                    # NOTE: input이면
                    rect_func = pyxel.rect
                    color = pyxel.COLOR_WHITE
                    text_color = pyxel.COLOR_BLACK
                elif self.position[0] == i or self.position[1] == j:
                    # NOTE: position과 같은 row, column highlight
                    rect_func = pyxel.rect
                    color = pyxel.COLOR_ORANGE
                    text_color = pyxel.COLOR_BLACK
                elif (self.position[0] // 3 == i // 3) and (self.position[1] // 3 == j // 3):
                    # NOTE: position과 같은 square highlight
                    rect_func = pyxel.rect
                    color = pyxel.COLOR_YELLOW
                    text_color = pyxel.COLOR_BLACK
                else:
                    rect_func = pyxel.rectb

                rect_func(12 + i * CELL_SIZE,
                          12 + j * CELL_SIZE,
                          CELL_SIZE,
                          CELL_SIZE,
                          color)

                text = self.sudoku.solve_array[j][i]
                if text != 0:
                    pyxel.text(12 + i * CELL_SIZE + 10,
                               12 + j * CELL_SIZE + 10,
                               f"{text}",
                               text_color)
        # NOTE: draw 3x3 square
        for i in range(3):
            for j in range(3):
                pyxel.rectb(12 + i * 3 * CELL_SIZE,
                            12 + j * 3 * CELL_SIZE,
                            3 * CELL_SIZE,
                            3 * CELL_SIZE,
                            pyxel.COLOR_RED)

if __name__ == "__main__":
    App()
