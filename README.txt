Projet de « Bases de Données I »
Dépendances fonctionnelles et normalisation

Explication du programme:

1) Introduire le nom de la base de données que l'on compte utiliser.
2) Introduire le numéro correspondant à l'action que l'on veut réaliser.
3) Le numéro 0 permet de quitter le programme.
4) Le numéro 1 permet d'afficher toutes les dépendances fonctionnelles (DF) présentes dans la table "FuncDep" qui regroupe toutes les DF de la base de données.
5) Le numéro 2 permet d'ajouter une DF à la table "FuncDep", en donnant le triplet (table_name, lhs, rhs) qui représente la DF lhs -> rhs dans la table "table_name".
6) Le numéro 3 permet d'effacer une DF à la table "FuncDep", en donnant le triplet (table_name, lhs, rhs) que l'on souhaite supprimer.
7) Le numéro 4 permet de modifier une DF en introduisant le triplet (table_name, lhs, rhs) ainsi que le nouveau "lhs" et le nouveau "rhs".
8) Le numéro 5 permet d'afficher toutes les DF d'une table contenues dans la table "FuncDep".
9) Le numéro 6 permet d'afficher toutes les DF insatisfaites contenues dans la table "FuncDep".
10) Le numéro 7 permet d'afficher toutes les DF redondantes contenues dans la table "FuncDep".
11) Le numéro 8 permet d'afficher toutes les DF inutiles et incohérentes contenues dans la table "FuncDep". Il est ensuite obligatoire de supprimer une de ces DF.
12) Le numéro 9 permet d'afficher toutes les clefs d'une table, en introduisant le nom de la table concernée.
13) Le numéro 10 permet de vérifier si la base de données respecte la norme BCNF.
14) Le numéro 11 permet de vérifier si la base de données respecte la norme 3NF.

Attention, en cas de fermeture forçée, les données modifiées ne seront pas sauvegardées.