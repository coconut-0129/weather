from utils import query

def get_user(account, password):
    sql = "select id from user where account= '" + account + "' and password= '" + password + "'"
    res = query(sql)
    return res
