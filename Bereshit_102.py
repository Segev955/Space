import math
import csv
import time
import pygame
import os

# pygame init
import Ship
import autoDriver

SPEED = 0.00001

pygame.font.init()
pygame.mixer.init()
first_distance_from_moon = 13748  # 2:25:40 (as in the simulation) // https://www.youtube.com/watch?v=JJ0VfRL9AMs
first_dist = 181 * 1000
WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulating Bereshit's Landing")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FONT = pygame.font.SysFont('comicsans', 20)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
MOON_HEIGHT = 100
SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('images', 'spaceship.png'))
MOON_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('images', 'moon.png')), (WIDTH, MOON_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('images', 'space.png')), (WIDTH, HEIGHT))


def draw_window(spaceship, angle, data={}):
    WIN.blit(SPACE, (0, 0))
    text = FONT.render(f"Bereshit Spaceship", 1, RED)
    center = ((WIDTH - text.get_width()) * 0.5)
    WIN.blit(text, (center, 15))
    text = FONT.render(f"Landing Information:", 1, WHITE)
    WIN.blit(text, (10, 25))
    i = 2
    for k, v in data.items():
        text = FONT.render(f"{k}: {v}", 1, WHITE)
        WIN.blit(text, (10, i * 25))
        i += 1
    SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
                                        angle)
    WIN.blit(MOON_IMAGE, (0, 800))
    WIN.blit(SPACESHIP, (spaceship.x, spaceship.y))
    pygame.display.update()


def spaceship_movement(distance, dist, spaceship):
    last_dist = -88605.0146196441
    dx = (dist - last_dist) / (first_dist - last_dist)
    dy = distance / first_distance_from_moon
    spaceship.x = WIDTH - WIDTH * dx - MOON_HEIGHT
    spaceship.y = HEIGHT - HEIGHT * dy - MOON_HEIGHT


def csv_unique_name():
    path = f"{os.getcwd()}\logs"
    if not os.path.isdir(path):
        os.makedirs(path)
    files = os.listdir(path)
    i = 1
    while 1:
        if f'log{i}.csv' not in files:
            return f'log{i}'
        i += 1


def makeCsv(l, folder='logs', csvname='bereshit_102'):
    path = os.path.join(os.getcwd(), folder)
    try:
        os.mkdir(path)
    except:
        pass
    f = open(f'{folder}/{csvname}.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerows(l)
    f.close()
    print(f'{csvname} saved.')


# 14095, 955.5, 24.8, 2.0
def main(simulation=1, first_distance_from_moon=first_distance_from_moon):
    tocsv = []
    ship = Ship.Ship(24.8, 932, first_dist, 58.3, first_distance_from_moon, 1, 0, 121)
    spaceship = pygame.Rect(0, 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # starting point:
    _time = 0
    p = 0.04
    i = 0.0003
    d = 0.2

    driver = autoDriver.autoDriver(p, i, d)

    print(f"simulation {simulation} started")
    if simulation == 1:
        print("Simulating Bereshit's Landing:")
        tocsv.append(['time', 'vertical_speed', 'horizontal_speed', 'dist', 'distance_from_moon', 'angle', 'weight',
                      'acceleration', 'dvs', 'fuel', 'PID', 'NN'])
        print(tocsv[0])
    NN = 0.7  # rate[0,1]
    last_NN = NN
    pid = 0
    dvs = ship.desired_vs()
    # pid2 = PID.PID(p,i,d, 100)

    # ***** main simulation loop ******
    while ship.distance_from_moon > 0:
        # # ------------------PID2---------------------------
        # dhs = ship.desired_hs()
        # dvs = ship.desired_vs()
        # error = ship.vertical_speed - dvs
        # gas = pid2.update(error, ship.dt)
        # # print(gas)
        # nn = NN + gas
        # if 0 <= nn <= 1:
        #     NN = nn
        # # ------------------PID2---------------------------

        # ------------------PID1---------------------------
        dvs = ship.desired_vs()
        pid = driver.pid(ship.vertical_speed, dvs)  # dvs = 23
        NN = max(min(last_NN + pid, 1), 0)
        # ------------------PID1---------------------------
        tocsv.append(
            [_time, ship.vertical_speed, ship.horizontal_speed, ship.dist, ship.distance_from_moon, ship.angle,
             ship.weight, ship.acceleration, dvs, ship.fuel, pid, NN])
        if simulation == 1 and (_time % 10 == 0 or ship.distance_from_moon < 100):
            print(tocsv[-1])
        ang = ship.angle
        if ship.distance_from_moon < 2000:
            if ship.angle > 3:
                ship.angle -= 3  # rotate to vertical position.
                ship.horizontal_speed -= 2
            else:
                ship.angle -= ang

        # main computations
        ang_rad = math.radians(ship.angle)
        h_acc = math.sin(ang_rad) * ship.acceleration
        v_acc = math.cos(ang_rad) * ship.acceleration
        vacc = ship.getAcc(ship.horizontal_speed)
        _time += ship.dt
        dw = ship.dt * ship.ALL_BURN * NN
        if ship.fuel > 0:
            ship.fuel -= dw
            weight = ship.WEIGHT_EMP + ship.fuel
            ship.acceleration = NN * ship.accMax(weight)

        else:  # ran out of fuel
            ship.acceleration = 0

        v_acc -= vacc
        if ship.horizontal_speed > 0:
            ship.horizontal_speed -= h_acc * ship.dt

            if ship.angle == 0:
                ship.horizontal_speed = 0
        ship.dist -= ship.horizontal_speed * ship.dt
        ship.vertical_speed -= v_acc * ship.dt
        ship.distance_from_moon -= ship.dt * ship.vertical_speed

        # update gui
        spaceship_movement(ship.distance_from_moon, ship.dist, spaceship)
        data = {'time': round(_time, 2), 'vertical speed': round(ship.vertical_speed, 2),
                'horizontal speed': round(ship.horizontal_speed, 2), 'distance': round(ship.distance_from_moon, 2),
                'wait': round(ship.weight, 2), 'dvs': round(dvs, 2), 'fuel': round(ship.fuel, 2), 'NN': round(NN, 2),
                'PID': round(pid, 5)}
        draw_window(spaceship, ship.angle, data)
        last_NN = NN
        time.sleep(0.01)

    tocsv.append(
        [_time, ship.vertical_speed, ship.horizontal_speed, ship.dist, ship.distance_from_moon, ship.angle,
         ship.weight, ship.acceleration, dvs, ship.fuel, pid, NN])
    # making a csv file of the data
    if simulation == 1:
        makeCsv(tocsv, csvname=csv_unique_name())

    # show the results for 10 seconds
    time.sleep(10)

    # repeat the gui for 5 times
    if simulation == 5:
        pygame.quit()
        return
    main(simulation=simulation + 1)


if __name__ == '__main__':
    main()
