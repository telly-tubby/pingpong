import pygame, pymunk
import random

pygame.init()

display = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
space = pymunk.Space()
fps = 100
left = 50
right = 950
top = 25
bottom = 575
middlex = 500
middley = 300
game_over = False


def print_text(text, x):
    font = pygame.font.SysFont("Algerian", 20, True, False)
    surface = font.render(text, True, (255,255,255))
    display.blit(surface, (x,5))


class Ball:
    def __init__(self):
        self.body = pymunk.Body()
        self.reset(0, 0, 0)
        self.body.position = middlex, middley
        self.body.velocity = 700, -300
        self.shape =pymunk.Circle(self.body, 8)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        self.shape.collision_type = 1

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(display, (255, 255, 255), (int(x), int(y)), 8)

    def reset(self, space=0, arbiter=0, data=0):
        self.body.position = middlex, middley
        self.body.velocity = -700*random.choice([-1, 1]), 300*random.choice([-1, 1])
        return False

    def vel(self, space=0, arbiter=0, data=0):
        self.body.velocity = self.body.velocity*(750/self.body.velocity.length)


class Wall:
    def __init__(self, p1, p2, col_num=None):
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 8)
        self.shape.elasticity = 1
        space.add(self.shape)
        if col_num:
            self.shape.collision_type = col_num

    def draw(self):
        pygame.draw.line(display, (255, 255, 255), self.shape.a, self.shape.b, 5)


class Player:
    def __init__(self, x):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, middley
        self.shape = pymunk.Segment(self.body, [0, -50], [0, 50], 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        self.shape.collision_type = 100
        self.score = 0

    def draw(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(display, (255, 255, 255), p1,p2, 10)

    def on_edge(self):
        if self.body.local_to_world(self.shape.a).y <= top:
            self.body.velocity = 0, 0
            self.body.position = self.body.position.x, top+50
        if self.body.local_to_world(self.shape.b).y >= bottom:
            self.body.velocity = 0, 0
            self.body.position = self.body.position.x, bottom - 50

    def move(self, up=True):
        if up and self.body.position.y > top:
            self.body.velocity = 0, -800
        elif not up and self.body.position.y < bottom:
            self.body.velocity = 0, 800

    def stop(self):
        self.body.velocity = 0, 0


def game():
    ball = Ball()
    wall_left = Wall([left, top], [left, bottom], 102)
    wall_right = Wall([right, top], [right, bottom], 101)
    wall_top = Wall([left, top], [right, top])
    wall_bottom = Wall([left, bottom], [right, bottom])
    player1 = Player(left+20)
    player2 = Player(right-20)

    scored_1 = space.add_collision_handler(1, 101)
    scored_2 = space.add_collision_handler(1, 102)

    def player1_scored(space, arbiter, data):
        player1.score += 1
        ball.reset()
        return False
    scored_1.begin = player1_scored

    def player2_scored(space, arbiter, data):
        player2.score += 1
        ball.reset()
        return False
    scored_2.begin = player2_scored
    contact_with_player = space.add_collision_handler(1, 100)
    contact_with_player.post_solve = ball.vel
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        keys = pygame.key.get_pressed()
        if not player2.on_edge():
            if keys[273]:
                player2.move()
            elif keys[274]:
                player2.move(False)
            else:
                player2.stop()
        if not player1.on_edge():
            if keys[119]: #w
                player1.move()
            elif keys[115]: #s
                player1.move(False)
            else:
                player1.stop()

        display.fill((0, 0, 0))
        ball.draw()
        wall_left.draw()
        wall_right.draw()
        wall_top.draw()
        wall_bottom.draw()
        player1.draw()
        player2.draw()
        pygame.draw.line(display, (255, 255, 255), [middlex, top], [middlex, bottom], 4)
        print_text(f"Score = {player1.score}", left)
        print_text(f"Score = {player2.score}", right-120)
        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)
game()

pygame.quit()