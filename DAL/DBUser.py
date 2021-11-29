from DAL.DBData import DBData


class DBUser:
    dta = DBData()

    def select_user(self, name):
        return self.dta.select_user(name)

    def insert_user(self, uuid, name, password, admin:bool):
        return self.dta.insert_user(uuid, name, password, admin)