import json
import mysql.connector
from mysql.connector import pooling

class Db:
    def __init__(self, config):
        self.config = config
        try:
            self.connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                  pool_size=5,
                                                  pool_reset_session=True,
                                                  host=self.config["host"],
                                                  database=self.config["database"],
                                                  user=self.config["user"],
                                                  password=self.config["password"])
        except:
            print("error: No database pool created!")


    def get_years(self, id):
        res = self.exec("SELECT first_year, last_year FROM entity_years WHERE id = '" + id +"'")
        if len(res) > 0:
            return res[0]
        else:
            return None

    def exec(self, sql):
        connection_object = self.connection_pool.get_connection()
        json_data=[]
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute(sql)
            rv = cursor.fetchall()
            row_headers=[x[0] for x in cursor.description]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))
            cursor.close()
            connection_object.close()
        return json_data