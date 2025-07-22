import pygame

pygame.init()
pygame.mixer.init()

# font = pygame.font.SysFont("comic sans", 35, bold=True)

clock = pygame.time.Clock()

win_res = [800, 600]
fps = 60

window = pygame.display.set_mode(win_res)
pygame.display.set_caption("Two Birds One Stone")

bg_color = (120, 200, 255)
bg_image = pygame.image.load("data/images/background.png")
ground = pygame.image.load("data/images/ground.png").convert_alpha()
ground.set_colorkey((255, 255, 255))
bg_img_2 = pygame.image.load("data/images/background_2.png")
heart_img = pygame.image.load("data/images/heart.png")
heart_img.set_colorkey((255, 255, 255))
title_image = pygame.image.load("data/images/title.png")
title_image.set_colorkey((255, 255, 255))
splash_screen = pygame.image.load("data/images/splash_screen.png")

kill_sound = pygame.mixer.Sound("data/audio/kill.wav")
hit_sound = pygame.mixer.Sound("data/audio/hit.wav")
throw_sound = pygame.mixer.Sound("data/audio/throw.wav")
pass_sound = pygame.mixer.Sound("data/audio/lvl_pass.wav")
explosion_sound = pygame.mixer.Sound("data/audio/explosion.wav")
reset_sound = pygame.mixer.Sound("data/audio/reset.wav")
select_sound = pygame.mixer.Sound("data/audio/select.wav")


