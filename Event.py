class Event:
    def __init__(self, venue, name, time, date):
        self.venue = venue
        self.name = name
        self.time = time
        self.date = date
        self.latitude = 0.0
        self.longitude = 0.0

    def __str__(self):
        return f"{self.venue}: {self.name} ({self.time})\n"

    __repr__ = __str__
