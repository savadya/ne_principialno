import os
import sys

import pygame
import requests

coord = ('37.530887', '55.703118')
height, width = 600, 450

map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&spn=0.002,0.002&l=map&size={HEIGHT},{WIDTH}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)


map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
screen.blit(pygame.image.load(map_file), (0, 0))

pygame.display.flip()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()


os.remove(map_file)