from DAL.DBData import DBData


class DBTemperature:
    dta = DBData()

    def select_all_temperatures(self, pi_id):
        return self.dta.select_query("temperature", pi_id)

    def insert_all_temperatures(self, temp_dict):
        return self.dta.bulk_insert_query("temperature",temp_dict)
