import pygame
import os
import random

pygame.init()

pygame.display.set_caption("Pangpang by Siwon")
clock = pygame.time.Clock()
imagePath = os.path.join(os.path.dirname(__file__), "img")
bgImages = ["background1.png", "background2.jpg"]
stopGame = False
level = 1

def Game():
    global stopGame
    global level
    
    background = pygame.image.load(os.path.join(imagePath, bgImages[random.randint(0, len(bgImages) - 1)]))
    screen_width = background.get_width()
    screen_height = background.get_height()
    screen = pygame.display.set_mode((screen_width, screen_height))

    stage = pygame.image.load(os.path.join(imagePath, "stage.png"))
    stage_width = stage.get_width()   
    stage_height = stage.get_height()

    characters = {"left": [
        pygame.image.load(os.path.join(imagePath, "character.png")),
        pygame.image.load(os.path.join(imagePath, "character1.png")),
        pygame.image.load(os.path.join(imagePath, "character.png")),
        pygame.image.load(os.path.join(imagePath, "character2.png"))
    ]}
    characters["right"] = [pygame.transform.flip(char, True, False) for char in characters["left"]]
    character = characters["left"][0]
    character_width = character.get_width()
    character_height = character.get_height()
    character_x_pos = (screen_width - character_width) / 2
    character_y_pos = screen_height - stage_height - character_height
    character_to_x = 0
    character_speed = 0.5
    character_animation_speed = 1

    weapon = pygame.image.load(os.path.join(imagePath, "weapon.png"))
    weapon_width = weapon.get_width()
    weapons = []
    weapon_speed = 10

    ball_images = [
                pygame.image.load(os.path.join(imagePath, "balloon1.png")),
                pygame.image.load(os.path.join(imagePath, "balloon2.png")),
                pygame.image.load(os.path.join(imagePath, "balloon3.png")),
                pygame.image.load(os.path.join(imagePath, "balloon4.png"))
                ]
    ball_speed_y = [-21, -18, -15, -12]
    balls = []
    for i in range(0, level):
        balls.append({
            "pos_x" : random.randint(0, screen_width - 160),
            "pos_y" : 50,
            "img_idx" : 0,
            "to_x" : 3 * (random.randint(0, 1) * -2 + 1),
            "to_y" : -6,
            "init_spd_y" : ball_speed_y[0]
        })

    running = True
    isCharLeft = True
    isMoving = False
    tick = 0
    tickIdx = 0 
    weapon_to_remove = -1
    ball_to_remove = -1
    game_result = "Game Over"
    total_time = 100
    game_font = pygame.font.Font(None, 40)
    start_ticks = pygame.time.get_ticks()

    while running:
        dt = clock.tick(40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                isMoving = True
                if event.key == pygame.K_LEFT:
                    character_to_x -= character_speed
                    if not isCharLeft:
                        isCharLeft = True
                if event.key == pygame.K_RIGHT:
                    character_to_x += character_speed
                    if isCharLeft:
                        isCharLeft = False
                if event.key == pygame.K_SPACE:
                    weapon_x_pos = character_x_pos + ((character_width + weapon_width) / 2)
                    weapon_y_pos = character_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])

                if event.key == pygame.K_ESCAPE:
                    running = False
                    stopGame = True

            if event.type == pygame.KEYUP:
                isMoving = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_to_x = 0
        if isMoving:
            tick = (tick + 1) % (4 * character_animation_speed)
            tickIdx = tick // character_animation_speed
        character_x_pos += character_to_x * dt

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        weapons = [ [w[0], w[1] - weapon_speed] for w in weapons ]
        weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0 ]
        
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_size = ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"] = ball_val["to_x"] * -1
            if ball_pos_y >= screen_height - stage_height - ball_height:
                ball_val["to_y"] = ball_val["init_spd_y"]
            else:
                ball_val["to_y"] += 0.4

            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

    ## collision ##

        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos 
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y
            if character_rect.colliderect(ball_rect):
                running = False
                stopGame = False
                level = 0
                break

            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_val[0]
                weapon_rect.top = weapon_val[1]
                if weapon_rect.colliderect(ball_rect):
                    weapon_to_remove = weapon_idx
                    ball_to_remove = ball_idx

                    if ball_img_idx < 3:
                        ball_width = ball_rect.size[0]
                        ball_height = ball_rect.size[1]

                        small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                        small_ball_width = small_ball_rect.size[0]
                        small_ball_height = small_ball_rect.size[1]

                        balls.append({
                            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            "img_idx" : ball_img_idx + 1,
                            "to_x" : -3,
                            "to_y" : -6,
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]
                        })
                        balls.append({
                            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            "img_idx" : ball_img_idx + 1,
                            "to_x" : 3,
                            "to_y" : -6,
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]
                        })
                    break
            else:
                continue
            break

        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1
        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1

        if len(balls) == 0:
            game_result = "Mission Complete"
            running = False

    ## draw ##

        screen.blit(background, (0, 0))
        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

        for ball in balls:
            screen.blit(ball_images[ball["img_idx"]], (ball["pos_x"], ball["pos_y"]))

        screen.blit(stage, (0, screen_height - stage_height))
        character = characters["left"][tickIdx] if isCharLeft else characters["right"][tickIdx]
        screen.blit(character, (character_x_pos, character_y_pos))

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (0, 0, 0))
        screen.blit(timer, (10, 10))

        if total_time - elapsed_time <= 0:
            game_result = "Time Over"
            running = False
            stopGame = True
        pygame.display.update()

    gameover = pygame.font.Font(None, 80)
    msg = gameover.render(game_result, True, (255, 0, 0))
    msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()

    pygame.time.delay(1000)


while not stopGame:
    Game()
    level += 1
pygame.quit()