import pygame
import random


class Fish(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('background.png')
        self.WIN_WIDTH = 640
        self.WIN_HEIGHT = 472
        self.x = 100
        self.y = 85
        self.line = pygame.math.Vector2
        img1 = pygame.image.load('img1.png')
        img2 = pygame.image.load('img2.png')
        img3 = pygame.image.load('img3.png')
        img4 = pygame.image.load('img4.png')
        self.lst_imgs = [img1, img2, img3, img4]
        self.image = self.lst_imgs[0]
        self.image = pygame.transform.scale(self.image, (self.x, self.y))
        self.rect = self.image.get_rect()
        self.rect.center = (self.WIN_WIDTH / 2, self.WIN_HEIGHT / 2)
        self.first_vector = self.line(0, 0)
        self.second_vector = self.line(0, 0)
        self.position = self.line(self.rect.center)

    def update(self):
        self.first_vector = self.line(0, 0)
        self.second_vector = self.line(0, 2)
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_SPACE]:
            self.second_vector.y =- 1.5
        else:
            self.image = self.lst_imgs[0]
            self.image = pygame.transform.scale(self.image, (self.x, self.y))
        self.first_vector += self.second_vector
        self.position += self.first_vector + self.second_vector / 2
        if self.position.y <= 0 + 0.5 * self.rect.width:
            self.position.y = 0 + 0.5 * self.rect.width
        if self.position.y >= self.WIN_HEIGHT - 0.5 * self.rect.width:
            self.position.y = self.WIN_HEIGHT - 0.5 * self.rect.width
        self.rect.center = self.position


class BarrierTop(pygame.sprite.Sprite):

    def __init__(self, r, top):
        super().__init__()
        self.WIN_HEIGHT = 472
        h = 80
        self.image = pygame.image.load('BarrierTop.png')
        self.image = pygame.transform.scale(self.image, (h, top))
        self.rect = self.image.get_rect()
        self.rect.x = r
        self.rect.y = 0

    def update(self):
        self.rect.x -= 2


class BarrierBot(pygame.sprite.Sprite):

    def __init__(self, r, bot):
        super().__init__()
        self.WIN_HEIGHT = 472
        h = 80
        self.image = pygame.image.load('BarrierBot.png')
        self.image = pygame.transform.scale(self.image, (h, bot))
        self.rect = self.image.get_rect()
        self.rect.x = r
        self.rect.y = self.WIN_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 2

class Game(Fish):

    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('background.png')
        self.garden = self.background.get_width()
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.WIN_WIDTH = 640
        self.WIN_HEIGHT = 472
        self.display = pygame.display.set_mode([self.WIN_WIDTH, self.WIN_HEIGHT])
        self.line = pygame.math.Vector2
        self.top = 175
        self.bot = 175
        self.dx = 0
        self.r = 650
        self.score = 0

    def barrier(self):
        r = random.randint(620, 650)
        a = []
        for i in range(60, 300, 15):
            a.append(i)
        b = random.choice(a)
        lst = [b, 360 - b]
        hieght_top = lst[0]
        hieght_bot = lst[1]
        self.top_barrier = BarrierTop(r, hieght_top)
        self.top_barriers = pygame.sprite.Group()
        self.top_barriers.add(self.top_barrier)
        self.all_s.add(self.top_barrier)
        self.bot_barrier = BarrierBot(r, hieght_bot)
        self.bot_barriers = pygame.sprite.Group()
        self.bot_barriers.add(self.bot_barrier)
        self.all_s.add(self.bot_barrier)

    def renovate(self):
        self.fish = Fish()
        self.all_s = pygame.sprite.Group()
        self.all_s.add(self.fish)
        self.top_barrier = BarrierTop(self.r, self.top)
        self.top_barriers = pygame.sprite.Group()
        self.top_barriers.add(self.top_barrier)
        self.all_s.add(self.top_barrier)
        self.bot_barrier = BarrierBot(self.r, self.bot)
        self.bot_barriers = pygame.sprite.Group()
        self.bot_barriers.add(self.bot_barrier)
        self.all_s.add(self.bot_barrier)
        self.score = 0

    def text(self, text, x, y, color, size):
        self.font = pygame.font.SysFont('comicsansms', size, bold=2)
        text = self.font.render(text, 1, color)
        textrect = text.get_rect()
        textrect.center = (x / 2, y / 2)
        self.display.blit(text, textrect.center)

    def game_over(self):
        over = True
        while over:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        over = False
            self.text("Вы проиграли!", self.WIN_WIDTH - 150, self.WIN_HEIGHT - 100, self.red, 30)
            self.text("Жми Enter, чтобы попробовать заново!", self.WIN_WIDTH - 400, self.WIN_HEIGHT + 100, self.black, 20)
            pygame.display.flip()
        self.renovate()

    def scores(self):
        self.text("Счёт:" + str(self.score), self.WIN_WIDTH - 50, 100, self.white, 30)

    def new(self):
        self.all_s.update()
        bot = pygame.sprite.spritecollide(self.fish, self.bot_barriers, False, pygame.sprite.collide_mask)
        top = pygame.sprite.spritecollide(self.fish, self.top_barriers, False, pygame.sprite.collide_mask)
        if bot or top:
            self.game_over()
        ddx = self.dx % self.garden + 5
        dy = ddx - self.garden + 3
        self.display.blit(self.background, (dy, 0))
        if ddx < self.WIN_WIDTH:
            self.display.blit(self.background, (ddx, 0))
        self.dx -= 2
        if self.bot_barrier.rect.x < self.WIN_WIDTH * 0.5 and self.top_barrier.rect.x < self.WIN_WIDTH * 0.5:
            self.barrier()
            self.score += 1
        else:
            self.score += 0

    def print(self):
        self.all_s.draw(self.display)
        self.scores()

    def go(self):
        for e in pygame.event.get():
            self.clock.tick(60)
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

    def play(self):
        while True:
            self.go()
            self.new()
            self.print()
            pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption('My Game')
    play = Game()
    while play.play:
        play.renovate()
        play.play()


if __name__ == '__main__':
    main()