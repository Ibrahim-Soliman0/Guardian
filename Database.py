import psycopg2


class SQL:

    def __init__(self):

        self.connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="Malware_Tracker",
            user="postgres",
            password="123",
        )
        self.cursor = self.connection.cursor()

    #def insert_next_version(self):
    #    sql = """
    #        INSERT INTO version (version_number)
    #        VALUES ( nextval('version_seq') )
    #        RETURNING version_number;
    #    """
    #    try:
    #        self.cursor.execute(sql)
    #        new_version = self.cursor.fetchone()[0]
    #        self.connection.commit()
    #        return new_version
    #    except Exception as e:
    #        self.connection.rollback()
    #        print("Something went wrong:", e)

    def insert_detection_data(self, data, freq, dtype, process_id):
        try:
            self.cursor.execute("""
                                INSERT INTO detection_data (data, freq, type, process_id)
                                VALUES (%s, %s, %s, %s)
                                """, (data, freq, dtype, process_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Something went wrong:", e)


    def insert_process(self, process_name):
        try:
            self.cursor.execute("""
                                INSERT INTO process ("process_name") VALUES (%s) RETURNING id;
                                """, (process_name,))
            process_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return process_id
        except Exception as e:
            self.connection.rollback()
            print("Something went wrong:", e)

    #def insert_malware_type(self, malware_type):
    #    try:
    #        self.cursor.execute("""
    #                            INSERT INTO malware_type ("type") VALUES (%s) RETURNING id;
    #                            """, (malware_type,))
    #        malware_type_id = self.cursor.fetchone()[0]
    #        self.connection.commit()
    #        return malware_type_id
    #    except Exception as e:
    #        self.connection.rollback()
    #        print("Something went wrong:", e)

    def insert_weight(self, weight):
        try:
            self.cursor.execute(
                "INSERT INTO weight (weight) VALUES (%s)",
                (weight,)
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Something went wrong:", e)

    def insert_process_path(self, process_id, type_id, path):
        try:
            self.cursor.execute("""
                                INSERT INTO malicious_process ("process_id", "type_id", "path") VALUES (%s, %s, %s)
                                """, (process_id, type_id, path,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Something went wrong:", e)

    def get_detection_data(self):
        self.cursor.execute("""SELECT * FROM detection_data;""")
        detection_data = self.cursor.fetchall()
        return detection_data

    def get_weight_data(self):
        self.cursor.execute("""SELECT * FROM weight;""")
        detection_data = self.cursor.fetchall()
        return detection_data

    def get_version(self):
        self.cursor.execute("SELECT MAX(version_number) FROM version;")
        row = self.cursor.fetchone()
        if row is None:
            return None
        return row[0]

    def get_process_id(self, process_name):
        self.cursor.execute("""SELECT id FROM process WHERE process_name = %s;""", (process_name,))
        process_id = self.cursor.fetchone()
        return process_id

    def get_malware_type_id(self, type):
        self.cursor.execute("""SELECT id FROM malware_type WHERE type = %s;""", (type,))
        type_id = self.cursor.fetchone()
        return type_id

    def get_freq_gt_zero(self):
        self.cursor.execute("""SELECT data, freq, type FROM detection_data WHERE freq > 0 ORDER BY type, data;""")
        rows_pos = self.cursor.fetchall()
        return rows_pos

    def get_freq_eq_zero(self):
        self.cursor.execute("""SELECT data, type FROM detection_data WHERE freq = 0 ORDER BY type, data;""")
        rows_zero = self.cursor.fetchall()
        return rows_zero

    def process_exists(self, process_name):
        self.cursor.execute("SELECT * FROM process WHERE process_name = %s;", (process_name,))
        exists = True if self.cursor.fetchall() else False
        return exists

    #def malware_type_exists(self, type):
    #    self.cursor.execute("SELECT * FROM malware_type WHERE type = %s;", (type,))
    #    exists = True if self.cursor.fetchall() else False
    #    return exists

    def close_resources(self):
        self.cursor.close()
        self.connection.close()