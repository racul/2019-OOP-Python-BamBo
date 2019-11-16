import pygame
import time
import random
import Classes

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = 710  # 게임화면의 가로크기
pad_height = 550  # 게임화면의 세로크기
spawn_rate = 100
spawn_cnt = 60
level_tic = 0

pygame.init()

background = pygame.image.load('img/field2.png')
background.fill((100, 100, 100, 200), None, pygame.BLEND_RGBA_MULT)
screen = pygame.display.set_mode((pad_width, pad_height))
pygame.display.set_caption("Python/Pygame Animation")
clock = pygame.time.Clock()
player = Classes.User((150, 150))

game_over = False

while game_over == False:
    # 배경
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # 레벨 조정
    level_tic += 1
    if level_tic == 200:
        spawn_rate = 180
    if level_tic == 500:
        spawn_rate = 160
    if level_tic == 800:
        spawn_rate = 120
    if level_tic == 1600:
        spawn_rate = 80

    # 이벤트 입력 관리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        player.handle_event(event)

    # 플레이어 관리
    player.update()

    # enemy 관리
    spawn_cnt += 1
    if spawn_cnt > spawn_rate:
        spawn_cnt = 0
        tmp_num = random.randrange(0, 4)
        tmp_x = random.choice([0, pad_width-32])
        tmp_y = random.randrange(0, pad_height-32)
        Classes.enemies.append(Classes.Enemy(position=[tmp_x, tmp_y], monster_num=tmp_num))
    for enemy in Classes.enemies:
        enemy.update(player)
        screen.blit(enemy.image, enemy.rect)

    # 공 관리
    for ball in Classes.balls:
        ball.update()
        screen.blit(ball.image, ball.rect)

    # 충돌 이벤트
    for ball in Classes.balls:
        ball_type = str(type(ball))[16:-2]
        for enemy in Classes.enemies:
            if pygame.sprite.collide_mask(ball, enemy):
                ball.hit(enemy)

    # print(player.mp)
    Classes.show_player_state(player, screen, True)
    for enemy in Classes.enemies:
        Classes.show_player_state(enemy, screen, False)

    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
