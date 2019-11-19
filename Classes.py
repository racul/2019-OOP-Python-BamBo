import pygame  # pygame 라이브러리 임포트
import random  # random 라이브러리 임포트

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = 1280  # 게임화면의 가로크기
pad_height = 720  # 게임화면의 세로크기
balls = []
enemies = []
score = 0
cheat_MP = False
cheat_SP = False


class GameObject(pygame.sprite.Sprite):
    rect = pygame.Rect
    vector = ''
    down_states = {}
    left_states = {}
    right_states = {}
    up_states = {}
    sheet = pygame.image
    reset_frame = 0
    mask = pygame.Mask

    def __init__(self, position, width, height):
        pygame.sprite.Sprite.__init__(self)
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
            self.frame = self.reset_frame
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
    detect_rate = 10
    detect_cnt = 9

    def __init__(self, position, monster_num):
        # position : user 를 둘 위치
        # monster_num : monster 종류 0, 1, 2, 3

        # 정보
        self.monster_num = monster_num
        self.id = monster_num * 96
        self.tic = 0
        self.event_name = ''
        self.attack_motion_number = 0
        if monster_num == 0:    # 초록이
            self.default_speed = 10
            self.speed = 10
            self.hp = 1000
            self.max_hp = 1000
            self.hp_recovery_speed = 0
            self.attack_damage = 20
        if monster_num == 1:    # 하양이
            self.default_speed = 5
            self.speed = 5
            self.hp = 2000
            self.max_hp = 2000
            self.hp_recovery_speed = 20
            self.attack_damage = 40
        if monster_num == 2:    # 파랑이
            self.default_speed = 5
            self.speed = 5
            self.hp = 8000
            self.max_hp = 8000
            self.hp_recovery_speed = 8
            self.attack_damage = 5
        if monster_num == 3:    # 검댕이
            self.default_speed = 15
            self.speed = 15
            self.hp = 100
            self.max_hp = 100
            self.hp_recovery_speed = 0
            self.attack_damage = 10

        self.sheet = pygame.image.load('img/enemy.png')
        self.sheet.set_clip(pygame.Rect(self.id, 0, 32, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.event_name = ''
        super(Enemy, self).__init__(position, 32, 32)

        # 바로 이전 상태 저장 변수
        self.bef_state = 'stand_left'

        # 이동 모션
        self.down_states = {0: (self.id, 0, 32, 32),
                            1: (self.id + 32, 0, 32, 32), 2: (self.id + 64, 0, 32, 32)}
        self.left_states = {0: (self.id, 32, 32, 32),
                            1: (self.id + 32, 32, 32, 32), 2: (self.id + 64, 32, 32, 32)}
        self.right_states = {0: (self.id, 64, 32, 32),
                             1: (self.id + 32, 64, 32, 32), 2: (self.id + 64, 64, 32, 32)}
        self.up_states = {0: (self.id, 96, 32, 32),
                          1: (self.id + 32, 96, 32, 32), 2: (self.id + 64, 96, 32, 32)}

        # 정지 모션
        self.down_stand = (self.id, 0, 32, 32)
        self.left_stand = (self.id, 32, 32, 32)
        self.right_stand = (self.id, 64, 32, 32)
        self.up_stand = (self.id, 96, 32, 32)

        # 상태 이상
        self.slow = 0       # leaf
        self.burned = 0     # fireball
        self.paralysis = 0  # blade
        self.confusion = 0  # dark

    def enemy_to_user(self, player):
        # direction 구하기
        self.detect_cnt += 1
        if self.detect_rate > self.detect_cnt:
            return
        self.detect_cnt = 0

        x = player.rect.topleft[0] - self.rect.topleft[0]
        y = player.rect.topleft[1] - self.rect.topleft[1]
        if abs(x) > abs(y):
            if 0 < x <= 26:
                self.direction = 'stand_right'
            elif 0 > x > -26:
                self.direction = 'stand_left'
            elif x > 0:
                self.direction = 'right'
            else:
                self.direction = 'left'
        else:
            if -26 < x < 26 and 0 < y <= 26:
                self.direction = 'stand_down'
            elif -26 < x < 26 and 0 > y >= -26:
                self.direction = 'stand_up'
            elif y > 0:
                self.direction = 'down'
            else:
                self.direction = 'up'
        self.event_name = self.direction

    def update(self, player):
        # 현재 해당하는 event_name 에 맞추어 event 를 실행하는 함수
        # 사망 이벤트
        if self.hp <= 0:
            global score
            enemies.remove(self)
            score += 5
            player.mp += 20

        # 이벤트명 설정 (이동 상태)
        self.enemy_to_user(player)

        # 상태이상 판정
        if self.slow > 0:
            self.slow -= 1
            self.speed = self.default_speed / 4
        else:
            self.speed = self.default_speed
        if self.burned > 0:
            self.burned -= 1
            self.hp -= self.max_hp / 500
        if self.paralysis > 0:
            self.paralysis -= 1
            return
        if self.confusion > 0:
            self.confusion -= 1
            self.event_name = random.choice(['left', 'right', 'up', 'down'])

        # tic 계산
        self.tic += 1
        if 30 / self.speed > self.tic:
            return
        self.tic = 0

        # 체력 회복
        if self.hp < self.max_hp:
            self.hp += self.hp_recovery_speed

        # 이동 이벤트
        if self.event_name == 'left':
            self.clip(self.left_states)
            self.rect.x -= 4
        if self.event_name == 'right':
            self.clip(self.right_states)
            self.rect.x += 4
        if self.event_name == 'up':
            self.clip(self.up_states)
            self.rect.y -= 4
        if self.event_name == 'down':
            self.clip(self.down_states)
            self.rect.y += 4

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
        self.mask = pygame.mask.from_surface(self.image)


class User(GameObject):
    def __init__(self, position):
        # position : use r를 둘 위치
        self.sheet = pygame.image.load('img/Fumiko_1.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 0, 24, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.mask = pygame.mask.from_surface(self.image)
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
        self.bef_state = 'stand_down'
        self.bef_attack = ''
        self.move_state = {'down' : False, 'up' : False, 'left' : False, 'right' : False}

        # 정보
        self.event_name = 'stand_down'
        self.attack_motion_number = 0
        self.mp = 800
        self.max_mp = 800
        self.mp_recovery_speed = 1.2
        self.hp = 1000
        self.max_hp = 1000
        self.hp_recovery_speed = 1
        self.speed = 20
        self.tic = 0
        # 상태 이상
        self.slow = 0  # leaf
        self.burned = 0  # fireball
        self.paralysis = 0  # blade
        self.confusion = 0  # dark

    def update(self):
        # 현재 해당하는 event_name 에 맞추어 event 를 실행하는 함수
        # tic 계산
        if not cheat_SP:
            self.tic += 1
            if 30 / self.speed > self.tic:
                return
            self.tic = 0

        # 이동 이벤트
        if self.event_name == 'left':
            self.clip(self.left_states)
            if self.rect.x > 5:
                self.rect.x -= 5
        if self.event_name == 'right':
            self.clip(self.right_states)
            if self.rect.x < pad_width - 28:
                self.rect.x += 5
        if self.event_name == 'up':
            self.clip(self.up_states)
            if self.rect.y > 5:
                self.rect.y -= 5
        if self.event_name == 'down':
            self.clip(self.down_states)
            if self.rect.y < pad_height - 34:
                self.rect.y += 5

        # 정지 이벤트
        if self.event_name == 'stand_left':
            self.clip(self.left_stand)
        if self.event_name == 'stand_right':
            self.clip(self.right_stand)
        if self.event_name == 'stand_up':
            self.clip(self.up_stand)
        if self.event_name == 'stand_down':
            self.clip(self.down_stand)

        # 공격 이벤트
        if 0 < self.attack_motion_number:
            # 던지는 모션이 시작되었고, 마나가 충분하면 던진다
            if self.attack_motion_number == 2 and self.check_mp(self.bef_attack):
                self.throw(self.bef_attack)
            if self.bef_state == 'stand_left':
                self.clip(self.throw_left_states)
            if self.bef_state == 'stand_right':
                self.clip(self.throw_right_states)
            if self.bef_state == 'stand_up':
                self.clip(self.throw_up_states)
            if self.bef_state == 'stand_down':
                self.clip(self.throw_down_states)

        if self.event_name[0:6] == 'attack':
            # 공격 상태 저장
            self.bef_attack = self.event_name[7:]

        if self.event_name[0:6] != 'attack' and self.attack_motion_number == 0:
            # 현재 어택 상태가 아니면 상태 초기화
            if self.event_name[0:5] == 'stand':
                self.bef_state = self.event_name
                self.frame = 0
            else:
                self.bef_state = 'stand_' + self.event_name
        else:
            self.attack_motion_number = (self.attack_motion_number + 1) % 5

        # user mp, hp 업데이트
        if self.mp < self.max_mp:
            self.mp += self.mp_recovery_speed
        if self.hp < self.max_hp:
            self.hp += self.hp_recovery_speed
        if cheat_MP:
            self.mp = self.max_mp

        # sheet 의 내용을 image 에 저장
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.mask = pygame.mask.from_surface(self.image)

    def check_mp(self, ball_type):
        if ball_type == 'fireball' and self.mp >= 20:
            self.mp -= 20
            return True
        if ball_type == 'blade' and self.mp >= 80:
            self.mp -= 80
            return True
        if ball_type == 'leaf' and self.mp >= 150:
            self.mp -= 150
            return True
        if ball_type == 'dark' and self.mp >= 110:
            self.mp -= 110
            return True
        if ball_type == 'lightning' and self.mp >= 500:
            self.mp -= 500
            return True
        return False

    def throw(self, ball_type):
        # 공 던지기 함수
        # 공의 종류에 맞추어 balls 리스트에 공을 추가한다.
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

    def find_move(self):
        for move_event in ['down', 'up', 'left', 'right']:
            if self.move_state[move_event]:
                return move_event
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.event_name = 'left'
                self.move_state[self.event_name] = True
            if event.key == pygame.K_d:
                self.event_name = 'right'
                self.move_state[self.event_name] = True
            if event.key == pygame.K_w:
                self.event_name = 'up'
                self.move_state[self.event_name] = True
            if event.key == pygame.K_s:
                self.event_name = 'down'
                self.move_state[self.event_name] = True
            if event.key == pygame.K_j:
                self.event_name = 'attack_fireball'
            if event.key == pygame.K_k:
                self.event_name = 'attack_blade'
            if event.key == pygame.K_l:
                self.event_name = 'attack_leaf'
            if event.key == pygame.K_i:
                self.event_name = 'attack_dark'
            # if event.key == pygame.K_t:
            #     self.event_name = 'attack_lightning'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.event_name = 'stand_left'
                self.move_state['left'] = False
            if event.key == pygame.K_d:
                self.event_name = 'stand_right'
                self.move_state['right'] = False
            if event.key == pygame.K_w:
                self.event_name = 'stand_up'
                self.move_state['up'] = False
            if event.key == pygame.K_s:
                self.event_name = 'stand_down'
                self.move_state['down'] = False
            if event.key in [pygame.K_j, pygame.K_k, pygame.K_i, pygame.K_l, pygame.K_t]:
                if self.bef_state == 'stand_left':
                    self.event_name = 'stand_left'
                if self.bef_state == 'stand_right':
                    self.event_name = 'stand_right'
                if self.bef_state == 'stand_up':
                    self.event_name = 'stand_up'
                if self.bef_state == 'stand_down':
                    self.event_name = 'stand_down'
            if self.find_move():
                self.event_name = self.find_move()


class Ball(GameObject):
    damage = 0
    slow = 0
    burned = 0
    paralysis = 0
    confusion = 0

    def __init__(self, x, y, speed, width, height, class_name):
        self.speed = speed
        super(Ball, self).__init__([x, y], width, height)
        self.tic = 0
        self.destroyer = 2000
        self.class_name = class_name

    def hit(self, enemy):
        enemy.hp -= self.damage
        enemy.slow = max(self.slow, enemy.slow)
        enemy.burned = max(enemy.burned, self.burned)
        enemy.paralysis = max(enemy.paralysis, self.paralysis)
        enemy.confusion = max(enemy.confusion, self.confusion)

    def update(self):
        # 파괴
        self.destroyer -= 1
        if self.destroyer <= 0:
            balls.remove(self)

        # tic 계산
        self.tic += 1
        if 3 > self.tic:
            return
        self.tic = 0

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
        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.x > pad_width + 200 or self.rect.x < -200 or self.rect.y > pad_height + 200 or self.rect.y < -200:
            balls.remove(self)


class Fireball(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/fireball.png').convert_alpha()
        if vector == 'right' or vector == 'left':
            self.sheet.set_clip(pygame.Rect(0, 0, 75, 40))
            self.height = 40
            self.width = 75
        if vector == 'up' or vector == 'down':
            self.sheet.set_clip(pygame.Rect(0, 0, 40, 75))
            self.height = 75
            self.width = 40
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        super(Fireball, self).__init__(x, y, 15, 40, 40, 'Fireball')
        if vector == 'up':
            self.rect.topleft = [x - 15, y - 40]
        if vector == 'down':
            self.rect.topleft = [x - 10, y]
        if vector == 'right':
            self.rect.topleft = [x, y]
        if vector == 'left':
            self.rect.topleft = [x - 40, y]

        # 이동 모션
        self.right_states = {0: (0, 185, 75, 40), 1: (75, 185, 75, 40), 2: (150, 185, 75, 40)}
        self.down_states = {0: (15, 0, 40, 75), 1: (90, 0, 40, 75), 2: (165, 0, 40, 75)}
        self.left_states = {0: (0, 110, 75, 40), 1: (75, 110, 75, 40), 2: (150, 110, 75, 40)}
        self.up_states = {0: (15, 225, 40, 75), 1: (90, 225, 40, 75), 2: (165, 225, 40, 75)}

        # 정보
        self.damage = 20
        self.slow = 0       # leaf
        self.burned = 500   # fireball
        self.paralysis = 0  # blade
        self.confusion = 0  # dark


class Blade(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/blade2.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 0, 100, 100))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        super(Blade, self).__init__(x, y, 15, 100, 100, 'Blade')
        if vector == 'up':
            self.rect.topleft = [x - 33, y - 50]
        if vector == 'down':
            self.rect.topleft = [x - 37, y - 10]
        if vector == 'right':
            self.rect.topleft = [x - 25, y - 30]
        if vector == 'left':
            self.rect.topleft = [x - 60, y - 30]
        self.reset_frame = 3

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
        # 정보
        self.damage = 900
        self.slow = 0  # leaf
        self.burned = 0  # fireball
        self.paralysis = 100  # blade
        self.confusion = 0  # dark


class Leaf(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/leaf2.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(325, 625, 100, 100))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        super(Leaf, self).__init__(x, y, 4, 100, 100, 'Leaf')
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

        # 정보
        self.damage = 5
        self.slow = 60  # leaf
        self.burned = 0  # fireball
        self.paralysis = 0  # blade
        self.confusion = 0  # dark


class Dark(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/dark2.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 0, 100, 100))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        super(Dark, self).__init__(x, y, 10, 100, 100, 'Dark')
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

        # 정보
        self.damage = 60
        self.slow = 0  # leaf
        self.burned = 0  # fireball
        self.paralysis = 0  # blade
        self.confusion = 50  # dark


class Lightning(Ball):
    def __init__(self, x, y, vector):
        self.vector = vector
        self.sheet = pygame.image.load('img/lightning2.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 0, 273, 566))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        super(Lightning, self).__init__(x, y, 10, 100, 100, 'Lightning')
        if vector == 'right':
            self.rect.topleft = [x - 50, y]
        if vector == 'left':
            self.rect.topleft = [x - 200, y]

        # 이동 모션
        self.right_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                             3: (13, 590, 241, 490)}
        self.down_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                            3: (13, 590, 241, 490)}
        self.left_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                            3: (13, 590, 241, 490)}
        self.up_states = {0: (534, 590, 241, 490), 1: (13, 71, 241, 490), 2: (534, 71, 241, 490),
                          3: (13, 590, 241, 490)}


