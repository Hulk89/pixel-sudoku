import pyxel

from srcs.sudoku import SudokuData

INITIAL_POS = (-1, -1)
RESOLUTION = (240, 320)
CELL_SIZE = 24
MARGIN_CELL = (min(*RESOLUTION) - (9 * CELL_SIZE)) // 2
OFFSET_CELL = (MARGIN_CELL, MARGIN_CELL)

OFFSET_INPUT = (RESOLUTION[0] - 4 - (3 * CELL_SIZE),
                RESOLUTION[0] + 4)

INPUT_LIST = [[1,2,3],[4,5,6],[7,8,9]]

class App():
    def __init__(self):
        self.sudoku = SudokuData(20)
        self.position = INITIAL_POS
        self.highlighted_number = -1

        pyxel.init(*RESOLUTION, title="Pyxel Sudoku")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        def update_cell(m_x, m_y):
            if m_x > OFFSET_CELL[0] and m_x < RESOLUTION[0] - OFFSET_CELL[0] and \
               m_y > OFFSET_CELL[1] and m_y < RESOLUTION[0] - OFFSET_CELL[1]:
                cell_x = (m_x - OFFSET_CELL[0]) // CELL_SIZE
                cell_y = (m_y - OFFSET_CELL[1]) // CELL_SIZE
                if cell_x >= 0 and cell_x < 9 and \
                   cell_y >= 0 and cell_y < 9:
                    prob_data = self.sudoku.problem_array[cell_y][cell_x]
                    if prob_data != 0:
                        return
                    self.position = (cell_x, cell_y)

        def update_input(m_x, m_y):
            if m_x > OFFSET_INPUT[0] and \
                 m_x < RESOLUTION[0] - 4 and \
                 m_y > OFFSET_INPUT[1] and \
                 m_y < RESOLUTION[1] - 4:
                # NOTE: input check.
                input_x = (m_x - OFFSET_INPUT[0]) // CELL_SIZE
                input_y = (m_y - OFFSET_INPUT[1]) // CELL_SIZE
                if sum(self.position) != sum(INITIAL_POS):
                    dup_pos = SudokuData.duplicate_pos(self.sudoku.solve_array,
                                                       self.position[0],
                                                       self.position[1],
                                                       INPUT_LIST[input_y][input_x])
                    if dup_pos is None:
                        self.sudoku.solve_array[self.position[1]][self.position[0]] = INPUT_LIST[input_y][input_x]
                        self.highlighted_number = -1
                    else:
                        self.highlighted_number = INPUT_LIST[input_y][input_x]

                self.position = INITIAL_POS
        m_x = pyxel.mouse_x
        m_y = pyxel.mouse_y

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            update_cell(m_x, m_y)
            update_input(m_x, m_y)
           
    def draw(self):
        pyxel.cls(0)

        # NOTE: draw cell
        for i in range(9):
            for j in range(9):
                color = pyxel.COLOR_LIGHT_BLUE
                text_color = pyxel.COLOR_BLACK
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
                    color = pyxel.COLOR_GRAY
                    text_color = pyxel.COLOR_WHITE

                text = self.sudoku.solve_array[j][i]
                if self.highlighted_number == text:
                    color = pyxel.COLOR_RED
                    text_color = pyxel.COLOR_WHITE
                    rect_func = pyxel.rect

                rect_func(12 + i * CELL_SIZE,
                          12 + j * CELL_SIZE,
                          CELL_SIZE,
                          CELL_SIZE,
                          color)


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

        # NOTE: draw input square
        for i in range(3):
            for j in range(3):
                pyxel.rectb(OFFSET_INPUT[0] + CELL_SIZE * i,
                            OFFSET_INPUT[1] + CELL_SIZE * j,
                            CELL_SIZE,
                            CELL_SIZE,
                            pyxel.COLOR_LIGHT_BLUE)
                pyxel.text(OFFSET_INPUT[0] + 10 + CELL_SIZE * i,
                           OFFSET_INPUT[1] + 10 + CELL_SIZE * j,
                           f"{INPUT_LIST[j][i]}",
                           pyxel.COLOR_LIGHT_BLUE)

if __name__ == "__main__":
    App()
