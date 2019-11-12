import pygame  # pygame 라이브러리 임포트
import random  # random 라이브러리 임포트
from time import sleep

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = 800  # 게임화면의 가로크기
pad_height = 1000  # 게임화면의 세로크기
balls = []
burn_damage = 10
# snowball_img = pygame.image.load("img/ball.png")
# fireball_img = pygame.image.load("img/fireball.png")
# blade_img = pygame.image.load("img/blade.png")
# lightning_img = pygame.image.load("img/lightning.png")


class GameObject:
    def __init__(self, position, width, height):
        self.rect.topleft = position
        self.frame = 0
        self.width = width
        self.height = height
        self.hitbox = (position[0], position[1], width, height)

    def get_frame(self, frame_set):
        # frame_set : 스프래드의 위치를 받아놓은 dict
        # 스프레드의 프레임에 해당하는 위치를 준 다음
        # 프레임을 업데이트 해주는 함수
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        # clipped_rect : 잘라낼 위치를 저장한 데이터
        # 스프레드로 주어진 이미지에서 지금 사용할 이미지를 잘라내주는 함수
        # clipped_rect 가 위치데이터의 dict 면 get_frame 으로
        # 알맞은 위치를 가져온다.
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect


class Enemy(GameObject):
    direction = None  # User 까지 방향 벡터

    def __init__(self, position, monster_num, speed):
        # position : user 를 둘 위치
        # monster_num : monster 종류
        self.sheet = pygame.image.load('img/enemy.png')
        self.sheet.set_clip(pygame.Rect(monster_num + 32, 0, 32, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.event_name = ''
        monster_num *= 32
        super(Enemy, self).__init__(position, 32, 32)

        # 바로 이전 상태 저장 변수
        self.bef_state = 'stand_left'

        # 정보
        self.event_name = ''
        self.attack_motion_number = 0
        self.mp = 600
        self.max_mp = 600
        self.mp_recovery_speed = 5
        self.hp = 1000
        self.max_hp = 1000
        self.hp_recovery_speed = 5
        self.default_speed = speed
        self.speed = speed

        # 이동 모션
        self.down_states = {0: (72, 0, 24, 32),
                            1: (monster_num + 32, 0, 32, 32), 2: (monster_num + 64, 0, 32, 32)}
        self.left_states = {0: (monster_num, 32, 32, 32),
                            1: (monster_num + 32, 32, 32, 32), 2: (monster_num + 64, 32, 32, 32)}
        self.right_states = {0: (monster_num, 64, 32, 32),
                             1: (monster_num + 32, 64, 32, 32), 2: (monster_num + 64, 64, 32, 32)}
        self.up_states = {0: (monster_num, 96, 24, 32),
                          1: (monster_num + 32, 96, 32, 32), 2: (monster_num + 64, 96, 32, 32)}

        # 정지 모션
        self.down_stand = (0, 0, 32, 32)
        self.left_stand = (0, 32, 32, 32)
        self.right_stand = (0, 64, 32, 32)
        self.up_stand = (0, 96, 32, 32)

        # 상태 이상
        self.slow = 0
        self.burned = 0
        self.paralysis = 0
        self.confusion = 0

    def enemy_to_user(self):
        # direction 구하기
        x = player.rect.topleft[0] - self.rect.topleft[0]
        y = player.rect.topleft[1] - self.rect.topleft[1]
        if abs(x) > abs(y):
            if x == 32:
                self.direction = 'stand_right'
            elif x == -32:
                self.direction = 'stand_left'
            elif x > 0:
                self.direction = 'right'
            else:
                self.direction = 'left'
        else:
            if x == 0 and y == 32:
                self.direction = 'stand_down'
            elif x == 0 and y == -32:
                self.direction = 'stand_up'
            elif y > 0:
                self.direction = 'down'
            else:
                self.direction = 'up'
        self.event_name = self.direction

    def update(self):
        # 현재 해당하는 event_name 에 맞추어 event 를 실행하는 함수
        # 이벤트명 설정
        self.enemy_to_user()

        # 상태이상 판정
        if self.slow > 0:
            self.slow -= 1
            self.speed = self.default_speed / 2
        if self.burned > 0:
            self.burned -= 1
            self.hp -= burn_damage
        if self.paralysis > 0:
            self.paralysis -= 1
            return
        if self.confusion > 0:
            self.confusion -= 1
            self.event_name = random.choice(['left', 'right', 'up', 'down'])

        # 이동 이벤트
        if self.event_name == 'left':
            self.clip(self.left_states)
            self.rect.x -= self.speed
        if self.event_name == 'right':
            self.clip(self.right_states)
            self.rect.x += self.speed
        if self.event_name == 'up':
            self.clip(self.up_states)
            self.rect.y -= self.speed
        if self.event_name == 'down':
            self.clip(self.down_states)
            self.rect.y += self.speed

        # 정지 이벤트
        if self.event_name == 'stand_left':
            self.clip(self.left_stand)
        if self.event_name == 'stand_right':
            self.clip(self.right_stand)
        if self.event_name == 'stand_up':
            self.clip(self.up_stand)
        if self.event_name == 'stand_down':
            self.clip(self.down_stand)
        self.image = self.sheet.subsurface(self.sheet.get_clip())


class User(GameObject):
    def __init__(self, position):
        # position : user를 둘 위치
        self.sheet = pygame.image.load('img/Fumiko_1.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 24, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        # 위치, 크기
        self.rect = self.image.get_rect()
        super(User, self).__init__(position, 24, 32)

        # 이동 모션
        self.right_states = {0: (72, 32, 24, 32), 1: (96, 32, 24, 32), 2: (120, 32, 24, 32)}
        self.down_states = {0: (72, 64, 24, 32), 1: (96, 64, 24, 32), 2: (120, 64, 24, 32)}
        self.left_states = {0: (72, 96, 24, 32), 1: (96, 96, 24, 32), 2: (120, 96, 24, 32)}
        self.up_states = {0: (72, 0, 24, 32), 1: (96, 0, 24, 32), 2: (120, 0, 24, 32)}

        # 정지 모션
        self.right_stand = (0, 32, 24, 32)
        self.down_stand = (0, 64, 24, 32)
        self.left_stand = (0, 96, 24, 32)
        self.up_stand = (0, 0, 24, 32)

        # 던지는 모션
        self.throw_up_states = {0: (0, 128, 24, 32), 1: (24, 128, 24, 32), 2: (48, 128, 24, 32),
                                3: (72, 128, 24, 32), 4: (96, 128, 24, 32)}
        self.throw_right_states = {0: (0, 160, 24, 32), 1: (24, 160, 24, 32), 2: (48, 160, 24, 32),
                                   3: (72, 160, 24, 32), 4: (96, 160, 24, 32)}
        self.throw_down_states = {0: (0, 192, 24, 32), 1: (24, 192, 24, 32), 2: (48, 192, 24, 32),
                                  3: (72, 192, 24, 32), 4: (96, 192, 24, 32)}
        self.throw_left_states = {0: (0, 224, 24, 32), 1: (24, 224, 24, 32), 2: (48, 224, 24, 32),
                                  3: (72, 224, 24, 32), 4: (96, 224, 24, 32)}
        
        # 바로 이전 상태 저장 변수
        self.bef_state = 'stand_left'
        
        # 정보
        self.event_name = ''
        self.attack_motion_number = 0
        self.mp = 600
        self.max_mp = 600
        self.mp_recovery_speed = 5
        self.hp = 1000
        self.max_hp = 1000
        self.hp_recovery_speed = 5
        self.speed = 5

    def update(self):
        # 현재 해당하는 event_name 에 맞추어 event 를 실행하는 함수
        # 이동 이벤트
        if self.event_name == 'left':
            self.clip(self.left_states)
            self.rect.x -= self.speed
        if self.event_name == 'right':
            self.clip(self.right_states)
            self.rect.x += self.speed
        if self.event_name == 'up':
            self.clip(self.up_states)
            self.rect.y -= self.speed
        if self.event_name == 'down':
            self.clip(self.down_states)
            self.rect.y += self.speed

        # 공격 이벤트
        if self.event_name[0:6] == 'attack':
            if self.attack_motion_number == 2 and self.check_mp(self.event_name[7:]):
                self.throw(self.event_name[7:])
            if self.bef_state == 'stand_left':
                self.clip(self.throw_left_states)
            if self.bef_state == 'stand_right':
                self.clip(self.throw_right_states)
            if self.bef_state == 'stand_up':
                self.clip(self.throw_up_states)
            if self.bef_state == 'stand_down':
                self.clip(self.throw_down_states)

        # 정지 이벤트
        if self.event_name == 'stand_left': x
            self.clip(self.left_stand)
        if self.event_name == 'stand_right':
            self.clip(self.right_stand)
        if self.event_name == 'stand_up':
            self.clip(self.up_stand)
        if self.event_name == 'stand_down':
            self.clip(self.down_stand)

        if self.event_name[0:6] != 'attack':
            self.attack_motion_number = 0
            if self.event_name[0:5] == 'stand':
                self.bef_state = self.event_name
            else:
                self.bef_state = 'stand_'+self.event_name
        else:
            self.attack_motion_number = (self.attack_motion_number + 1) % 5

        # user mp, hp 업데이트
        if player.mp < player.max_mp:
            player.mp += player.mp_recovery_speed
        if player.hp < player.max_hp:
            player.hp += player.hp_recovery_speed

        # sheet 의 내용을 image 에 저장
        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def check_mp(self, ball_type):
        if ball_type == 'fireball' and self.mp >= 100:
            self.mp -= 100
            return True
        if ball_type == 'blade' and self.mp >= 150:
            self.mp -= 150
            return True
        if ball_type == 'leaf' and self.mp >= 200:
            self.mp -= 200
            return True
        if ball_type == 'dark' and self.mp >= 150:
            self.mp -= 150
            return True
        if ball_type == 'lightning' and self.mp >= 500:
            self.mp -= 500
            return True
        return False

    def throw(self, ball_type):
        if ball_type == 'fireball':
            balls.append(Fireball(self.rect.x, self.rect.y, self.bef_state[6:]))
        if ball_type == 'blade':
            balls.append(Blade(self.rect.x, self.rect.y, self.bef_state[6:]))
        if ball_type == 'leaf':
            balls.append(Leaf(self.rect.x, self.rect.y, self.bef_state[6:]))
        if ball_type == 'dark':
            balls.append(Dark(self.rect.x, self.rect.y, self.bef_state[6:]))
        if ball_type == 'lightning':
            balls.append(Lightning(self.rect.x, 0, self.bef_state[6:]))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.event_name = 'left'
            if event.key == pygame.K_RIGHT:
                self.event_name = 'right'
            if event.key == pygame.K_UP:
                self.event_name = 'up'
            if event.key == pygame.K_DOWN:
                self.event_name = 'down'
            if event.key == pygame.K_f:
                self.event_name = 'attack_fireball'
            if event.key == pygame.K_d:
                self.event_name = 'attack_blade'
            if event.key == pygame.K_s:
                self.event_name = 'attack_leaf'
            if event.key == pygame.K_a:
                self.event_name = 'attack_dark'
            if event.key == pygame.K_t:
                self.event_name = 'attack_lightning'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.event_name = 'stand_left'
            if event.key == pygame.K_RIGHT:
                self.event_name = 'stand_right'
            if event.key == pygame.K_UP:
                self.event_name = 'stand_up'
            if event.key == pygame.K_DOWN:
                self.event_name = 'stand_down'
            if event.key in [pygame.K_f, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_t]:
                if self.bef_state == 'stand_left':
                    self.event_name = 'stand_left'
                if self.bef_state == 'stand_right':
                    self.event_name = 'stand_right'
                if self.bef_state == 'stand_up':
                    self.event_name = 'stand_up'
                if self.bef_state == 'stand_down':
                    self.event_name = 'stand_down'


class Ball(GameObject):
    def __init__(self, x, y, speed, width, height):
        self.speed = speed
        super(Ball, self).__init__([x, y], width, height)

    def update(self):
        if self.vector == 'down':
            self.clip(self.down_states)
            self.rect.y += self.speed
        if self.vector == 'up':
            self.rect.y -= self.speed
            self.clip(self.up_states)
        if self.vector == 'left':
            self.rect.x -= self.speed
            self.clip(self.left_states)
        if self.vector == 'right':
            self.rect.x += self.speed
            self.clip(self.right_states)
        self.image = self.sheet.subsurface(self.sheet.get_clip())


class Fireball(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/fireball.png')
        if vector == 'right' or vector == 'left':
            self.sheet.set_clip(pygame.Rect(0, 0, 75, 40))
            self.height = 40
            self.width = 75
        if vector == 'up' or vector == 'down':
            self.sheet.set_clip(pygame.Rect(0, 0, 40, 75))
            self.height = 75
            self.width = 40
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        if vector == 'up':
            self.rect.topleft = [x - 15, y - 40]
        if vector == 'down':
            self.rect.topleft = [x - 10, y]
        if vector == 'right':
            self.rect.topleft = [x, y]
        if vector == 'left':
            self.rect.topleft = [x - 40, y]
        super(Fireball, self).__init__(x, y, 15, 40, 40)

        # 이동 모션
        self.right_states = {0: (0, 185, 75, 40), 1: (75, 185, 75, 40), 2: (150, 185, 75, 40)}
        self.down_states = {0: (15, 0, 40, 75), 1: (90, 0, 40, 75), 2: (165, 0, 40, 75)}
        self.left_states = {0: (0, 110, 75, 40), 1: (75, 110, 75, 40), 2: (150, 110, 75, 40)}
        self.up_states = {0: (15, 225, 40, 75), 1: (90, 225, 40, 75), 2: (165, 225, 40, 75)}


class Blade(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/blade2.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 100, 100))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        super(Blade, self).__init__(x, y, 15, 100, 100)
        if vector == 'up':
            self.rect.topleft = [x - 33, y - 50]
        if vector == 'down':
            self.rect.topleft = [x - 37, y - 10]
        if vector == 'right':
            self.rect.topleft = [x - 25, y - 30]
        if vector == 'left':
            self.rect.topleft = [x - 60, y - 30]

        # 이동 모션
        self.right_states = {0: (25, 325, 100, 100), 1: (175, 325, 100, 100), 2: (325, 325, 100, 100),
                             3: (475, 325, 100, 100), 4: (625, 325, 100, 100), 5: (475, 325, 100, 100),
                             6: (325, 325, 100, 100)}
        self.down_states = {0: (25, 325, 100, 100), 1: (175, 325, 100, 100), 2: (325, 325, 100, 100),
                            3: (475, 325, 100, 100), 4: (625, 325, 100, 100), 5: (475, 325, 100, 100),
                            6: (325, 325, 100, 100)}
        self.left_states = {0: (25, 325, 100, 100), 1: (175, 325, 100, 100), 2: (325, 325, 100, 100),
                            3: (475, 325, 100, 100), 4: (625, 325, 100, 100), 5: (475, 325, 100, 100),
                            6: (325, 325, 100, 100)}
        self.up_states = {0: (25, 325, 100, 100), 1: (175, 325, 100, 100), 2: (325, 325, 100, 100),
                          3: (475, 325, 100, 100), 4: (625, 325, 100, 100), 5: (475, 325, 100, 100),
                          6: (325, 325, 100, 100)}


class Leaf(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/leaf2.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 100, 100))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        super(Leaf, self).__init__(x, y, 4, 100, 100)
        if vector == 'up':
            self.rect.topleft = [x - 33, y - 50]
        if vector == 'down':
            self.rect.topleft = [x - 37, y - 10]
        if vector == 'right':
            self.rect.topleft = [x - 25, y - 30]
        if vector == 'left':
            self.rect.topleft = [x - 60, y - 30]

        # 이동 모션
        self.right_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                             3: (475, 625, 100, 100)}
        self.down_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                            3: (475, 625, 100, 100)}
        self.left_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                            3: (475, 625, 100, 100)}
        self.up_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                          3: (475, 625, 100, 100)}


