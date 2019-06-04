import psycopg2
import screte_database.screte_db_login as login


def main(filename):
    db_conn = psycopg2.connect(dbname=login.db_name, user=login.username,
                                 password=login.password, host=login.host, port=login.port)
    db_cursor = db_conn.cursor()

    content = '## users \n\n id | username | password | first_name | last_name | registration_time | ip_address | pri_key |\n' \
              + ':----: |' * 8 + '\n'

    db_cursor.execute("SELECT * FROM users")
    users = db_cursor.fetchall()
    content += '\n'.join([' | '.join([str(el) for el in row]) for row in users])

    content += '\n\n ## contacts \n\n user1_id | user2_id |\n' + ':----: |' * 2 + '\n'
    db_cursor.execute("SELECT * FROM contacts")
    contacts = db_cursor.fetchall()
    content += '\n'.join([' | '.join([str(el) for el in row]) for row in contacts])

    content += '\n\n ## pictures \n\n id | from_user_id | to_user_id | had_been_read | info_from_user |\n' + ':----: |' * 5 + '\n'
    db_cursor.execute("SELECT * FROM pictures")
    pictures = db_cursor.fetchall()
    content += '\n'.join([' | '.join([str(el) for el in row]) for row in pictures])

    content += '\n\n ## sessions \n\n id | user_id | start_time | finish_time | num_enc | num_dec |\n' + ':----: |' * 6 + '\n'
    db_cursor.execute("SELECT * FROM sessions")
    sessions = db_cursor.fetchall()
    content += '\n'.join([' | '.join([str(el) for el in row]) for row in sessions])

    with open(filename, 'w') as file:
        file.write(content)


if __name__ == "__main__":
    main('db_inside.md')
