from typing import Sequence

from mysql.connector import connect


class Database:
    def __init__(self, host, user, password, database):
        self.connection = connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

    def query(self, query, params=None):
        _cursor = self.connection.cursor()
        try:
            _cursor.execute(query, params or ())
            print('end query')
            return _cursor
        except Exception as e:
            print(e)

    def get(self, table: str, fields: Sequence[str] | str = '*', where: str = None, limit: int = None, values=None):
        query = f'SELECT {", ".join(fields)} FROM {table}'
        if where:
            query += f' WHERE {where} = %s'
        if limit:
            query += f' LIMIT {limit}'
        try:
            print(f'get {query=}')
            return self.query(query, values).fetchall()
        except Exception as e:
            return e

    def get_table_fields(self, table: str) -> list[str]:
        query = f"SHOW COLUMNS FROM {table}"
        print(f'{query=}')
        _cursor = self.query(query)
        return [row[0] for row in _cursor.fetchall()]

    def insert(self, table: str, fields: Sequence[str], values: Sequence[str]):
        query = f'INSERT INTO {table} ({", ".join(fields)}) VALUES ({", ".join(["%s" for _ in fields])})'
        print(f'{query=}', values)
        self.query(query, values)
        self.connection.commit()

    def update(self, table, fields: Sequence[str], values: Sequence[str], where: str):
        query = f'UPDATE {table} SET {", ".join([f"{field}=%s" for field in fields])} WHERE {where} = %s'
        print(f'{query=}', values)
        self.query(query, values)
        self.connection.commit()

    def delete(self, table: str, where: str, values: Sequence[str]):
        query = f'DELETE FROM {table} WHERE {where} = %s'
        self.query(query, values)
        print(f'{query=}', values)
        self.connection.commit()


# tests
if __name__ == "__main__":
    my_cursor = connect(
        host='localhost',
        user='erfan',
        password='erfanmysql',
        database='university',
    ).cursor()

    #     get student where dept_name is physics
    my_cursor.execute('SELECT * FROM student')
    print(my_cursor.fetchall())
