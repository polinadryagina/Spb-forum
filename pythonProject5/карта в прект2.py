import pygame
import sys
import os
import requests
import math
import district
import webbrowser


class MapParams(object):
    def __init__(self):
        self.lat = 59.965278
        self.lon = 30.213492
        self.zoom = 9
        self.type = "map"

    def coords(self):
        return str(self.lon) + "," + str(self.lat)

    def update(self, event):
        my_step = 0.010
        if event.key == 280 and self.zoom < 19:
            self.zoom += 1
        elif event.key == 281 and self.zoom > 2:
            self.zoom -= 1
        elif event.key == 276:
            self.lon -= my_step * math.pow(2, 15 - self.zoom)
        elif event.key == 275:
            self.lon += my_step * math.pow(2, 15 - self.zoom)
        elif event.key == 273 and self.lat < 85:
            self.lat += my_step * math.pow(2, 15 - self.zoom)
        elif event.key == 274 and self.lat > -85:
            self.lat -= my_step * math.pow(2, 15 - self.zoom)


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.coords(), z=mp.zoom,
                                                                                    type=mp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи файла:", ex)
        sys.exit(2)
    return map_file


def main():
    initialized = False
    screen = None
    mp = MapParams()
    map_file = load_map(mp)
    markers_list = []

    def init_pygame():
        nonlocal initialized
        nonlocal screen
        nonlocal map_file

        pygame.init()
        screen = pygame.display.set_mode((600, 450))
        map_file = load_map(mp)
        markers_list.clear()

        initialized = True

    def finalize(district_caption=None, district_name=None, *, map_file):
        nonlocal initialized

        pygame.quit()
        os.remove(map_file)

        webbrowser.open('http://localhost:5000')  # FIXME: this only works due to natural delay when opening the page
        if district_caption and district_name:
            district.main(district_caption, district_name)

        initialized = False

    while True:
        if not initialized:
            init_pygame()
            pygame.display.set_caption('Выберите район')

        event = pygame.event.wait()
        cursor = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            print('you clicked {}'.format(cursor))
            markers_list.append(cursor)
        if 225 < cursor[0] and cursor[0] < 420 and 188 < cursor[1] and cursor[1] < 340:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('невский район Санкт-Петербурга', 'neva', map_file=map_file)
        if 67 < cursor[0] and cursor[0] < 194 and 145 < cursor[1] and cursor[1] < 227:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('кронштадтский район Санкт-Петербурга', 'kronshtadt', map_file=map_file)
        if 70 < cursor[0] and cursor[0] < 169 and 232 < cursor[1] and cursor[1] < 322:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('ломоносовский район Санкт-Петербурга', 'lomonosov', map_file=map_file)
        if 169 < cursor[0] and cursor[0] < 226 and 248 < cursor[1] and cursor[1] < 356:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('петродворцовый район Санкт-Петербурга', 'petrodvorets', map_file=map_file)
        if 226 < cursor[0] and cursor[0] < 311 and 337 < cursor[1] and cursor[1] < 448:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('красносельский район Санкт-Петербурга', 'krasn', map_file=map_file)
        if 312 < cursor[0] and cursor[0] < 411 and 341 < cursor[1] and cursor[1] < 448:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('пушкинский район Санкт-Петербурга', 'pushkin', map_file=map_file)
        if 417 < cursor[0] and cursor[0] < 565 and 322 < cursor[1] and cursor[1] < 448:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('колпинский район Санкт-Петербурга', 'kolpino', map_file=map_file)
        if 192 < cursor[0] and cursor[0] < 394 and 146 < cursor[1] and cursor[1] < 184:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('приморский район Санкт-Петербурга', 'prim', map_file=map_file)
        if 1 < cursor[0] and cursor[0] < 66 and 223 < cursor[1] and cursor[1] < 312:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('кингисеппский район Санкт-Петербурга', 'kingisep', map_file=map_file)
        if 1 < cursor[0] and cursor[0] < 166 and 312 < cursor[1] and cursor[1] < 448:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('волосовский район Санкт-Петербурга', 'volosovo', map_file=map_file)
        if 263 < cursor[0] and cursor[0] < 416 and 1 < cursor[1] and cursor[1] < 140:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('выборгский район Санкт-Петербурга', 'viborg', map_file=map_file)
        if 1 < cursor[0] and cursor[0] < 262 and 1 < cursor[1] and cursor[1] < 145:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('курортный район Санкт-Петербурга', 'kurort', map_file=map_file)
        if 416 < cursor[0] and cursor[0] < 494 and 1 < cursor[1] and cursor[1] < 188:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                finalize('калининский район Санкт-Петербурга', 'kalin', map_file=map_file)
        elif event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            mp.update(event)

        if initialized:
            image = pygame.image.load(map_file)
            screen.blit(image, (0, 0))
            for m in markers_list:
                pygame.draw.circle(screen, (0, 0, 255), m, 3, 1)
            pygame.display.flip()

    finalize(map_file=map_file)


if __name__ == "__main__":
    main()
