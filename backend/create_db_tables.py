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
    with connexion:
        cursor = connexion.cursor()
        cursor.execute('CREATE DATABASE {};'.format(config.get('MySQL', 'db')))


def create_images_table(connexion):
    with connexion:
        cursor = connexion.cursor()
        cursor.execute("""CREATE TABLE images (
                        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                        checksum VARCHAR(256),
                        date_creation datetime,
                        url VARCHAR(250),
                        website VARCHAR(100),
                        file_type VARCHAR(50),
                        original_url VARCHAR(500),
                        authorized VARCHAR(50),
                        descreption VARCHAR(500))""")


def create_sites_table(connexion):
    with connexion:
        cursor = connexion.cursor()
        cursor.execute("""CREATE TABLE websites (
                        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                        domain_name VARCHAR(256))""")


def create_adtracking_table(connexion):
    with connexion:
        cursor = connexion.cursor()
        cursor.execute("""CREATE TABLE adtracking (
                        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                        checksum VARCHAR(256),
                        date_creation datetime,
                        location VARCHAR(256))""")


def insert_existing_websites(connexion):
    with connexion:
        cursor = connexion.cursor()
        with open('url_list.txt', 'r') as f:
            url_list = f.read().splitlines()
            for url in url_list:
                try:
                    cursor.execute("""INSERT INTO websites (domain_name)
                            VALUES ({})""".format(repr(url)))
                    connexion.commit()
                except:
                    print '[-] Failed insert to DB'
                    connexion.rollback()


def find_all_websites(connexion):
    with connexion:
        cursor = connexion.cursor()
        cursor.execute('''SELECT * FROM websites''')
        result = cursor.fetchall()
    return [i[1] for i in result]


if __name__ == '__main__':
    config = ConfigParser()
    config.read('conf.ini')
    try:
        create_database(config)
    except:
        pass
    conn = db_connection(config)
    create_images_table(conn)
    create_sites_table(conn)
    insert_existing_websites(conn)
    create_adtracking_table(conn)
