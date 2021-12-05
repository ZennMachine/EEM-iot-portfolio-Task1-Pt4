import sqlite3
from datetime import datetime

from sqlalchemy import Column,String,Integer,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class EnvironmentTPH(Base):
    __tablename__ = "tph_storage"
    id = Column(Integer, primary_key=True)
    device_name = Column(String)
    device_mac = Column(String)
    device_serial = Column(String)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    created_at = Column(DateTime)

    def __init__(self):
        self.device_name = "UNKNOWN"
        self.device_mac = "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"
        self.device_serial = "UNKNOWN"
        self.temperature = 60
        self.humidity = 50
        self.pressure = 110
        self.created_at = Column(DateTime)

class CPU(Base):
    __tablename__ = "processor_statistics"
    id = Column(Integer, primary_key=True)
    device_name = Column(String)
    device_mac = Column(String)
    device_serial = Column(String)
    load = Column(Float)
    cpu_temp = Column(Float)
    gpu_temp = Column(Float)
    created_at = Column(DateTime)

    def __init__(self):
        self.device_name = "UNKNOWN"
        self.device_mac = "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"
        self.device_serial = "UNKNOWN"
        self.load = -999.99
        self.cpu_temp = -999.99
        self.gpu_temp =  -999.99

class Storage(Base):
    __tablename__ = 'device_storage'
    id = Column(Integer, primary_key=True)
    host_name = Column(String)
    host_mac = Column(String)
    total_storage = Column(Integer)
    free_storage = Column(Integer)
    used_storage = Column(Integer)
    created_at = Column(DateTime)

    def __init__(self):
        self.host_name = "UNKNOWN"
        self.host_mac = "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"
        self.created_at = datetime.now()
        self.total_storage = None
        self.free_storage = None
        self.used_storage = None


class Database:
    def __init__(self, filename, table_name='cpu_loads'):
        self.__filename = filename
        self.__table_name = table_name

    def __execute(self, query):
        """
        Convenience method that opens connection, retrieves a cursor,
        executes a query, then closes the connection.

        SHOUOLD NOT be used for queries that fetch actual data.
        """
        connection = sqlite3.connect(self.__filename)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def __retrieve(self, query, json=False):
        """
        Convenience method that opens connection, retrieves a cursor,
        executes a query, retrieves the query results, closes the
        connection, and then returns results

        SHOULD NOT be used for actions that modify database, tables or data.
        """
        connection = sqlite3.connect(self.__filename)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        count = 0
        if json:
            # Create an array of dictionaries
            results = []
            for row in rows:
                # For each row in the rows,
                # Grab the table's field names (from SQLite) and
                # (using ZIP) associate each field name with the
                # corresponding value from  the row
                # Then append the dictionary to the results list
                results.append(dict(zip(
                    [c[0] for c in cursor.description], row)))
        else:
            # Create an "indexed" dictionary
            results = {}
            for row in rows:
                # For each row in the rows,
                # Grab the table's field names (from SQLite) and
                # (using ZIP) associate each field name with the
                # corresponding value from  the row
                # Then create a dictionary of the resulting row with a
                # unique ID for the resulting row of data.
                results[count] = dict(zip(
                    [c[0] for c in cursor.description], row))
                count += 1
        connection.close()
        return results

    def create(self):
        """
        Method that creates database table if not already exists.
        """
        query = f'CREATE TABLE IF NOT EXISTS {self.__table_name} (' \
                '    [id] INTEGER PRIMARY KEY,' \
                '    [load] DECIMAL,' \
                '    [created_at] DATETIME' \
                ')'

        self.__execute(query)

    def store(self, value):
        """
        Method that stores a single data value into the table.
        """
        query = f'INSERT INTO {self.__table_name} ' \
                f'    VALUES (null, {value}, datetime())'
        self.__execute(query)

    def get_last(self, value="10", json=False):
        """
            This method returns the last <value> items of stored data.
            For example, calling `get_last(13)` will return the last
            thirteen items of recorded data.

            :param value:   An Integer
            :param json:    A boolean identifying if results to be JSON, or a
                            Dictionary
            :return:        JSON | Dictionary
        """
        try:
            if not value.isnumeric():
                value = 10
        except AttributeError:
            value = abs(int(value))
        else:
            value = abs(int(value))

        query = f"SELECT * FROM {self.__table_name}" \
                f"    ORDER BY created_at DESC" \
                f"    LIMIT {value}"
        return self.__retrieve(query, json=json)

    def get_in_last(self, value="1", period="MINUTES", json=False):
        """
        This method returns the data that was in the last <value> <period>.
        For example, calling `get_in_last(3,"seconds")` will return the last
        three seconds of recorded data.

        :param value:   An Integer
        :param period:  A value from Seconds, Minutes, Hours, Days, Weeks,
                        Months and Years
        :param json:    A boolean identifying if results to be JSON, or a
                        Dictionary
        :return:        JSON | Dictionary
        """
        period = period.upper()
        if period not in (
                'SECONDS', 'MINUTES', 'HOURS', 'DAYS',
                'WEEKS', 'MONTHS', 'YEARS'):
            period = 'MINUTES'
        try:
            if not value.isnumeric():
                value = -1
        except AttributeError:
            value = -abs(int(value))
        else:
            value = -abs(int(value))

        query = f"SELECT * FROM {self.__table_name}" \
                f"    WHERE created_at > datetime('now', '{value} {period}')" \
                f"    ORDER BY created_at DESC"
        return self.__retrieve(query, json=json)
