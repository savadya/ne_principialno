import os
import sys
import math
import pygame
import requests
from yandex_geocoder import Client

coord = ['37.628070', '55.750630']
height, width = 600, 450
scale = 15
client = Client("40d1649f-0493-4b70-98ba-98533de7710b")


def update_image():
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&z={scale}&size={height},{width}&l=map&pt={coord[0]},{coord[1]}"

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

def get_coord(address):
    coordinates = client.coordinates(address)
    return coordinates

class Button:
    def __init__(self, x, y, height, width, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.draw()

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.height, self.width), width=1)

        font = pygame.font.Font(None, self.width)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.x + 15, self.y + 5))

    def push_button(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.height and pos[1] > self.y and pos[1] < self.y + self.width:
            return True


pygame.init()
screen = pygame.display.set_mode((height, width + 200))
map_file = update_image()
button = Button(250, 600, 100, 30, 'Искать')
font = pygame.font.Font(None, 30)

pygame.display.flip()
run = True
address = ''
text = font.render(address, True, (255, 255, 255))
rect = text.get_rect()
rect.center = (150, 550)

while run:
    screen.fill((0, 0, 0))
    button.draw()
    pygame.draw.line(screen, (255, 255, 255), (150, 550), (450, 550))
    screen.blit(pygame.image.load(map_file), (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.push_button(event.pos):
                coord = get_coord(address)
                update_image()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if scale < 17:
                    scale += 1
                    map_file = update_image()
            if event.key == pygame.K_PAGEDOWN:
                if scale > 1:
                    scale -= 1
                    map_file = update_image()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    coord[1] = str(float(coord[1]) + 0.008 * math.pow(2, 15 - scale))
                    map_file = update_image()
                if event.key == pygame.K_DOWN:
                    coord[1] = str(float(coord[1]) - 0.008 * math.pow(2, 15 - scale))
                    map_file = update_image()
                if event.key == pygame.K_RIGHT:
                    coord[0] = str(float(coord[0]) + 0.008 * math.pow(2, 15 - scale))
                    map_file = update_image()
                if event.key == pygame.K_LEFT:
                    coord[0] = str(float(coord[0]) - 0.008 * math.pow(2, 15 - scale))
                    map_file = update_image()

                if event.unicode:
                    address += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    address = address[:-1]
                elif event.key == pygame.K_DELETE:
                    address = ""

                text = font.render(address, True, (255, 255, 255))
                rect = text.get_rect()
                rect.center = (300 + len(address) * 0.1, 535)
                
    screen.blit(text, rect)
            
    pygame.display.flip()
os.remove(map_file)
pygame.quit()
