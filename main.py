import pygame
import time
import random
import pygame.font


pygame.init()
pygame.mouse.set_visible(0)

# pygame.mixer.music.load("soundtrack1.mp3")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.2)
win_width = 1000
win_height = 600
font = pygame.font.SysFont(None, 36)

bg_sea = pygame.image.load("sea.jpg")

bg_binocle = pygame.image.load("binocle.png")

bg_sea = pygame.transform.scale(bg_sea, (win_width, win_height))

bg_binocle = pygame.transform.scale(bg_binocle, (win_width, win_height))



clock = pygame.time.Clock()


# CREATING CANVAS
canvas = pygame.display.set_mode((win_width, win_height))

# TITLE OF CANVAS
pygame.display.set_caption("Sea shooter")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(new_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        canvas.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, new_image, x, y, width, height, delay) -> None:
        super().__init__(new_image, x, y, width, height)
        self.shoot_time = time.time()
        self.delay = delay

    def update(self):
        coordinate_x = pygame.mouse.get_pos()[0]
        if coordinate_x <= win_width - 80 and coordinate_x >= 0:
            self.rect.x = coordinate_x
        mouse = pygame.mouse.get_pressed()[0]
        if mouse and (time.time() - self.shoot_time > self.delay):
            self.shoot_time = time.time()
            bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 5))

class Bullet(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()  # Remove the bullet when it goes off the screen

class Enemy(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed

    def update(self):
        global enemies_passed
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            enemies_passed += 1
            self.kill()

class Bonus(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.kill()

def spawn_enemy():
    for _ in range(5):
        enemies.add(Enemy('meteorite.png', random.randint(80, win_width - 80), random.randint(-500, -80), 80, 80, 2))

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

player = Player('com.png', win_width/2, win_height - 200, 150, 80, 0.4)

previous_time = pygame.time.get_ticks()

score = 0

finish = False

paused = True

enemies_passed = 0  # Variable to keep track of enemies passing the last coordinate

game_over_text = ''

bonus_counter_font = pygame.font.SysFont(None, 30)  # Font for bonus counter

exit = False

while not exit:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and not finish:
                paused = not paused  # Toggle the paused state
            if event.key == pygame.K_r and finish:
                player.rect.x = win_width/2
                player.rect.y = win_height - 80
                score = 0
                enemies_passed = 0
                enemies.empty()
                bullets.empty()
                bonuses.empty()
                finish = False
    canvas.blit(bg_sea, (0, 0))

    if not enemies.sprites():
        spawn_enemy()

    if not finish and not paused:
        player.update()
        enemies.update()
        bullets.update()
        bonuses.update()

    collided_list: dict[Bullet, Enemy] = pygame.sprite.groupcollide(bullets, enemies, True, True)
    # if collided_list:
    #     for bullet in collided_list: # each bullet
    #         for enemy in collided_list[bullet]: # each alien that collides with that bullet
    #             bonuses.add(Bonus('bonus.png', enemy.rect.centerx, enemy.rect.y, 40, 40, 2))

    if pygame.sprite.spritecollide(player, bonuses, True):
        score += 1

    if score >= 10:
        game_over_text = font.render("Вітаю! Ти виграв зібравши 10 бонусів", True, (255, 0, 0))
        finish = True

    if enemies_passed >= 3:
        game_over_text = font.render("Ти програв пропустивши 3 ворогів", True, (255, 0, 0))
        finish = True


    player.show()
    enemies.draw(canvas)
    bullets.draw(canvas)
    bonuses.draw(canvas)

    if finish:
        text_rect = game_over_text.get_rect(center=(250, 375))
        canvas.blit(game_over_text, text_rect)
    
    canvas.blit(bonus_counter_font.render(f"Бонусів: {score}/10", True, (255, 255, 255)), (10, 10))
    canvas.blit(bg_binocle, (0, 0))

    pygame.display.update()
    clock.tick(60)



