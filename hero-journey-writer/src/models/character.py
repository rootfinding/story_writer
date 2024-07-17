class Character:
    def __init__(self, name, role, weakness, key):
        self.name = name
        self.role = role
        self.weakness = weakness
        self.key = key
        self.attitude = 0  # -100 to 100, negative is hostile, positive is friendly

    def update_attitude(self, value):
        self.attitude += value
        self.attitude = max(-100, min(100, self.attitude))

    def get_disposition(self):
        if self.attitude > 50:
            return "Muy amistoso"
        elif self.attitude > 0:
            return "Amistoso"
        elif self.attitude > -50:
            return "Neutral"
        else:
            return "Hostil"
