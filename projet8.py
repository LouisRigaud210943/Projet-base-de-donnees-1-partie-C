import sqlite3
import itertools
import copy

con = sqlite3.connect('database.db')

cur = con.cursor()
cur2 = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS FuncDep(table_name String, lhs String, rhs String)")

cur.execute("CREATE TABLE IF NOT EXISTS Vehicules(name String, tires_size String, cost int)")   #à supprimer
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

def Ask_Df_To_Del_And_Verify():
    df = []
    table_name = input("Enter a table name:\n")
    tab_name_exist_in_FuncDep = False
    while not tab_name_exist_in_FuncDep:
        for row in cur.execute("SELECT * FROM FuncDep"):
            tab_name_exist_in_FuncDep = tab_name_exist_in_FuncDep or row[0] == table_name
        if tab_name_exist_in_FuncDep == False:
            table_name = input("Please enter a valid table name:\n")
    df.append(table_name)
    lhs = input("Enter lhs:\n")
    lhs_exist_in_FuncDep = False
    while not lhs_exist_in_FuncDep:
        for row in cur.execute("SELECT * FROM FuncDep"):
            lhs_exist_in_FuncDep = lhs_exist_in_FuncDep or row[1] == lhs
        if lhs_exist_in_FuncDep == False:
            lhs = input("Please enter a valid lhs:\n")
    df.append(lhs)
    rhs = input("Enter rhs:\n")
    rhs_exist_in_FuncDep = False
    while not rhs_exist_in_FuncDep:
        for row in cur.execute("SELECT * FROM FuncDep"):
            rhs_exist_in_FuncDep = rhs_exist_in_FuncDep or row[2] == rhs
        if rhs_exist_in_FuncDep == False:
            rhs = input("Please enter a valid rhs:\n")
    df.append(rhs)
    return df

def Ask_LhsRhs_To_Add_And_Verify(table_name, update):
    lhs_rhs = []
    listOfCols = cur2.execute("SELECT * FROM " + table_name).description
    cols_tab = []
    for col in listOfCols:
        cols_tab.append(col[0])
    if update:
        lhs = input("Enter new lhs:\n")
    else:
        lhs = input("Enter lhs:\n")
    while lhs=="":
        lhs = input("Please enter an existing lhs:\n")
    non_existent_lhs = True
    while non_existent_lhs:
        lhs_string = ""
        non_existent_lhs = False
        for element in lhs.split():
            non_existent_lhs = non_existent_lhs or element not in cols_tab
            if lhs_string == "":
                lhs_string += element
            else:
                lhs_string += " " + element
        if non_existent_lhs == True:
            lhs = input("Please enter an existing lhs:\n")
    lhs_rhs.append(lhs_string)
    if update:
        rhs = input("Enter new rhs:\n")
    else:
        rhs = input("Enter rhs:\n")
    if rhs not in cols_tab:
        existing_rhs = False
        while existing_rhs == False:
            rhs = input("Please enter an existing rhs:\n")
            if rhs in cols_tab:
                existing_rhs = True
    lhs_rhs.append(rhs)
    return lhs_rhs

def Ask_Existing_Table():
    listOfTables = cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'").fetchall()
    table_name = input("Enter a table name:\n")
    if tuple(table_name.split()) not in listOfTables or table_name=="FuncDep":
        existing_table_name = False
        while existing_table_name == False:
            table_name = input("Please enter an existing table name:\n")
            if tuple(table_name.split()) in listOfTables and table_name!="FuncDep":
                existing_table_name = True
    return table_name.split()[0]

def Display_Choices():
    print("Enter 0 : Quit")
    print("Enter 1 : Show all functional dependencies")
    print("Enter 2 : Add a new functional dependencie")
    print("Enter 3 : Delete a functional dependencie")
    print("Enter 4 : Update a functional dependencie")
    print("Enter 5 : Show functional dependencies from a table")
    print("Enter 6 : Show unsatisfied functional dependencies")
    print("Enter 7 : Show redundant functional dependencies")
    print("Enter 8 : Show and delete useless or inconsistent functional dependencies")
    print("Enter 9 : Show keys") 
    return input("Please enter a number:\n")

value = Display_Choices()

while value != "0":
    if value == "1":
        if cur.execute("SELECT count(*) FROM FuncDep").fetchall()[0][0] == 0:
            print("There is no functional dependencies in FuncDep table")
        for row in cur.execute('SELECT * FROM FuncDep'):
            print(row)

    elif value == "2":
        update = False
        table_name = Ask_Existing_Table()
        lhs_rhs = Ask_LhsRhs_To_Add_And_Verify(table_name, update)
        Add(table_name, lhs_rhs[0], lhs_rhs[1]) 

    elif value == "3":
        if cur.execute("SELECT count(*) FROM FuncDep").fetchall()[0][0] == 0:
            print("There is no functional dependencies in FuncDep table")
        else:
            df = Ask_Df_To_Del_And_Verify()
            Delete(df[0], df[1], df[2])

    elif value == "4":
        if cur.execute("SELECT count(*) FROM FuncDep").fetchall()[0][0] == 0:
            print("There is no functional dependencies in FuncDep table")
        else:
            update = True
            df = Ask_Df_To_Del_And_Verify()
            Delete(df[0], df[1], df[2])
            lhs_rhs = Ask_LhsRhs_To_Add_And_Verify(df[0], update)
            Add(df[0], lhs_rhs[0], lhs_rhs[1])

    elif value == "5":
        table_name = Ask_Existing_Table()
        existing_df = False
        for row in cur.execute("SELECT * FROM FuncDep"):
            if row[0] == table_name:
                print(row)
                existing_df = True
        if not existing_df:
            print("There is no functional dependencies for this table")

    elif value == "6":
        listOfTables = cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'").fetchall()
        existing_df = False
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
                                existing_df = True
                                finish = True
                                break
        if not existing_df:
            print("There is no unsatisfied functional dependencies")

    elif value == "7":
        x = []
        existing_df = False
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
        if x != []:
            existing_df = True
        for y in x:
            print(y)

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
                                                print(row)
                                                existing_df = True
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
        if not existing_df:
            print("There is no redundant functional dependencies")

    elif value == "8":
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
            print("There is no useless or inconsistent functional dependencies")
        else:
            print("Here is all the useless or inconsistent functional dependencies:")
            for df in tab_df:
                print(df)
            print("")
            print("Which one do you want to delete ?")
            df_to_del = Ask_Df_To_Del_And_Verify()
            correct_df = False
            while correct_df == False:
                if tuple(df_to_del) not in tab_df:
                    print("Please enter a useless or inconsistent functional dependencie")
                    df_to_del = Ask_Df_To_Del_And_Verify()
                else:
                    correct_df = True
            Delete(df_to_del[0], df_to_del[1], df_to_del[2])

    elif value=="9":
        table_name = Ask_Existing_Table()
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
    else:
        print("Invalid number")
    print("")
    value = Display_Choices()

con.commit()

con.close()