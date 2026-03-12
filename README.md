## Interpréteur mini-langage (ESGI 3A)


Baptise COQUET - Loris RAMEAU


### Fichiers

Répartition en 3 fichiers:

- **exo.py** : point d’entrée, lit le programme sur l’entrée standard, affiche l’AST, appelle l’interpréteur.
- **grammar.py** : définition du lexer et de la grammaire PLY, construction de l’AST.
- **logic.py** : logique d’exécution (interpréteur) à partir de l’AST.

### Fonctionnalités implémentées
- **Variables** : noms à plusieurs caractères, affectation simple `x = 4;`.
- **Expressions numériques** : `+ - * /`, parenthèses, utilisation de variables.
- **Affichage** : `print(expr);` affiche `calc > <valeur>`.
- **Conditionnels** : `if(cond) stmt;`, `if(cond) stmt else stmt;` avec `<` et `==`.
- **Boucles** : `while(cond){...}` et `for(i = a to b){...}`.
- **Fonctions** :
  - `fonctionVoid nom(p1, p2){ ... }` (sans valeur de retour).
  - `fonctionValue nom(p1, p2){ ... }` (avec `return` explicite ou retour implicite via une variable du nom de la fonction).
  - Appels de fonctions comme instruction ou expression : `toto(3, 5);`, `x = toto(3, 5);`.



Exemple simple :


   ```text
   x=4;x=x+3;print(x);
   
   ```
