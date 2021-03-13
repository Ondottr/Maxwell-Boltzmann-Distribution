import asyncio
import random
import turtle

border = turtle.Turtle()
border.hideturtle()
border.speed(0)
border.pensize(5)
border.up()
border.goto(-250, 250)
border.down()
border.goto(-250, -250)
border.goto(250, -250)
border.goto(250, 250)
border.goto(-250, 250)

window = turtle.Screen()
window.bgcolor('white')
window.tracer(200000)


async def ball_spawn(count):
    for x in range(0, count):
        ball = turtle.Turtle(shape='circle')
        ball.turtlesize(0.3)
        red = random.random()
        green = random.random()
        blue = random.random()
        ball.color(red, green, blue)
        ball.up()
        ball.goto(random.randint(-200, 200), random.randint(-200, 200))

        ball.speedY = 0
        while ball.speedY == 0:
            ball.speedY = random.randint(-5, 5)

        ball.speedX = 0
        while ball.speedX == 0:
            ball.speedX = random.randint(-5, 5)

        ball.angle = 0
        while ball.angle == 0:
            ball.angle = random.randint(-5, 5)

        yield ball


async def ball_refresh(balls):
    for ball in balls:
        yield ball


async def cycle():
    gen = ball_spawn(100)
    balls = [ball async for ball in gen.__aiter__()]
    while True:
        window.update()
        for ball in balls:
            # ball.down()
            ball.goto(ball.xcor() + ball.speedX, ball.ycor() + ball.speedY)

            speedReducing = 0.00001

            ball.speedY = ball.speedY + speedReducing if ball.speedY < 0 else ball.speedY + speedReducing if not ball.speedY > 0 else 0

            ball.speedX = ball.speedX + speedReducing if ball.speedX < 0 else ball.speedX + speedReducing if not ball.speedX > 0 else 0

            if ball.ycor() <= -250:
                ball.sety(-250)
                ball.speedY = -ball.speedY
            if ball.ycor() >= 250:
                ball.sety(250)
                ball.speedY = -ball.speedY

            if ball.xcor() >= 250:
                ball.setx(250)
                ball.speedX = -ball.speedX

            if ball.xcor() <= -250:
                ball.setx(-250)
                ball.speedX = -ball.speedX

            # temp_ball = balls.pop(balls.index(ball))
            async for ball_ in ball_refresh(balls).__aiter__():
                if ball_.xcor() - 5 <= ball.xcor() <= ball_.xcor() + 5 \
                        and ball_.ycor() - 5 <= ball.ycor() <= ball_.ycor() + 5:
                    ball.speedY *= -1
                    ball.speedX *= -1
                    ball_.speedY *= -1
                    ball_.speedX *= -1
                    ball_.left(180)
                    ball.left(180)
            # balls.append(temp_ball)


asyncio.run(cycle())

window.mainloop()