def destroy(ball, enemy):
    if enemy.monster_num == 2:
        ball.destroyer -= 500
    if ball.class_name == 'Blade':
        ball.destroyer -= 1000


def texting(arg, x, y, color, font_size, screen):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(str(arg), True, color)  # zfill : 앞자리를 0으로 채움

    text_rect = text.get_rect()  # 텍스트 객체를 출력위치에 가져옴
    text_rect.centerx = x  # 출력할 때의 x 좌표를 설정한다
    text_rect.centery = y
    screen.blit(text, text_rect)  # 화면에 텍스트객체를 그린다.


def textingL(arg, x, y, color, font_size, screen):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(str(arg), True, color)  # zfill : 앞자리를 0으로 채움

    text_rect = text.get_rect()  # 텍스트 객체를 출력위치에 가져옴
    text_rect.x = x  # 출력할 때의 x 좌표를 설정한다
    text_rect.y = y
    screen.blit(text, text_rect)  # 화면에 텍스트객체를 그린다.


def show_player_state(player, screen, mp_t):
    # texting(player.hp, 100, 50, 'red', screen)
    # texting(player.mp, 100, 80, 'blue', screen)
    if mp_t:
        # mp 가 존재하는 존재라면
        up = 20
        hp_color = (255, 0, 0)
    else:
        up = 10
        if player.burned > 0:
            # 불타고 있으면
            hp_color = (200, 100, 100)
        else:
            # 불타지 않는다면
            hp_color = (125, 0, 0)

    pygame.draw.rect(screen, (50, 0, 0), (player.rect.x, player.rect.y - up, 32, 8))
    pygame.draw.rect(screen, hp_color,
                     (player.rect.x, player.rect.y - up, 32 - ((player.max_hp - player.hp) / player.max_hp * 32), 8))
    if mp_t:
        pygame.draw.rect(screen, (0, 0, 80), (player.rect.x, player.rect.y - 10, 32, 8))
        pygame.draw.rect(screen, (50, 100, 255),
                         (player.rect.x, player.rect.y - 10,
                          32 - ((player.max_mp - player.mp) / player.max_mp * 32), 8))