import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="test",
  password="test"
)

c = conn.cursor()

c.execute("CREATE DATABASE IF NOT Exists smartroster")
conn.commit()
conn.close()

cnx = mysql.connector.connect(user='test',
                             password='test',
                             host='localhost',
                             database='smartroster')
cursor =cnx.cursor()

def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except :
            pass

executeScriptsFromFile('SQLImportFiles/smartroster_nurses.sql')
executeScriptsFromFile('SQLImportFiles/smartroster_patients.sql')
executeScriptsFromFile('SQLImportFiles/smartroster_patient_nurse_assignments.sql')
executeScriptsFromFile('SQLImportFiles/smartroster_users.sql')    
executeScriptsFromFile('SQLImportFiles/smartroster_adv_role_assignments.sql')
executeScriptsFromFile('SQLImportFiles/smartroster_reference_page.sql')
cnx.commit()
cnx.close()