import os
import psycopg2


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('FSTR_DB_HOST', 'localhost'),
                port=os.getenv('FSTR_DB_PORT', '5432'),
                database=os.getenv('FSTR_DB_NAME', 'pereval'),
                user=os.getenv('FSTR_DB_LOGIN', 'postgres'),
                password=os.getenv('FSTR_DB_PASS', '')
            )
        except Exception as e:
            raise Exception(f"Ошибка подключения к базе данных: {e}")

    def close(self):
        if self.connection:
            self.connection.close()

    def create_pereval(self, data):
        try:
            with self.connection.cursor() as cursor:
                user_query = """
                INSERT INTO pereval_user (email, phone, fam, name, otc)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """
                cursor.execute(user_query, (
                    data['user']['email'],
                    data['user']['phone'],
                    data['user']['fam'],
                    data['user']['name'],
                    data['user']['otc']
                ))
                user_id = cursor.fetchone()[0]

                coords_query = """
                INSERT INTO pereval_coords (latitude, longitude, height)
                VALUES (%s, %s, %s)
                RETURNING id
                """
                cursor.execute(coords_query, (
                    data['coords']['latitude'],
                    data['coords']['longitude'],
                    data['coords']['height']
                ))
                coords_id = cursor.fetchone()[0]

                level_query = """
                INSERT INTO pereval_level (winter, summer, autumn, spring)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """
                cursor.execute(level_query, (
                    data['level']['winter'] or '',
                    data['level']['summer'] or '',
                    data['level']['autumn'] or '',
                    data['level']['spring'] or ''
                ))
                level_id = cursor.fetchone()[0]

                pereval_query = """
                INSERT INTO pereval_pereval 
                (beauty_title, title, other_titles, connect, add_time, 
                 user_id, coords_id, level_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """
                cursor.execute(pereval_query, (
                    data['beauty_title'],
                    data['title'],
                    data['other_titles'],
                    data['connect'],
                    data['add_time'],
                    user_id,
                    coords_id,
                    level_id,
                    'new'
                ))
                pereval_id = cursor.fetchone()[0]

                for image in data['images']:
                    image_query = """
                    INSERT INTO pereval_image (data, title, pereval_id)
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(image_query, (
                        image['data'],
                        image['title'],
                        pereval_id
                    ))

                self.connection.commit()
                return pereval_id

        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Ошибка при создании записи: {e}")

    def __del__(self):
        self.close()
