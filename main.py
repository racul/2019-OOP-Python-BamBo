import pygame
import Classes

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = 800  # 게임화면의 가로크기
pad_height = 1000  # 게임화면의 세로크기
balls = []

pygame.init()


screen = pygame.display.set_mode((pad_height, pad_width))
pygame.display.set_caption("Python/Pygame Animation")
clock = pygame.time.Clock()
player = Classes.User((150, 150))

game_over = False

while game_over == False:

    # 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        player.handle_event(event)


    player.update()
    screen.fill(pygame.Color('white'))
    Classes.show_player_state()

    # 공 처리
    for ball in balls:
        ball.update()
        screen.blit(ball.image, ball.rect)

    print(player.mp)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
