import sqlite3
import itertools
import copy

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
print("Enter 6 : show redundant functional dependencies")

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
        finish = False
        x = []
        cur.execute("SELECT " + row[1] + " FROM " + row[0])
        x += [cur.fetchall()]
        cur.execute("SELECT " + row[2] + " FROM " + row[0])
        x += [cur.fetchall()]
        for y in range(len(x[0])):
            if finish:
                break
            else:
                for z in range(len(x[0])):
                    if x[0][z] == x[0][y] and x[1][z] != x[1][y]:
                        print(row)
                        finish = True
                        break

elif value == "6":
    x = []
    compteur = 0
    for row in cur.execute("SELECT * FROM FuncDep"):
        compteur += 1
        compteur2 = 0
        for row2 in cur2.execute("SELECT * FROM FuncDep"):
            compteur2 += 1
            if compteur < compteur2:
                if row[0] == row2[0] and sorted(row[1].split()) == sorted(row2[1].split()) and row[2] == row2[2]:
                    if row2 not in x:
                        x.append(row2)
    for y in x:
        print(y)
        #ad -> b    bd -> e
        #adc -> e
        
    for row in cur.execute("SELECT * FROM FuncDep"):
        tab=[row]
        #print(row)
        x = row[1].split()
        again=True
        while(again==True):
            #print("while")
            x_old=copy.deepcopy(x)
            #print(x_old)
            c=0
            for row2 in cur2.execute("SELECT * FROM FuncDep"):
                if row2 not in tab:
                    c+=1
            if c==0:
                again=False
            if row[2] in x :
                #print("redundant")
                #print(row)
                again=False
            #print("OK")
            for y in range(0, len(x)+1):
                #print("ok2")
                for z in itertools.combinations(x, y):
                    #print(row)
                    #print(z)
                    #print(row)
                    for row2 in cur2.execute("SELECT * FROM FuncDep"):
                        #print(row2)
                        if row2 not in tab and row[0] == row2[0]:
                            #print(sorted(row2[1].split())==sorted(list(z)))
                            #print(sorted(list(z)))
                            if sorted(row2[1].split()) == sorted(list(z)):
                                #print(row2[1].split())
                                #print(list(z))
                                #print(row2[2])
                                #print(row[2])
                                for l in x:
                                   if row2[2] not in x:
                                       x.append(row2[2])
                                       #print(x)
                                       #print("jpp")
                                       #print(row[2] in x)
                                       if row[2] in x :
                                           print("redundant")
                                           print(row)
                                           again=False
                                           x_old=x
                                tab.append(row2)
                                #print(tab)
                                #break
                                    
            #print("message")
            #print("x_old")
            #print(x_old)
            #print(x)
            if x_old!=x:
                again=True
            else:
                again=False

con.commit()

con.close()
