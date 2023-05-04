import pymysql

#### MAIN DB CONNECTION ####
def connect():
    connection = pymysql.connect(host='bryanmarshall.com',
                                 port=3306,
                                 database='dbuzxie9rljc8i',
                                 user='u1ikgtowhsaic',
                                 password='az69mszhgsr8',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("Connected")
    return connection