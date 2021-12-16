from DAL.DBData import DBData


class DBPis:
    dta = DBData()

    def select_all_pis(self):
        return self.dta.select_all_pi()