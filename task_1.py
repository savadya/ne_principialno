import os
import sys

import pygame
import requests

coord = ('37.628070', '55.750630')
height, width = 600, 450
scale = 15

map_request = f"https://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&z={scale}&size={height},{width}&l=map"
print(map_request)
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

d1 = toponym['boundedBy']['Envelope']['lowerCorner'].split()
d2 = toponym['boundedBy']['Envelope']['upperCorner'].split()
org_point = toponym['Point']['pos']
org_point[0], org_point[1] = float(org_point[0]), float(org_point[1])
d1[0], d1[1] = float(d1[0]), float(d1[1])
d2[0], d2[1] = float(d2[0]), float(d2[1])
delta = [str(d2[0] - d1[0]), str(d2[1] - d1[1])]
# Собираем параметры для запроса к StaticMapsAPI:

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(delta),
    "l": "map",
    "pt": ",".join([toponym_longitude, toponym_lattitude])
}

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((height, width))
screen.blit(pygame.image.load(map_file), (0, 0))

pygame.display.flip()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                coord[1] += width
            if event.key == pygame.K_DOWN:
                coord[1] -= width
            if event.key == pygame.K_RIGHT:
                coord[0] -= width
            if event.key == pygame.K_LEFT:
                coord[0] += width
            if event.key == pygame.K_PAGEUP:
                pass
            if event.key == pygame.K_PAGEDOWN:
                pass
            if event.key == pygame.K_m:
                map_params["l"] = "map"
            if event.key == pygame.K_s:
                map_params["l"] = "sat"
    pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
