import sqlite3

con = sqlite3.connect('database.db')

cur = con.cursor()
cur2 = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS FuncDep(table_name String, lhs String, rhs String)")

cur.execute("CREATE TABLE IF NOT EXISTS Vehicules(name String, tires_size String, cost int)")
#cur.execute('INSERT INTO Vehicules VALUES ("voiture", "grande", 10000)')
#cur.execute('INSERT INTO Vehicules VALUES ("velo", "petite", 1000)')
#cur.execute('INSERT INTO Vehicules VALUES ("moto", "moyenne", 1000)')
#cur.execute('INSERT INTO Vehicules VALUES ("voiture", "grande", 11000)')

def Add(table_name, lhs, rhs) :
    cur.execute('INSERT INTO FuncDep VALUES (?, ?, ?)', (table_name, lhs, rhs))
    return None

def Delete(table_name, l, r) :
    cur.execute("DELETE FROM FuncDep Where table_name = ? AND lhs = ? AND rhs = ?", (table_name, l, r))
    return None
    
for row in cur.execute('SELECT * FROM FuncDep'):
    print(row)

print("Enter 1 : add a new row")
print("Enter 2 : delete a row")
print("Enter 3 : update a row")
print("Enter 4 : show functional dependencies from a table")
print("Enter 5 : show unsatisfied functional dependencies")

value = input("Please enter a number:\n")

if value == "1":
    table_name = input("Enter table_name:\n")
    lhs = input("Enter lhs:\n")
    rhs = input("Enter rhs:\n")
    Add(table_name, lhs, rhs) 

elif value == "2":
    table_name = input("Enter table_name:\n")
    lhs = input("Enter lhs:\n")
    rhs = input("Enter rhs:\n")
    Delete(table_name, lhs, rhs)

elif value == "3":
    table_name = input("Enter the table_name you want to update:\n")
    lhs = input("Enter old lhs:\n")
    rhs = input("Enter old rhs:\n")
    Delete(table_name, lhs, rhs)
    lhs = input("Enter new lhs:\n")
    rhs = input("Enter new rhs:\n")
    Add(table_name, lhs, rhs)
    
elif value == "4":
    table_name = input("Enter table_name:\n")
    for row in cur.execute('SELECT * FROM FuncDep Where table_name = ?', (table_name)):
        print(row)
        
elif value == "5":
    for row in cur2.execute("SELECT * FROM FuncDep"):
        x = []
        cur.execute("SELECT " + row[1] + " FROM " + row[0])
        x += [cur.fetchall()]
        cur.execute("SELECT " + row[2] + " FROM " + row[0])
        x += [cur.fetchall()]
        print(x)
        for y in range(len(x[0])):
            if x[0][0] == x[0][y] and x[1][0] != x[1][y]:
                print("attention")
            else:
                print("ok")
        #x = []
        #rows = [row[1][0] for row[1] in cur.execute("SELECT " + row[1] + " FROM " + row[0])]
        #print(rows)
        #for row2 in cur.execute("SELECT * FROM " + row[0]):
        #    lhs_value = cur.execute("SELECT " + row[1] + " FROM " + row2.fetchall())
        #    rhs_value = cur.execute("SELECT ? FROM ?", (row[2], row2))
        #    for row3 in cur.execute("SELECT * FROM ?", (row[0])):
        #        lhs_value2 = cur.execute("SELECT ? FROM ?", (row[1], row3))
        #        rhs_value2 = cur.execute("SELECT ? FROM ?", (row[2], row3))
        #        if lhs_value == lhs_value2:
        #            if rhs_value != rhs_value2:
        #                print(row)
    
#for row in cur.execute('SELECT * FROM FuncDep'):
#    print(row)

con.commit()

con.close()