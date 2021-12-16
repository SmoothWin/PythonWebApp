from DAL.DBData import DBData


class DBHumidity:
    dta = DBData()

    def select_all_humidities(self, pi_id):
        return self.dta.select_query("humidity", pi_id)

    def insert_all_humidities(self, temp_dict):
        return self.dta.bulk_insert_query("humidity",temp_dict)