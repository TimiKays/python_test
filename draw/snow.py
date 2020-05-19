import turtle

def draw_side(length,level):
    if level==0:
        turtle.fd(length)
    else:
        for i in (0,60,-120,60):
            turtle.left(i)
            draw_side(length/3,level-1)

if __name__ == '__main__':
    turtle.penup()
    turtle.goto(-100,100)
    turtle.hideturtle()
    turtle.pensize(2)
    length = 300
    # 先固定三角形好了
    level=4
    # angle=180-(level-2)*180/level
    turtle.pendown()
    for i in range(3):
        draw_side(length,level)
        turtle.right(120)
    turtle.done()
