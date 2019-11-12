import pygame
import time
import random
import Classes

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = 800  # 게임화면의 가로크기
pad_height = 1000  # 게임화면의 세로크기
enemies = []
spawn_rate = 40
spawn_cnt = 30

pygame.init()


screen = pygame.display.set_mode((pad_height, pad_width))
pygame.display.set_caption("Python/Pygame Animation")
clock = pygame.time.Clock()
player = Classes.User((150, 150))

game_over = False

while game_over == False:

    screen.fill(pygame.Color('white'))
    # 이벤트 입력 관리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        player.handle_event(event)

    # 플레이어 관리
    player.update()
    Classes.show_player_state(player, screen)

    # enemy 관리
    spawn_cnt += 1
    if spawn_cnt > spawn_rate:
        spawn_cnt = 0
        tmp_num = random.randrange(0, 4)
        tmp_x = random.choice([0, pad_width])
        tmp_y = random.randrange(0, pad_height)
        enemies.append(Classes.Enemy(position=[tmp_x, tmp_y], monster_num=tmp_num))
    for enemy in enemies:
        enemy.update(player)
        screen.blit(enemy.image, enemy.rect)

    # 공 관리
    for ball in Classes.balls:
        ball.update()
        screen.blit(ball.image, ball.rect)

    # print(player.mp)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
