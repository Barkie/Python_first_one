import sqlite3
from bottle import route, run, template

@route('/mac')
def mac():
    db = sqlite3.connect('c:/python/db_test/sw.db')
    c = db.cursor()
    c.execute("SELECT File_name, Hostname, Vlan, Mac_Address, Interface, Dev_Vendor FROM MAC")
    data = c.fetchall()
    c.close()
    output = template('c:/python/git/mac.tpl', rows=data)
    return output

run(host='localhost', port=8080)
