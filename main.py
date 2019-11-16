import pygame
import time
import random
import Classes

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = Classes.pad_width  # 게임화면의 가로크기
pad_height = Classes.pad_height  # 게임화면의 세로크기
level_tic = 0
fps = 30
spawn_rate = fps * 7
spawn_cnt = fps * 6
boss_spawn_cnt = 0


def spawn_random_enemy(boss):
    if not boss:
        tmp_num = random.choice([0, 1, 3])
    else:
        tmp_num = 2
    tmp_x = random.choice([0, pad_width - 32])
    tmp_y = random.randrange(0, pad_height - 32)
    Classes.enemies.append(Classes.Enemy(position=[tmp_x, tmp_y], monster_num=tmp_num))


pygame.init()

background = pygame.image.load('img/field2.png')
background.fill((100, 100, 100, 200), None, pygame.BLEND_RGBA_MULT)
screen = pygame.display.set_mode((pad_width, pad_height))
pygame.display.set_caption("Python/Pygame Animation")
clock = pygame.time.Clock()
player = Classes.User((150, 150))

game_over = False
Quit = False

while not Quit:

    while not game_over:
        # 배경
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # 레벨 조정
        level_tic += 1
        if level_tic == fps * 20:
            spawn_rate = fps * 6
        if level_tic == fps * 60:
            spawn_rate = fps * 5
        if level_tic == fps * 180:
            spawn_rate = fps * 4
        if level_tic == fps * 360:
            spawn_rate = fps * 3

        # 이벤트 입력 관리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                Quit = True
            player.handle_event(event)

        # 플레이어 관리
        player.update()

        # enemy 관리
        spawn_cnt += 1
        if spawn_cnt > spawn_rate:
            spawn_cnt = 0
            spawn_random_enemy(boss=False)
        boss_spawn_cnt += 1
        if boss_spawn_cnt > spawn_rate * 15:
            boss_spawn_cnt = 0
            spawn_random_enemy(boss=True)
        for enemy in Classes.enemies:
            enemy.update(player)
            screen.blit(enemy.image, enemy.rect)

        # 공 관리
        for ball in Classes.balls:
            ball.update()
            screen.blit(ball.image, ball.rect)

        # 충돌 이벤트
        # 공 -> 몬스터
        for ball in Classes.balls:
            for enemy in Classes.enemies:
                if pygame.sprite.collide_mask(ball, enemy):
                    ball.hit(enemy)
                    Classes.destroy(ball, enemy)
        # 몬스터 -> 유저
        for enemy in Classes.enemies:
            if not enemy.paralysis and pygame.sprite.collide_rect(enemy, player):
                remain = player.hp - enemy.attack_damage
                if remain > 0:
                    player.hp = remain
                else:
                    player.hp = 0

        # print(player.mp)
        Classes.show_player_state(player, screen, True)
        for enemy in Classes.enemies:
            Classes.show_player_state(enemy, screen, False)

        screen.blit(player.image, player.rect)
        Classes.texting(Classes.score, 40, 40, (255, 10, 10), 24, screen)
        pygame.display.flip()
        clock.tick(fps)

        if player.hp <= 0:
            player.hp = 0
            game_over = True

    Classes.texting("You DEAD!!!!",
                    screen.get_rect().centerx, screen.get_rect().centery , (255, 0, 0), 50, screen)
    Classes.texting("It's time to study now",
                    screen.get_rect().centerx, screen.get_rect().centery + 50, (255, 100, 100), 30, screen)
    Classes.texting("If you want to restart, prees SPACE",
                    screen.get_rect().centerx, screen.get_rect().centery + 100, (50, 50, 50), 18, screen)
    # 이벤트 입력 관리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit = True
        if event.key == pygame.K_SPACE:
            level_tic = 0
            fps = 30
            spawn_rate = fps * 7
            spawn_cnt = fps * 6
            boss_spawn_cnt = 0
            player = Classes.User((150, 150))
            Classes.balls = []
            Classes.enemies = []
            Classes.score = 0
            game_over = False

    pygame.display.flip()
    clock.tick(fps)

pygame.display.flip()
pygame.quit()