class Dark(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/dark2.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 100, 100))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        if vector == 'up':
            self.rect.topleft = [x - 33, y - 50]
        if vector == 'down':
            self.rect.topleft = [x - 37, y - 10]
        if vector == 'right':
            self.rect.topleft = [x - 25, y - 30]
        if vector == 'left':
            self.rect.topleft = [x - 60, y - 30]
        super(Dark, self).__init__(x, y, 10, 100, 100)

        # 이동 모션
        self.right_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                             3: (475, 625, 100, 100)}
        self.down_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                            3: (475, 625, 100, 100)}
        self.left_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                            3: (475, 625, 100, 100)}
        self.up_states = {0: (325, 625, 100, 100), 1: (475, 625, 100, 100), 2: (625, 625, 100, 100),
                          3: (475, 625, 100, 100)}


class Lightning(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/lightning2.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 273, 566))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        if vector == 'right':
            self.rect.topleft = [x - 50, y]
        if vector == 'left':
            self.rect.topleft = [x - 200, y]
        super(Lightning, self).__init__(x, y, 10, 100, 100)

        # 이동 모션
        self.right_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                             3: (13, 590, 241, 490)}
        self.down_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                             3: (13, 590, 241, 490)}
        self.left_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                             3: (13, 590, 241, 490)}
        self.up_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                             3: (13, 590, 241, 490)}


