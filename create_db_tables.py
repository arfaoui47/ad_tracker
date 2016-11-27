from configparser import ConfigParser
import MySQLdb


def db_connection(config):
    connexion = MySQLdb.connect(host=config.get('MySQL', 'host'),
                                user=config.get('MySQL', 'user'),
                                passwd=config.get('MySQL', 'password'),
                                db=config.get('MySQL', 'db'))

    return connexion


def create_database(config):
    connexion = MySQLdb.connect(host=config.get('MySQL', 'host'),
                                user=config.get('MySQL', 'user'),
                                passwd=config.get('MySQL', 'password'),)
    cursor = connexion.cursor()
    cursor.execute('CREATE DATABASE {};'.format(config.get('MySQL', 'db')))


def create_images_table(connexion):
    cursor = connexion.cursor()
    cursor.execute("""CREATE TABLE images (
                    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    checksum VARCHAR(256),
                    date_creation datetime,
                    url VARCHAR(250),
                    website VARCHAR(100),
                    file_type VARCHAR(50))""")


if __name__ == '__main__':
    config = ConfigParser()
    config.read('conf.ini')
    try:
        create_database(config)
    except:
        pass
    conn = db_connection(config)
    create_images_table(conn)
