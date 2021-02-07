import os
import sys
import math
import pygame
import requests

coord = ['37.628070', '55.750630']
height, width = 600, 450
scale = 15
layer = 'map'
need_input = False
input_text = ''
pt = []


def update_image():
    map_request = "https://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ",".join(coord),
        "z": scale,
        "size": ",".join([str(height), str(width)]),
        "l": layer}

    response = requests.get(map_request, map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    print(coord)

    return map_file


def button():
    screen.fill(pygame.Color('#C9C9C9'), (5, 420, 300, 25))
    screen.fill(pygame.Color('#F8173E'), (310, 420, 78, 25))
    font = pygame.font.Font(None, 25)
    text = font.render("Искать", True, pygame.Color('#FFFFFF'))
    screen.blit(text, (320, 425))
    font2 = pygame.font.Font(None, 25)
    text2 = font2.render(input_text, True, pygame.Color('#FFFFFF'))
    screen.blit(text2, (15, 425))
    print('f')



def reserch():
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": input_text,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    print(json_response)

    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    coord = toponym_coodrinates.split(" ")

    map_params = {
        "ll": ",".join(coord),
        "z": scale,
        "l": layer,
        "pt": f"{coord[0]},{coord[1]},pmwtm1"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    print(response.url)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    return coord


pygame.init()
screen = pygame.display.set_mode((height, width))
map_file = update_image()

pygame.display.flip()
run = True
map_file = update_image()
button()
flag_layer = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if need_input and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            if event.key == pygame.K_RETURN or (310 <= pygame.mouse.get_pos()[0] <= 388 and
                                                420 <= pygame.mouse.get_pos()[1] <= 445):
                coord = reserch()
                input_text = ''
                need_input = False
                flag_layer = True
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
                flag_layer = False

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
                if flag_layer:
                    if event.key == pygame.K_m:
                        layer = "map"
                    if event.key == pygame.K_s:
                        layer = "sat"
                    if event.key == pygame.K_g:
                        layer = "sat,skl"
                map_file = update_image()
                button()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 5 <= pygame.mouse.get_pos()[0] <= 305 and 420 <= pygame.mouse.get_pos()[1] <= 445:
                need_input = True


    pygame.display.flip()
pygame.quit()
