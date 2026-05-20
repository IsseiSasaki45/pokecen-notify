import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 700))  # ウィンドウサイズ
pygame.display.set_caption("Black Window")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # 真っ黒
    pygame.display.flip()