import pygame
# 按键的打印
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('test')

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(event.key)
    # screen.fill(ai_settings.bg_color)
    pygame.display.flip()