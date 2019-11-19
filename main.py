import pygame
from pygame.locals import *
import time
import random
import Classes

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = Classes.pad_width  # 게임화면의 가로크기
pad_height = Classes.pad_height  # 게임화면의 세로크기
level_tic = 0
level = 1
fps = 30
spawn_rate = fps * 6
spawn_cnt = fps * 6
boss_rate = 15
boss_spawn_cnt = 0
level_times = [0, 20, 60, 180, 300, 420, 520, 600]
spawn_rates = [5, 4, 3, 2.5, 2, 2, 1, 0.8]
boss_rates = [15, 14, 12, 10, 9, 12, 15, 20]
cheat_PO = False
cheat_SP = False
cheat_Hell = False


def spawn_random_enemy(boss):
    if not boss:
        tmp_num = random.choice([0, 1, 3])
    else:
        tmp_num = 2
    tmp_x = random.choice([0, pad_width - 32])
    tmp_y = random.randrange(32, pad_height - 32)
    Classes.enemies.append(Classes.Enemy(position=[tmp_x, tmp_y], monster_num=tmp_num))


def cheating():
    global cheat_PO, cheat_SP, cheat_Hell, level_tic, level
    cheat_on = True
    print("cheat_on")
    cheat_input = ''
    while cheat_on:
        for cheat_key in pygame.event.get():
            if cheat_key.type == KEYDOWN:
                if cheat_key.type == KEYDOWN:
                    if cheat_key.unicode.isalpha():
                        cheat_input += cheat_key.unicode
                    elif cheat_key.key in \
                            [pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]:
                        cheat_input += cheat_key.unicode
                    elif cheat_key.key == K_BACKSPACE:
                        cheat_input = cheat_input[:-1]
                    elif cheat_key.key == K_RETURN:
                        cheat_on = False
    if cheat_input.upper() == 'POWER':
        cheat_PO = not cheat_PO
    if cheat_input.upper() == 'SPEED':
        Classes.cheat_SP = not Classes.cheat_SP
    if cheat_input.upper() == 'MONEY':
        Classes.cheat_MP = not Classes.cheat_MP
    if cheat_input.upper() == 'CHALLENGE':
        cheat_Hell = True
    if cheat_input.upper()[:5] == 'LEVEL' and len(cheat_input) == 6 and \
            cheat_input[5] in ['2', '3', '4', '5', '6', '7', '8']:
        level_tic = level_times[int(cheat_input[5]) - 1] * fps - 10
        level = int(cheat_input[5]) - 1
        print(cheat_input[5])


pygame.init()

background = pygame.image.load('img/field4.png')
background.fill((100, 100, 100, 200), None, pygame.BLEND_RGBA_MULT)
background = pygame.transform.scale(background, (pad_width, pad_height))
screen = pygame.display.set_mode((pad_width, pad_height), FULLSCREEN | HWSURFACE)
# screen = pygame.display.set_mode((pad_width, pad_height))
pygame.display.set_caption("BamBo")
clock = pygame.time.Clock()
player = Classes.User((pad_width/2, pad_height/2))

game_over = False
Quit = False

