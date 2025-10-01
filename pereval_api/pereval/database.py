import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


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
            print("Успешное подключение к базе данных")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")

    def create_pereval(self, data):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
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
                user_id = cursor.fetchone()['id']

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
                coords_id = cursor.fetchone()['id']

                level_query = """
                INSERT INTO pereval_level (winter, summer, autumn, spring)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """
                cursor.execute(level_query, (
                    data['level']['winter'],
                    data['level']['summer'],
                    data['level']['autumn'],
                    data['level']['spring']
                ))
                level_id = cursor.fetchone()['id']

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
                    datetime.now(),
                    user_id,
                    coords_id,
                    level_id,
                    'new'
                ))
                pereval_id = cursor.fetchone()['id']

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
            print(f"Ошибка при создании записи: {e}")
            raise

    def get_pereval(self, pereval_id):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT p.*, u.*, c.*, l.*,
                       (SELECT json_agg(json_build_object('data', i.data, 'title', i.title))
                        FROM pereval_image i WHERE i.pereval_id = p.id) as images
                FROM pereval_pereval p
                JOIN pereval_user u ON p.user_id = u.id
                JOIN pereval_coords c ON p.coords_id = c.id
                JOIN pereval_level l ON p.level_id = l.id
                WHERE p.id = %s
                """
                cursor.execute(query, (pereval_id,))
                return cursor.fetchone()

        except Exception as e:
            print(f"Ошибка при получении записи: {e}")
            raise