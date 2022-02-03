from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.started = False
        self.x = 0
        self.y = 0
        self.canvas.bind_all('<KeyPress-Return>', self.start)
        self.bounce_count = 0

    def bounce(self):
        self.bounce_count += 1

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
            return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y *= -1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y *= -1
            self.x = self.x + self.paddle.x
            self.bounce()
        if pos[0] <= 0:
            self.x *= -1
        if pos[2] >= self.canvas_width:
            self.x *= -1

    def start(self, evt):
        if self.started == False:
            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]
            self.y = -3
            self.started = True

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[0] > 0:
            self.x = -2

    def turn_right(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[2] < self.canvas_width:
            self.x = 2

    def destroy(self):
        self.destroy()

def main():
    tk = Tk()
    tk.title("Игра")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()
    maxscore = 0

    score = canvas.create_text(45, 20, text="score 0", font=('Courier', 16))
    max = canvas.create_text(58, 40, text="max " + str(maxscore), font=('Courier', 16))
    finish = canvas.create_text(220, 200, text='Game over', font=('Courier', 22), state="hidden")

    while True:
        paddle = Paddle(canvas, 'blue')
        ball = Ball(canvas, paddle, 'red')

        while ball.hit_bottom == False:
            ball.draw()
            paddle.draw()
            canvas.itemconfig(score,text="score " + str(ball.bounce_count))
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)

        time.sleep(0.5)
        canvas.itemconfig(paddle.id, state="hidden")
        canvas.itemconfig(ball.id, state="hidden")
        canvas.itemconfig(finish, state="normal")
        tk.update()

        if ball.bounce_count > maxscore:
            maxscore = ball.bounce_count
            canvas.itemconfig(max, text="max " + str(maxscore))

        time.sleep(1)
        canvas.itemconfig(finish, state="hidden")

if __name__ == "__main__":
    main()