while not Quit:

    # 배경
    screen.fill((100, 100, 100))
    screen.blit(background, (0, 0))

    while not game_over:
        # 배경
        screen.fill((180, 180, 160))
        screen.blit(background, (0, 0))
        # 스코어 표시
        Classes.textingL('Score : ' + str(Classes.score).zfill(4), 20, 40, (255, 10, 10), 30, screen)
        Classes.textingL('Stage : ' + str(level), 20, 80, (200, 200, 200), 30, screen)
        Classes.texting('  move : wasd', pad_width - 100, 30, (150, 150, 150), 20, screen)
        Classes.texting('attack : jkli', pad_width - 100, 60, (200, 110, 110), 20, screen)
        Classes.texting('hp : ' + str(player.hp).zfill(4), pad_width - 78, pad_height - 60, (200, 100, 100), 20,
                        screen)
        Classes.texting('mp : ' + str(int(player.mp)).zfill(4), pad_width - 80, pad_height - 30, (100, 100, 200), 20,
                        screen)

        # 레벨 조정
        level_tic += 1
        if level_tic == fps * level_times[level]:
            spawn_rate = fps * spawn_rates[level]
            boss_rate = boss_rates[level]
            level += 1
        if cheat_Hell:
            level = 'HELL'
            spawn_rate = fps * 0.2
            boss_rate = 50
            cheat_Hell = False
            level_tic = fps * 6000

        # 이벤트 입력 관리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                Quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    Quit = True
                # 치트
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    cheating()
                        
            player.handle_event(event)

        # 플레이어 관리
        player.update()

        # enemy 스폰 및 업데이트
        spawn_cnt += 1
        if spawn_cnt > spawn_rate:
            spawn_cnt = 0
            spawn_random_enemy(boss=False)
        boss_spawn_cnt += 1
        if boss_spawn_cnt > spawn_rate * boss_rate:
            boss_spawn_cnt = 0
            spawn_random_enemy(boss=True)
        for enemy in Classes.enemies:
            enemy.update(player)
            screen.blit(enemy.image, enemy.rect)

        # 공 관리
        for ball in Classes.balls:
            ball.update()
            screen.blit(ball.image, ball.rect)

        # 충돌 이벤트 (데미지 부여)
        # 공 -> 몬스터
        for ball in Classes.balls:
            for enemy in Classes.enemies:
                if pygame.sprite.collide_mask(ball, enemy):
                    ball.hit(enemy)
                    Classes.destroy(ball, enemy)
        # 몬스터 -> 유저
        if not cheat_PO:
            for enemy in Classes.enemies:
                if not enemy.paralysis and pygame.sprite.collide_rect(enemy, player):
                    remain = player.hp - enemy.attack_damage
                    if remain > 0:
                        player.hp = remain
                    else:
                        player.hp = 0
        # 스텟 나타내기
        Classes.show_player_state(player, screen, True)
        for enemy in Classes.enemies:
            Classes.show_player_state(enemy, screen, False)
        # 맨 위에 사람 그리기
        screen.blit(player.image, player.rect)
        # 화면 생성
        pygame.display.flip()
        # 시간 딜레이
        clock.tick(fps)
        # 게임 종료
        if player.hp <= 0:
            player.hp = 0
            game_over = True

    # 종료 메세지
    Classes.texting("You're DEAD!!!!",
                    screen.get_rect().centerx, screen.get_rect().centery, (255, 0, 0), 60, screen)
    Classes.texting("It's time to study",
                    screen.get_rect().centerx, screen.get_rect().centery + 50, (255, 100, 100), 35, screen)
    Classes.texting("If you want to restart, press SPACE",
                    screen.get_rect().centerx, screen.get_rect().centery + 100, (50, 50, 50), 20, screen)
    # 스코어 표시
    Classes.textingL('Score : ' + str(Classes.score).zfill(4), 20, 40, (255, 10, 10), 30, screen)
    Classes.textingL('Stage : ' + str(level), 20, 80, (200, 200, 200), 30, screen)
    Classes.texting('  move : wasd', pad_width - 100, 30, (150, 150, 150), 20, screen)
    Classes.texting('attack : jkli', pad_width - 100, 60, (200, 110, 110), 20, screen)
    Classes.texting('hp : ' + str(player.hp).zfill(4), pad_width - 78, pad_height - 60, (200, 100, 100), 20,
                    screen)
    Classes.texting('mp : ' + str(int(player.mp)).zfill(4), pad_width - 80, pad_height - 30, (100, 100, 200), 20,
                    screen)
    # 이벤트 입력 관리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Quit = True
            if event.key == pygame.K_SPACE:
                level_tic = 0
                level = 1
                fps = 30
                spawn_rate = fps * 7
                spawn_cnt = fps * 6
                boss_spawn_cnt = 0
                player = Classes.User((pad_width/2, pad_height/2))
                Classes.balls = []
                Classes.enemies = []
                Classes.score = 0
                game_over = False

    pygame.display.flip()
    clock.tick(fps)

pygame.display.flip()
pygame.quit()
