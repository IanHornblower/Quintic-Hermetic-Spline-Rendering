import numpy as np

class Polynomial:
    def derive(self):
        pass

    def evaluate(self, time):
        pass

class Quintic(Polynomial):
    def __init__(self, a5, a4, a3, a2, a1, a0):
        self.a5 = a5
        self.a4 = a4
        self.a3 = a3
        self.a2 = a2
        self.a1 = a1
        self.a0 = a0

    def derive(self):
        return Quartic(self.a5 * 5.0, self.a4 * 4.0, self.a3 * 3.0, self.a2 * 2.0, self.a1)

    def evaluate(self, time):
        return self.a5 * (time ** 5) + self.a4 * (time ** 4) + self.a3 * (time ** 3) + self.a2 * (time ** 2) + self.a1 * time + self.a0

    def translate_x(self, translation):
        coeffs = np.poly1d([self.a5, self.a4, self.a3, self.a2, self.a1, self.a0]).__call__(np.poly1d([1, -translation]))
        return Quintic(coeffs[0], coeffs[1], coeffs[2], coeffs[3], coeffs[4], coeffs[5])

    def __str__(self):
        return f"{self.a5}x^5 + {self.a4}x^4 + {self.a3}x^3 + {self.a2}x^2 + {self.a1}x + {self.a0}"

class Quartic(Polynomial):
    def __init__(self, a4, a3, a2, a1, a0):
        self.a4 = a4
        self.a3 = a3
        self.a2 = a2
        self.a1 = a1
        self.a0 = a0

    def derive(self):
        return Cubic(self.a4 * 4.0, self.a3 * 3.0, self.a2 * 2.0, self.a1)

    def evaluate(self, time):
        return self.a4 * (time ** 4) + self.a3 * (time ** 3) + self.a2 * (time ** 2) + self.a1 * time + self.a0

    def translate_x(self, translation):
        coeffs = np.poly1d([self.a4, self.a3, self.a2, self.a1, self.a0]).__call__(np.poly1d([1, -translation]))
        return Quartic(coeffs[0], coeffs[1], coeffs[2], coeffs[3], coeffs[4])

    def __str__(self):
        return f"{self.a4}x^4 + {self.a3}x^3 + {self.a2}x^2 + {self.a1}x + {self.a0}"


class Cubic(Polynomial):
    def __init__(self, a3, a2, a1, a0):
        self.a3 = a3
        self.a2 = a2
        self.a1 = a1
        self.a0 = a0

    def derive(self):
        return Quardatic(self.a3 * 3.0, self.a2 * 2.0, self.a1)

    def evaluate(self, time):
        return self.a3 * (time ** 3) + self.a2 * (time ** 2) + self.a1 * time + self.a0
    
    def translate_x(self, translation):
        self.a3, self.a2, self.a1, self.a0 = np.poly1d([self.a3, self.a2, self.a1, self.a0]).__call__(np.poly1d([1, -translation]))
        return Cubic(self.a3, self.a2, self.a1, self.a0)

    def __str__(self):
        return f"{self.a3}x^3 + {self.a2}x^2 + {self.a1}x + {self.a0}"

class Quardatic(Polynomial):
    def __init__(self, a2, a1, a0):
        self.a2 = a2
        self.a1 = a1
        self.a0 = a0
    
    def derive(self):
        return Linear(self.a2 * 2, self.a1)

    def evaluate(self, time):
        return self.a2 * (time ** 2) + self.a1 * time + self.a0

    def translate_x(self, translation): # untested
        self.a2, self.a1, self.a0 = np.poly1d([self.a2, self.a1, self.a0]).__call__(np.poly1d([1, -translation]))
        return Quardatic(self.a2, self.a1, self.a0)

    def __str__(self):
        return f"{self.a2}x^2 + {self.a1}x + {self.a0}"

class Linear(Polynomial):
    def __init__(self, a1, a0):
        self.a1 = a1
        self.a0 = a0

    def derive(self):
        return Constant(self.a1)

    def evaluate(self, time):
        return self.a1 * time + self.a0

    def translate_x(self, translation): # untested
        self.a1, self.a0 = np.poly1d([self.a1, self.a0]).__call__(np.poly1d([1, -translation]))
        return Linear(self.a1, self.a0)

    def __str__(self):
        return f"{self.a1}x + {self.a0}"

class Constant(Polynomial):
    def __init__(self, a0):
        self.a0 = a0

    def evaluate(self, time):
        return self.a0

    def derive(self):
        return 0
    
    def __str__(self):
        return f"{self.a0}"