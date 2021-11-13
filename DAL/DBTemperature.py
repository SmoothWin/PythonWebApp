from DAL.DBData import DBData

class DBTemperature:
    dta = DBData()

    def select_all_temperatures(self):
        return self.dta.select_query("temperature")