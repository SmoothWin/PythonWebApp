class Status:
    date_time = None
    online = False

    def __init__(self, date_time, online):
        self.date_time = date_time
        self.online = online

    def to_dict(self):
        return{
            "date_time": self.date_time,
            "online": self.online
        }