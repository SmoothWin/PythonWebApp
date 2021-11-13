class Humidity:
    date_time = None
    humidity = 0

    def __init__(self, date_time, humidity):
        self.date_time = date_time
        self.humidity = humidity

    def to_dict(self):
        return {
            "date_time": self.date_time,
            "humidity": self.humidity
        }