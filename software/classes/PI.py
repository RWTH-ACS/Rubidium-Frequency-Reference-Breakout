class PI():
    #halbiert um 08:03 5.12.25 i:1e-8, p:-5e-5
    I = 1e-5
    P = 5e6
    last = 0
    now = 0
    bound = 2e-9
    limit = 0.5
    def __init__(self, x):
        self.i = x
        self.p = 0
    def update(self, error):
        
        if error >= self.bound:
            error = error - self.bound
        elif error <= -self.bound:
            error = error + self.bound
        else:
            error = 0
        
        self.last = self.i + self.p
        self.i += error * self.I
        if abs(self.i) > self.limit:
            self.i -= error * self.I
        self.p = error * self.P
        self.now = self.i + self.p