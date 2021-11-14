from DAL.DBData import DBData


class DBAll:
    dta = DBData()

    def select_all(self):
        return self.dta.select_query_all()