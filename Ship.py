import csv
import os


class Ship:
    def __init__(self, vertical_speed, horizontal_speed, dist, angle, distance_from_moon, dt, acceleration, fuel):
        self.WEIGHT_EMP = 165  # kg
        self.WEIGHT_FULE = 420  # kg
        self.WEIGHT_FULL = self.WEIGHT_EMP + self.WEIGHT_FULE  # kg
        self.MAIN_ENG_F = 430  # N
        self.SECOND_ENG_F = 25  # N
        self.MAIN_BURN = 0.15  # liter per sec, 12 liter per m'
        self.SECOND_BURN = 0.009  # liter per sec 0.6 liter per m'
        self.ALL_BURN = self.MAIN_BURN + 8 * self.SECOND_BURN
        self.RADIUS = 3475 * 1000  # meters
        self.ACC = 1.622  # m/s^2
        self.EQ_SPEED = 1700  # m/s

        self.vertical_speed = vertical_speed
        self.horizontal_speed = horizontal_speed
        self.dist = dist
        self.angle = angle
        self.distance_from_moon = distance_from_moon
        self.dt = dt
        self.acceleration = acceleration
        self.fuel = fuel
        self.weight = self.WEIGHT_EMP + self.fuel

    def accMax(self, weight: float) -> float:
        return self.acc(weight, True, 8)

    def acc(self, weight: float, main: bool, seconds: int) -> float:
        t = 0
        if main:
            t += self.MAIN_ENG_F
        t += seconds * self.SECOND_ENG_F
        ans = t / weight
        return ans

    def getAcc(self, speed):
        n = abs(speed) / self.EQ_SPEED
        ans = (1 - n) * self.ACC
        return ans

    def desired_vs(self):
        maxAlt = 30000
        if self.distance_from_moon > maxAlt:
            return 0
        if self.distance_from_moon > 2000:
            return 24
        if self.distance_from_moon > 1000:
            return 20
        if self.distance_from_moon > 500:
            return 15
        if self.distance_from_moon > 300:
            return 12
        if self.distance_from_moon > 200:
            return 10
        if self.distance_from_moon > 100:
            return 8
        if self.distance_from_moon > 50:
            return 6
        if self.distance_from_moon > 20:
            return 2
        return 3

    def desired_hs(self):
        minAlt = 2000
        maxAlt = 30000
        if self.distance_from_moon < minAlt:
            return 0
        if self.distance_from_moon > maxAlt:
            return self.EQ_SPEED
        norm = pow((self.distance_from_moon - minAlt) / (maxAlt - minAlt),0.70)
        dhs = norm * self.EQ_SPEED
        return dhs

