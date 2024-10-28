window = 640
field = 144

PIXELS_PER_INCH = field / window

def toField(x, y = None):
    if type(y) == type(None):
        y = x[1]
        x = x[0]
    
    return pxToIn(x) - field / 2, -(pxToIn(y) - field / 2)

def toScreen(x, y = None):
    if type(y) == type(None):
        y = x[1]
        x = x[0]

    return inToPx(x + field / 2), inToPx(-y + field / 2)

def pxToIn(a):
    return a * PIXELS_PER_INCH

def inToPx(a):
    return a / PIXELS_PER_INCH