from DAL.DBData import DBData


class DBStatus:
    dta = DBData()

    def select_all_status(self, pi_id):
        return self.dta.select_query("status", pi_id)

    def insert_all_status(self, temp_dict):
        return self.dta.bulk_insert_query("status",temp_dict)