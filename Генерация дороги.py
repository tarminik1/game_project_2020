import pygame
from random import randint

print('z ujdyjtl')

pygame.init()

FPS = 30
Ecrx = 1200
Ecry = 720
screen = pygame.display.set_mode((Ecrx, Ecry))
screen.fill((100, 200, 0))


def generate_road(ecrx, ecry):
    x = ecrx / 10
    y = ecry / 2
    shag = 0
    massiv = [[int(x), int(y)]]
    while x < 9 * ecrx / 10 - 50:
        shag += 1
        dl = randint(-100, 100)
        if shag % 2 == 1:
            x = x + 50 + dl ** 2 / abs(dl)
        else:
            y += dl / abs(dl) * (50 + abs(dl))
        if y < 100 or y > 600:
            y -= 2 * dl / abs(dl) * (50 + abs(dl))
        massiv = massiv + [[int(x), int(y)]]
    if x < 9 * ecrx / 10:
        massiv = massiv + [[int(9 * ecrx / 10), int(y)]]
    return massiv


def draw_road(massiv):
    for pos in massiv:
        pygame.draw.circle(screen, [0, 0, 0], pos, 12)
    pygame.draw.lines(screen, [0, 0, 0], False, massiv, 24)
    for pos in massiv:
        pygame.draw.circle(screen, [200, 100, 0], pos, 10)
    pygame.draw.lines(screen, [200, 100, 0], False, massiv, 20)


def inside_check(x, y, a):
    """
    проверяет, находится ли внутри выпуклого(!!!) многоугольника данная точка
    :param x: координата х данной точки
    :param y: координата у данной точки
    :param a: массив с координатами точек вершин многоугольника
    :return:
    """
    det_prev = 0
    for iba in range(len(a)):
        a_x = a[iba][0]
        a_y = a[iba][1]
        b_x = a[(iba + 1) % len(a)][0]
        b_y = a[(iba + 1) % len(a)][1]
        # counting vector between the first neighbouring vertex and point
        ev_point_x = x - a_x
        ev_point_y = y - a_y
        v_x = b_x - a_x
        v_y = b_y - a_y
        # counting the determinant(oriented area)
        det = - ev_point_x * v_y + ev_point_y * v_x
        # Ориентация поменялась?
        if det * det_prev < 0:
            return False
        det_prev = - ev_point_x * v_y + ev_point_y * v_x
    return True


def generare_buildings(massiv_road, r):
    min_x, min_y, max_x, max_y = 1000, 1000, 0, 0
    road = [[0, 0]]
    for pos in massiv_road:
        min_x = min(min_x, pos[0])
        max_x = max(max_x, pos[0])
        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])
    x = min_x
    y = 100
    for i in range(len(massiv_road) - 1):
        while x < massiv_road[i + 1][0]:
            road += [[int(x), int(
                (massiv_road[i][1] * (x - massiv_road[i][0]) + massiv_road[i + 1][1] * (massiv_road[i + 1][0] - x)) / (
                        massiv_road[i + 1][0] - massiv_road[i][0]))]]
            x += 3

    return road


pygame.display.update()
clock = pygame.time.Clock()
finished = False

Road = generate_road(Ecrx, Ecry)
Buildings = generare_buildings(Road, 50)
print(Road)
print(Buildings)

while not finished:
    clock.tick(FPS)
    draw_road(Road)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
