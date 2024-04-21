import turtle

# Создаем экран
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("Скибиди туалет")

# Создаем черепашку
t = turtle.Turtle()
t.speed(0)  # Максимальная скорость

# Функция для рисования прямоугольника
def draw_rectangle(x, y, width, height, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()

# Рисуем стены
draw_rectangle(-200, -100, 400, 200, "lightblue")

# Рисуем крышу
t.penup()
t.goto(-220, 100)
t.pendown()
t.color("brown")
t.begin_fill()
t.goto(220, 100)
t.goto(0, 220)
t.goto(-220, 100)
t.end_fill()

# Рисуем дверь
draw_rectangle(-40, -100, 80, 100, "white")

# Рисуем окно
draw_rectangle(100, 0, 80, 80, "white")

# Рисуем туалет
draw_rectangle(-180, -80, 80, 60, "white")

# Надпись "СКИБИДИ"
t.penup()
t.goto(-160, -40)
t.pendown()
t.color("black")
t.write("СКИБИДИ", align="center", font=("Arial", 16, "bold"))

# Надпись "ТУАЛЕТ"
t.penup()
t.goto(-160, -70)
t.pendown()
t.color("black")
t.write("ТУАЛЕТ", align="center", font=("Arial", 16, "bold"))

# Закрываем окно при клике
screen.mainloop()
