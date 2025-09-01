import pyxel


class App:
    def __init__(self):
        pyxel.init(320, 240, title="Pyxel Draw API")
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


    def draw(self):
        pyxel.cls(0)
        self.test_line(106, 6)
        self.test_rect(6, 38)
        self.test_rectb(106, 38)
        self.test_text(6, 124)
    def test_line(self, x, y):
        pyxel.text(x, y, "line(x1,y1,x2,y2,col)", 7)

        x += 4
        y += 9
        col = 5

        for i in range(3):
            pyxel.line(x, y + i * 8, x + 48, y + i * 8, col)
            col += 1

        for i in range(4):
            pyxel.line(x + i * 16, y, x + i * 16, y + 16, col)
            col += 1

        for i in range(4):
            pyxel.line(x + i * 16, y, x + (3 - i) * 16, y + 16, col)
            col += 1

    def test_rect(self, x, y):
        pyxel.text(x, y, "rect(x,y,w,h,col)", 7)

        x += 4
        y += 16
        for i in range(8):
            pyxel.rect(x + i * 8, y - i, i + 1, i + 1, i + 8)

    def test_rectb(self, x, y):
        pyxel.text(x, y, "rectb(x,y,w,h,col)", 7)

    def test_text(self, x, y):
        pyxel.text(x, y, "text(x,y,s,col)", 7)

        x += 4
        y += 8
        s = (
            f"Elapsed frame count is {pyxel.frame_count}\n"
            f"Current mouse position is ({pyxel.mouse_x},{pyxel.mouse_y})"
        )
        pyxel.text(x + 1, y, s, 1)
        pyxel.text(x, y, s, 9)


App()
