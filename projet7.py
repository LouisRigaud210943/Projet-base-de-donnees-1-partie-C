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
print("Enter 7 : show and delete useless or inconsistent functional dependencies")
print("Enter 8 : show keys") 

value = input("Please enter a number:\n")

if value == "1":
    listOfTables = cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'").fetchall()
    table_name = input("Enter table_name:\n")
    if tuple(table_name.split()) not in listOfTables or table_name=="FuncDep":
        existing_table_name = False
        while existing_table_name == False:
            table_name = input("Please enter an existing table_name:\n")
            if tuple(table_name.split()) in listOfTables and table_name!="FuncDep":
                existing_table_name = True
    listOfCols = cur2.execute("SELECT * FROM " + table_name).description
    cols_tab = []
    for col in listOfCols:
        cols_tab.append(col[0])
    lhs = input("Enter lhs:\n")
    while lhs=="":
        lhs = input("Please enter an existing lhs:\n")
    for element in lhs.split():
        if element not in cols_tab:
            existing_lhs = False
            while existing_lhs == False:
                existing_lhs = True
                lhs = input("Please enter an existing lhs:\n")
                for element in lhs.split():
                    existing_lhs = existing_lhs and element in cols_tab
    rhs = input("Enter rhs:\n")
    if rhs not in cols_tab:
        existing_rhs = False
        while existing_rhs == False:
            rhs = input("Please enter an existing rhs:\n")
            if rhs in cols_tab:
                existing_rhs = True
    Add(table_name, lhs, rhs) 

elif value == "2":
    table_name = input("Enter table_name:\n")
    tab_name_exist_in_FuncDep = False
    while not tab_name_exist_in_FuncDep:
        for row in cur.execute("SELECT * FROM FuncDep"):
            tab_name_exist_in_FuncDep = tab_name_exist_in_FuncDep or row[0] == table_name
        if tab_name_exist_in_FuncDep == False:
            table_name = input("Please enter a valid table_name:\n")
    lhs = input("Enter lhs:\n")
    lhs_exist_in_FuncDep = False
    while not lhs_exist_in_FuncDep:
        for row in cur.execute("SELECT * FROM FuncDep"):
            lhs_exist_in_FuncDep = lhs_exist_in_FuncDep or row[1] == lhs
        if lhs_exist_in_FuncDep == False:
            lhs = input("Please enter a valid lhs:\n")
    rhs = input("Enter rhs:\n")
    rhs_exist_in_FuncDep = False
    while not rhs_exist_in_FuncDep:
        for row in cur.execute("SELECT * FROM FuncDep"):
            rhs_exist_in_FuncDep = rhs_exist_in_FuncDep or row[2] == rhs
        if rhs_exist_in_FuncDep == False:
            rhs = input("Please enter a valid rhs:\n")
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
    for row in cur.execute("SELECT * FROM FuncDep"):
        if row[0] == table_name:
            print(row)
        
elif value == "5":
    listOfTables = cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'").fetchall()
    for row in cur2.execute("SELECT * FROM FuncDep"):
        if tuple(row[0].split()) in listOfTables:
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

elif value == "7":
    tab_df = []
    listOfTables = cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'").fetchall()
    compt_tab = []
    compt = 0
    for row in cur.execute("SELECT * FROM FuncDep"):
        compt += 1
        if tuple(row[0].split()) not in listOfTables:
            tab_df.append(row)
            compt_tab.append(compt)
        else:
            listOfCols = cur2.execute("SELECT * FROM " + row[0]).description
            cols_tab = []
            for col in listOfCols:
                cols_tab.append(col[0])
            if row[2] not in cols_tab:
                tab_df.append(row)
                compt_tab.append(compt)
            else:
                for element in tuple(row[1].split()):
                    if element not in cols_tab:
                        tab_df.append(row)
                        compt_tab.append(compt)
                        break

    compt2 = 0
    for row in cur2.execute("SELECT * FROM FuncDep"):
        compt2 += 1
        if compt2 not in compt_tab:
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
                            if row not in tab_df:
                                tab_df.append(row)
                            finish = True
                            break
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

    for row in cur.execute("SELECT * FROM FuncDep"):
        tab=[row]
        x = row[1].split()
        again=True
        while(again==True):
            x_old=copy.deepcopy(x)
            c=0
            for row2 in cur2.execute("SELECT * FROM FuncDep"):
                if row2 not in tab:
                    c+=1
            if c==0:
                again=False
            if row[2] in x :
                again=False
            for y in range(0, len(x)+1):
                for z in itertools.combinations(x, y):
                    for row2 in cur2.execute("SELECT * FROM FuncDep"):
                        if row2 not in tab and row[0] == row2[0]:
                            if sorted(row2[1].split()) == sorted(list(z)):
                                for l in x:
                                    if row2[2] not in x:
                                        x.append(row2[2])
                                        if row[2] in x :
                                            if row not in tab_df:
                                                tab_df.append(row)
                                            again=False
                                            x_old=x
                                tab.append(row2)
            if x_old!=x:
                again=True
            else:
                again=False

    if tab_df == []:
        print("Il n'existe aucune DF inutile ou incohérente")
    else:
        print("Voici toutes les DF inutiles ou incohérentes:")
        for df in tab_df:
            print(df)
        print("")
        print("Laquelle voulez-vous supprimer ?")
        table_name = input("Enter table_name:\n")
        lhs = input("Enter lhs:\n")
        rhs = input("Enter rhs:\n")
        Delete(table_name, lhs, rhs)

elif value=="8":
    table_name=input("Pour quelle table\n")
    cur.execute('SELECT * from '+table_name)
    x=[description[0] for description in cur.description]
    keys=[]
    print(x)
    for y in range(0, len(x)+1):
        for z in itertools.combinations(x, y):
            z_new=copy.deepcopy(list(z))
            again=True
            while(again==True):
                z_new_new=copy.deepcopy(list(z_new))
                for row in cur.execute("SELECT * FROM FuncDep"):
                    if row[1] in z_new:
                        if row[2] not in z_new:
                            z_new.append(row[2])
                if z_new_new==z_new:
                    again=False
                if sorted(z_new)==sorted(x):
                    if len(keys)>0:
                        if len(z)==len(keys[0]):
                            keys.append(z)
                    else:
                        keys.append(z)
                    again=False
    print(keys)

con.commit()

con.close()