class MotionProfile:
    def __init__(self, maxVelo, minDecel, maxAccel, minVelo = 0, length = 1, curvature = None):
        self.maxVelo = maxVelo
        self.minDecel = minDecel
        self.maxAccel = maxAccel
        self.minVelo = minVelo
        self.length = length

        self.duration, self.average_velocity, self.t_accel, self.t_decel, self.t_cruise = self.compute()

    def calculateTime(self):
        t_accel = (self.maxVelo - self.minVelo) / self.maxAccel
        t_decel = (self.maxVelo - self.minVelo) / abs(self.minDecel)
        d_accel = 0.5 * self.maxAccel * t_accel**2 + self.minVelo * t_accel
        d_decel = 0.5 * abs(self.minDecel) * t_decel**2 + self.minVelo * t_decel
        d_cruise = self.length - d_accel - d_decel
        
        if d_cruise < 0:
            self.minVelo = ((2 * self.maxAccel * abs(self.minDecel) * self.length) /
                            (self.maxAccel + abs(self.minDecel))) ** 0.5
            t_accel = (self.maxVelo - self.minVelo) / self.maxAccel
            t_decel = (self.maxVelo - self.minVelo) / abs(self.minDecel)
            d_accel = 0.5 * self.maxAccel * t_accel**2 + self.minVelo * t_accel
            d_decel = 0.5 * abs(self.minDecel) * t_decel**2 + self.minVelo * t_decel
            d_cruise = 0

        t_cruise = d_cruise / self.maxVelo if d_cruise > 0 else 0
        return t_accel + t_cruise + t_decel

    def compute(self):
        t_accel = (self.maxVelo - self.minVelo) / self.maxAccel
        t_decel = (self.maxVelo - self.minVelo) / abs(self.minDecel)

        d_accel = 0.5 * self.maxAccel * t_accel**2 + self.minVelo * t_accel
        d_decel = 0.5 * abs(self.minDecel) * t_decel**2 + self.minVelo * t_decel

        d_cruise = self.length - d_accel - d_decel

        if d_cruise < 0:
            self.maxVelo = ((2 * self.maxAccel * abs(self.minDecel) * self.length) /
                            (self.maxAccel + abs(self.minDecel))) ** 0.5
            t_accel = (self.maxVelo - self.minVelo) / self.maxAccel
            t_decel = (self.maxVelo - self.minVelo) / abs(self.minDecel)
            d_accel = 0.5 * self.maxAccel * t_accel**2 + self.minVelo * t_accel
            d_decel = 0.5 * abs(self.minDecel) * t_decel**2 + self.minVelo * t_decel
            d_cruise = 0

        t_cruise = d_cruise / self.maxVelo if d_cruise > 0 else 0

        duration = self.calculateTime()

        return duration, self.length / duration, t_accel, t_decel, t_cruise

    def velocity(self, time):
        if time < self.t_accel:
            return self.minVelo + self.maxAccel * time
        elif time < self.t_accel + self.t_cruise:
            return self.maxVelo
        elif time < self.t_accel + self.t_cruise + self.t_decel:
            decel_time = time - (self.t_accel + self.t_cruise)
            return self.maxVelo - abs(self.minDecel) * decel_time
        else:
            return self.minVelo
