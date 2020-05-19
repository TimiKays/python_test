import turtle as t

t.setup(1000,800)
t.penup()
t.fd(-300)
t.seth(-40)
t.pencolor('tomato')
size=20
t.pensize(size)
t.pendown()
for i in range(4):
    t.circle(50,80)
    t.circle(-50,80)
t.circle(50,40)
t.fd(50)
t.circle(30,180)
while size>1:
    size=size-1
    t.pensize(size)
    t.fd(5)
t.done()