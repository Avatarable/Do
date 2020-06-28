import sqlite3
import datetime


class Account(object):

    @staticmethod
    def _current_time():
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def __init__(self, account_name):
        self.account_name = account_name
        self.db = sqlite3.connect(f"{self.account_name}.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

    def create(self, list_name):
        try:
            self.db.execute("CREATE TABLE IF NOT EXISTS {} (item TEXT PRIMARY KEY NOT NULL, date_created TEXT NOT NULL)".format(list_name))
        except:
            self.db.rollback()
        else:
            self.db.commit()

    def insert(self, list_name, item):
        try:
            date_created = self._current_time()
            self.db.execute("INSERT INTO {} VALUES (?, ?)".format(list_name), (item, date_created))
        except:
            self.db.rollback()
        else:
            self.db.commit()

    def update(self, list_name, item, modified_item):
        try:
            self.db.execute("UPDATE {} SET item=? WHERE (item=?)".format(list_name), (modified_item, item))
        except:
            self.db.rollback()
        else:
            self.db.commit()

    def delete(self, list_name, item):
        try:
            self.db.execute("DELETE FROM {} WHERE (item=?)".format(list_name), (item,))
        except:
            self.db.rollback()
        else:
            self.db.commit()

    def load(self, list_name):
        list_items = []
        cursor = self.db.execute("SELECT item, date_created FROM {}".format(list_name))
        row = cursor.fetchall()
        if row:
            for item in row:
                list_items.append(item[0])
            return list_items

    def load_tables(self):
        tables = []
        cursor = self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        row = cursor.fetchall()
        if row:
            for table_name in row:
                tables.append(table_name[0])
            return tables

    def drop(self, list_name):
        try:
            self.db.execute("DROP TABLE {}".format(list_name))
        except:
            print("cannot delete")
            self.db.rollback()
        else:
            self.db.commit()


if __name__ == '__main__':
    bruno = Account("Bruno")
    bruno.create("monday")
    bruno.insert('monday', 'buy rice')
    bruno.insert('monday', 'play games')
    print(bruno.load('monday'))
    t = bruno.load_tables()
    print(t)

    bruno.db.close()