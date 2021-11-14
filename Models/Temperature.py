class Temperature:
    date_time = None
    temperature = 0

    def __init__(self, date_time, temperature):
        self.date_time = date_time
        self.temperature = temperature

    def to_dict(self):
        return{
            "date_time": self.date_time,
            "temperature": self.temperature
        }