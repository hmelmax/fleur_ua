import mysql.connector

class DB():

    def __init__(self):
        self.conn = None
        self.cur = None
        self.db_name = 'fleur.db'

    def connect(self):
        self.conn = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='fleur')
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    def create_if_empty(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS category
                        (name text, url text, page_count text, last_page text)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS item
                        (name text, price text, category text, sku text, available text)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS tmp_item
                        (name text, price text, category text, sku text, available text)''')

    def insert_into_category(self, category_name, url, page_count):
        self.cur.execute('''SELECT * FROM category WHERE name=%s''', category_name)
        if self.cur.rowcount == 0:
            self.cur.execute('''INSERT INTO category (name, url, page_count, last_page) values
                            (%s, %s, %s, 0);''', (category_name, url, page_count))
        else:
            self.cur.execute('''UPDATE category SET page_count=%s
                             WHERE name=%s''', (page_count, category_name))

    def insert_into_tmp_item(self, item_name, price, category, sku, available,):
        self.cur.execute('''INSERT INTO tmp_item (name, price, category, sku, available) values
                        (%s, %s, %s, %s, %s);''', (item_name, price, category, sku, available))

    def swap(self):
        self.cur.execute('''DROP TABLE item''')
        self.cur.execute('''ALTER TABLE tmp_item RENAME TO item''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tmp_item
                        (name text, price text, category text, sku text, available text)''')

    def select_categories(self):
        result = {}
        self.cur.execute('''SELECT * FROM category''')
        for row in self.cur:
            result[row[0]] = {"url": row[1], "count": row[2], "last_page": row[3]}
        return result

    def commit(self):
        self.conn.commit()

    def update_category(self, category, last_page):
        self.cur.execute('''UPDATE category SET last_page=%s
                         WHERE name=%s''', (last_page, category))
