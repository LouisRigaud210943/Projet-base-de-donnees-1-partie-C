import sqlite3

con = sqlite3.connect('database.db')

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS FuncDep(table_name String, lhs String, rhs String)")

def Add(table_name, lhs, rhs) :
    cur.execute('INSERT INTO FuncDep VALUES (?, ?, ?)', (table_name, lhs, rhs))
    return None

def Delete(table_name, l, r) :
    cur.execute("DELETE FROM FuncDep Where table_name = ? AND lhs = ? AND rhs = ?", (table_name, l, r))
    return None

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
    for row in cur.execute("SELECT * FROM FuncDep"):
        #à implémenter
        print(row)
    
for row in cur.execute('SELECT * FROM FuncDep'):
    print(row)

con.commit()

con.close()