class Sling_Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()
        self.image = pygame.image.load("data/images/sling_shot.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel


class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()
        self.image = pygame.image.load("data/images/stone.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel
        self.fired = False

    def update(self):
        if self.fired:
            self.rect.y -= self.vel


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, moving, direction):
        super().__init__()
        self.image = pygame.image.load("data/images/bird.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel
        self.moving = moving
        self.dir = direction

    def update(self):
        if self.moving:
            self.rect.x += self.vel * self.dir
            if self.rect.x <= 100 or self.rect.x + self.rect.width >= 700:
                self.vel = -self.vel


class Current(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()
        self.image = pygame.image.load("data/images/current.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel

    def update(self):
        self.rect.x += self.vel
        if self.rect.x <= 100 or self.rect.x + self.rect.width >= 700:
            self.vel = -self.vel


def lvl_selector(lvl):
    birds = []

    match lvl:
        case 1:
            bird = Bird(365, 85, 2, False, 1)
            birds.append(bird)

        case 2:
            bird = Bird(365, 85, 2, True, 1)
            birds.append(bird)

        case 3:
            bird = Bird(365, 85, 2, True, 1)
            bird2 = Bird(365, 205, 2, True, -1)
            birds.append(bird)
            birds.append(bird2)

        case 4:
            bird = Bird(365, 85, 2, True, 1)
            birds.append(bird)
            bird2 = Bird(610, 205, 2, False, 1)
            birds.append(bird2)

        case 5:
            bird = Bird(550, 85, 2, True, -1)
            bird2 = Bird(550, 205, 2, True, 1)
            bird3 = Bird(250, 85, 2, True, -1)
            bird4 = Bird(250, 205, 2, True, 1)
            birds.append(bird)
            birds.append(bird2)
            birds.append(bird3)
            birds.append(bird4)

        case 6:
            bird = Bird(550, 85, 2, True, 1)
            birds.append(bird)

        case 7:
            bird = Bird(550, 85, 2, True, 1)
            bird3 = Bird(250, 85, 2, True, -1)
            birds.append(bird)
            birds.append(bird3)

    return birds


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("data/images/box.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def box_selector(lvl, sprite_group):
    match lvl:
        case 4:
            box = Box(590, 119)
            sprite_group.add(box)

        case _:
            sprite_group.empty()

    return sprite_group


def current_selector(lvl, sprite_group):
    match lvl:
        case 6:
            current = Current(450, 260, 3)
            current2 = Current(350, 260, 3)
            sprite_group.add(current, current2)

        case 7:
            current = Current(385, 260, 0)
            current2 = Current(350, 260, 0)
            sprite_group.add(current, current2)

        case _:
            sprite_group.remove()

    return sprite_group


def render_text(text, text_color, x, y, win, size):
    font = pygame.font.SysFont("comic sans", size, bold=True)

    # Create a text surface
    text_surface = font.render(text, True, text_color)

    text_width = text_surface.get_width() // 2

    x -= text_width

    # Blit the text surface onto the window
    win.blit(text_surface, (x, y))


def game_loop():
    sling_shot = Sling_Shot(375, 500, 5)
    stone = Stone(387.5, 485, 5)

    lvl = 1

    lives = 3

    throws = 0

    kills = 0

    y = 150
    d = -1
    vel = 0.5

    current_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(sling_shot, stone)
    birds = lvl_selector(lvl)
    for bird in birds:
        all_sprites.add(bird)

    start_button = pygame.Rect(325, 300, 150, 70)
    quit_button = pygame.Rect(325, 380, 150, 70)

    start = True

    splash_time = 60

    main_menu = False
    running = True
    while running:
        if main_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        select_sound.play()
                        main_menu = False
                    if quit_button.collidepoint(event.pos):
                        select_sound.play()
                        running = False
            if y == 150:
                d = -1
            elif y == 140:
                d = 1
            y += vel * d

            window.fill(bg_color)
            pygame.draw.rect(window, (255, 50, 50), start_button)
            pygame.draw.rect(window, (255, 50, 50), quit_button)
            window.blit(title_image, (400 - title_image.get_width()//2, y))
            render_text("start", (255, 255, 255), 400, 293, window, 50)
            render_text("quit", (255, 255, 255), 400, 373, window, 50)

        elif start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            window.blit(splash_screen, (0, 0))
            splash_time -= 1

            if splash_time <= 0:
                main_menu = True
                start = False

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    stone.fired = True
                    throws += 1
                    throw_sound.play()

            x = pygame.mouse.get_pos()[0]  # Get only the x-coordinate of the mouse

            if 120 <= x <= 670:
                sling_shot.rect.x = x - 25

            if not stone.fired:
                stone.rect.x = sling_shot.rect.x + 17.5

            if pygame.sprite.collide_rect(stone, sling_shot) and stone.vel < 0:
                stone.vel = -stone.vel  # Stop the stone when it hits the slingshot
                stone.rect.y = sling_shot.rect.y - 15
                stone.fired = False

                # Reset the stone's position if needed
                if not stone.fired:
                    stone.rect.x = sling_shot.rect.x + 17.5

            for bird in birds.copy():
                if pygame.sprite.collide_rect(stone, bird):
                    bird.kill()
                    birds.remove(bird)
                    kill_sound.play()
                    kills += 1
                    if not birds:
                        stone.rect.y = sling_shot.rect.y - 12.5
                        stone.rect.x = sling_shot.rect.x
                        stone.fired = False
                        lvl += 1
                        current_group.empty()
                        box_group.empty()
                        birds.clear()
                        bird.kill()
                        birds = lvl_selector(lvl)
                        box_group = box_selector(lvl, box_group)
                        current_group = current_selector(lvl, current_group)

            for bird in birds:
                all_sprites.add(bird)

            for bird in birds:
                if lvl == 4:
                    if bird.rect.x + bird.rect.width >= 580 and bird.rect.y == 85:
                        bird.vel = -bird.vel
                if lvl == 5:
                    if bird.rect.x + bird.rect.width == 400 or bird.rect.x == 400:
                        bird.vel = -bird.vel

            if stone.rect.y <= 0 or stone.rect.y + stone.rect.width >= win_res[1]:
                stone.rect.y = sling_shot.rect.y - 12.5
                stone.rect.x = sling_shot.rect.x
                stone.fired = False
                lives -= 1
                reset_sound.play()

                # Clear the old birds
                for bird in birds:
                    bird.kill()
                birds.clear()

                # Add new birds for the current level
                current_group.empty()
                box_group.empty()
                birds.extend(lvl_selector(lvl))
                box_group = box_selector(lvl, box_group)
                current_group = current_selector(lvl, current_group)

            collisions = pygame.sprite.groupcollide(all_sprites, box_group, False, False)

            for stone, box in collisions.items():
                stone.vel = -stone.vel
                hit_sound.play()

            collisions = pygame.sprite.groupcollide(all_sprites, current_group, False, False)

            for stone, current in collisions.items():
                stone.rect.y = sling_shot.rect.y - 12.5
                stone.rect.x = sling_shot.rect.x
                stone.fired = False
                lives -= 1
                explosion_sound.play()

                # Clear the old birds
                for bird in birds:
                    bird.kill()
                birds.clear()

                # Add new birds for the current level
                birds.extend(lvl_selector(lvl))
                current_group.empty()
                box_group.empty()
                box_group = box_selector(lvl, box_group)
                current_group = current_selector(lvl, current_group)

            if lvl == 5 and stone.rect.y <= 55 and stone.rect.x + stone.rect.width >= 530:
                stone.vel = -stone.vel
                hit_sound.play()

            for current in current_group:
                if lvl == 7:
                    for bird in birds:
                        current.rect.centerx = bird.rect.centerx

            window.blit(bg_image, (0, 0))
            if lvl == 5:
                window.blit(bg_img_2, (0, 0))
            window.blit(ground, (0, 40))

            for i in range(lives):
                window.blit(heart_img, (i * 50 + 10, 546))

            if lives <= 0:
                reset_sound.play()
                main_menu = True
                lives = 3
                lvl = 1
                current_group.empty()
                box_group.empty()
                birds.clear()
                birds = lvl_selector(lvl)
                box_group = box_selector(lvl, box_group)
                current_group = current_selector(lvl, current_group)

            all_sprites.draw(window)
            box_group.draw(window)
            current_group.draw(window)

            all_sprites.update()
            box_group.update(window)
            current_group.update()

            render_text("Level " + str(lvl) + " / 10", (0, 0, 0), 400, 0, window, 25)
            render_text("throws: "+str(throws), (0, 0, 0), 400, 560, window, 25)
            render_text("kills "+str(kills), (0, 0, 0), 740, 560, window, 25)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


game_loop()
