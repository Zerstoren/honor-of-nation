# import pymysql as sql
# from sys import exit
#
# import config
# dbConnect = sql.connect(
#     host=config.get('database.mysql.host') if config.get('database.mysql.host') != 'default' else '127.0.0.1',
#     user=config.get('database.mysql.user'),
#     passwd=config.get('database.mysql.pass'),
#     db=config.get('database.mysql.base')
# )
#
# # if dbConnect: dbConnect.set_character_set('UTF8')
#
# class Mysql:
#     cursor = False
#     db = False
#
#     def __init__(self, cursor):
#         self.cursor = cursor
#         self.db = dbConnect
#
#     def numRows(self):
#         return self.cursor.rowcount
#
#     def result(self):
#         names = [x[0].lower() for x in self.cursor.description]
#         data = []
#         for row in self.cursor:
#             data.append(dict(zip(names, row)))
#
#         return data
#
#     def row(self):
#         names = [x[0].lower() for x in self.cursor.description]
#         for row in self.cursor:
#             return dict(zip(names, row))
#
#     def insertId(self):
#         return dbConnect.insert_id()
#
#     # def __del__(self):
#     #     self.cursor.close()
#     #     del self.cursor
#
#
# def query(sql, data=(), showQuery = False):
#     """
#     :type sql: str
#     """
#
#     if type(data) == 'str':
#         data = dbConnect.escape(data)
#
#     elif type(data) == 'tuple':
#         for i in range(len(data)):
#             data[i] = dbConnect.escape(data[i])
#
#     cur = dbConnect.cursor()
#
#     try:
#         cur.execute(sql.strip() % data)
#
#         if(showQuery):
#             print(sql.strip() % data)
#
#         return Mysql(cur)
#
#     except Exception as e:
#         print(e)
#         print("{Mysql error}")
#         print(sql.strip() % data)
#         exit(500)
#
# db = query