def texting(arg, x, y, color):
    font = pygame.font.Font('freesansbold.ttf', 24)
    if color == 'blue':
        text = font.render("MP: " + str(arg).zfill(4), True, (0, 0, 255))  # zfill : 앞자리를 0으로 채움
    elif color == 'red':
        text = font.render("HP: " + str(arg).zfill(4), True, (255, 0, 0))  # zfill : 앞자리를 0으로 채움
    else:
        text = font.render("SC: " + str(arg).zfill(4), True, (0, 0, 0))  # zfill : 앞자리를 0으로 채움

    text_rect = text.get_rect()  # 텍스트 객체를 출력위치에 가져옴
    text_rect.centerx = x    # 출력할 때의 x 좌표를 설정한다
    text_rect.centery = y
    screen.blit(text, text_rect) # 화면에 텍스트객체를 그린다.


def show_player_state():
    texting(player.hp, 100, 50, 'red')
    texting(player.mp, 100, 80, 'blue')

pygame.init()


screen = pygame.display.set_mode((pad_height, pad_width))
pygame.display.set_caption("Python/Pygame Animation")
clock = pygame.time.Clock()
player = User((150, 150))

game_over = False

while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        player.handle_event(event)

    player.update()
    screen.fill(pygame.Color('white'))
    show_player_state()

    # 공 처리
    for ball in balls:
        ball.update()
        screen.blit(ball.image, ball.rect)
        if ball.rect.x > pad_width + 200 or ball.rect.x < -200 or ball.rect.y > pad_height + 200 or ball.rect.y < -200:
            balls.remove(ball)


    print(player.mp)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
