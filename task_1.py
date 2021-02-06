import os
import sys
import math
import pygame
import requests

coord = ['37.628070', '55.750630']
height, width = 600, 450
scale = 15
layer = 'map'


def update_image():
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&z={scale}&size={height},{width}&l=" \
                  f"{layer}"

    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))

    return map_file


#def button():
#    screen.fill(pygame.Color('#C9C9C9'), (425, 5, 20, 100))


pygame.init()
screen = pygame.display.set_mode((height, width))
map_file = update_image()

pygame.display.flip()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if scale < 17:
                    scale += 1
            if event.key == pygame.K_PAGEDOWN:
                if scale > 1:
                    scale -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    coord[1] = str(float(coord[1]) + 0.008 * math.pow(2, 15 - scale))
                if event.key == pygame.K_DOWN:
                    coord[1] = str(float(coord[1]) - 0.008 * math.pow(2, 15 - scale))
                if event.key == pygame.K_RIGHT:
                    coord[0] = str(float(coord[0]) + 0.008 * math.pow(2, 15 - scale))
                if event.key == pygame.K_LEFT:
                    coord[0] = str(float(coord[0]) - 0.008 * math.pow(2, 15 - scale))
                if event.key == pygame.K_m:
                    layer = "map"
                if event.key == pygame.K_s:
                    layer = "sat"
                if event.key == pygame.K_g:
                    layer = "sat,skl"
            map_file = update_image()
#            button()
    pygame.display.flip()
pygame.quit()