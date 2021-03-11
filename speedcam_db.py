import mysql.connector
import mysql.connector.cursor
import sc_utils
import datetime
from dateutil.parser import parse

class SpeedcamDB:
    def __init__(self, hostname="localhost", user="root", password="speedcam", db_name="speedcam_mining"):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.db_name = db_name
        self.db: mysql.connector.MySQLConnection = None
        self.cursor: mysql.connector.cursor.MySQLCursor = None

        self._open_db_connection()
        self._ensure_speedcam_table_initialized()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def _open_db_connection(self):
        self.db = mysql.connector.connect(
            host=self.hostname,
            user=self.user,
            password=self.password,
            database=self.db_name,
        )
        self.db.get_warnings = True
        self.db.raise_on_warnings = True
        self.cursor = self.db.cursor()

    def _ensure_speedcam_table_initialized(self):
        self.cursor.execute("SHOW TABLES")

        table_name_strings = [row[0] for row in self.cursor]
        if "speedcams" not in table_name_strings:
            self._initialize_speedcam_table()

    def _initialize_speedcam_table(self):
        create_stmt = """
            CREATE TABLE speedcams (
                content BIGINT PRIMARY KEY NOT NULL,
                internal_id BIGINT UNIQUE NOT NULL AUTO_INCREMENT,
                lat DECIMAL(8, 6) NOT NULL,
                lng DECIMAL(8, 6) NOT NULL,
                backend VARCHAR(20) NOT NULL,
                id BIGINT,
                country CHAR(2),
                state CHAR(2),
                zip_code VARCHAR(8),
                city VARCHAR(50),
                type TINYINT,
                vmax SMALLINT,
                counter SMALLINT,
                created_date DATETIME,
                confirmed_date DATETIME,
                removed_date DATETIME,
                partly_fixed BOOLEAN,
                reason VARCHAR(200)
            ) ENGINE = InnoDB;
            """

        self.cursor.execute(create_stmt)

    def insert_speedcam(self, speedcam):
        self._insert_new_speedcams(self._json_speedcams_to_tuples(speedcam))

    def _insert_new_speedcams(self, speedcams):
        insert_stmt = """
            INSERT INTO speedcams (content, internal_id, lat, lng, backend, id,
                country, state, zip_code, city, type, vmax, counter, created_date,
                confirmed_date, removed_date, partly_fixed, reason)
            VALUES (%s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        self.cursor.executemany(insert_stmt, speedcams)
        self.db.commit()

    def _speedcam_exists_in_db(self, speedcam) -> bool:
        select_stmt = """
            SELECT COUNT(content)
            FROM speedcams
            WHERE content=%(content)s
        """

        self.cursor.execute(select_stmt, {"content": speedcam["content"]})
        return self.cursor.fetchall()[0][0] > 0

    def _json_speedcams_to_tuples(self, json_speedcams):
        tuples = list()

        for json_speedcam in json_speedcams:
            tuples.append((
                self._get_json_value_if_exists(json_speedcam, ["content"]),
                self._get_json_value_if_exists(json_speedcam, ["lat"]),
                self._get_json_value_if_exists(json_speedcam, ["lng"]),
                self._get_json_value_if_exists(json_speedcam, ["backend"]),
                self._get_json_value_if_exists(json_speedcam, ["id"]),
                self._get_json_value_if_exists(json_speedcam, ["address", "country"]),
                self._get_state_code(json_speedcam),
                self._get_json_value_if_exists(json_speedcam, ["address", "zip_code"]),
                self._get_json_value_if_exists(json_speedcam, ["address", "city"]),
                self._get_json_value_if_exists(json_speedcam, ["type"]),
                self._get_json_value_if_exists(json_speedcam, ["vmax"]),
                self._get_json_value_if_exists(json_speedcam, ["counter"]),
                parse(self._get_json_value_if_exists(json_speedcam, ["create_date"]), dayfirst=True, yearfirst=False),
                parse(self._get_json_value_if_exists(json_speedcam, ["confirm_date"]), dayfirst=True, yearfirst=False),
                None,  # removed date
                self._get_json_value_if_exists(json_speedcam, ["info", "partly_fixed"]),
                self._get_json_value_if_exists(json_speedcam, ["info", "reason"]),
            ))

        return tuples

    def _get_json_value_if_exists(self, json, path: list):
        for node in path:
            if node not in json:
                return None
            if type(json[node]) is bool:
                return None
            if json[node] == "":
                return None
            json = json[node]

        return json

    def _get_state_code(self, json_speedcam):
        state_code = self._get_json_value_if_exists(json_speedcam, ["address", "state"])

        if state_code is not None:
            return state_code[3:5]
        else:
            return None


def main():
    db = SpeedcamDB()
    filenames = sc_utils.get_json_filenames_in_dir("out_night")
    jsons = sc_utils.load_json_files(filenames)
    json_with_speedcams = jsons[0]
    db.insert_speedcam(json_with_speedcams)


if __name__ == '__main__':
    main()
