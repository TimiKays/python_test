import time
import turtle

def draw_line():
    turtle.fd(50)
    turtle.penup()
    turtle.fd(10)
    turtle.right(90)
    turtle.fd(10)


def draw_digital(i):
    turtle.pensize(8)
    if i in '2345689':
        turtle.pendown()
    draw_line()
    if i in '134567890':
        turtle.pendown()
    draw_line()
    if i in '2356890':
        turtle.pendown()
    draw_line()
    if i in '2680':
        turtle.pendown()
    turtle.fd(50)
    turtle.penup()
    turtle.fd(20)

    if i in '456890':
        turtle.pendown()
    draw_line()
    if i in '23567890':
        turtle.pendown()
    draw_line()
    if i in '12347890':
        turtle.pendown()
    draw_line()





def draw_date(today):
    turtle.setup(1100,800)
    turtle.penup()
    turtle.fd(-400)
    turtle.pencolor('red')
    for i in today:
        if i=='-':
            turtle.write('年', font=("Arial", 18, "normal"))
            turtle.pencolor('blue')
        elif i=='=':
            turtle.write('月',font=('Arial',18,'normal'))
            turtle.pencolor('purple')
        elif i=='+':
            turtle.write('日',font=('Arial',18,'normal'))
        else:
            draw_digital(i)

        turtle.penup()
        turtle.seth(0)
        turtle.fd(50)



if __name__ == '__main__':
    t=time.gmtime()
    today=time.strftime('%Y-%m=%d+')
    draw_date(today)
    turtle.done()

