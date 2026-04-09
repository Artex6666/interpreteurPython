# Interpréteur mini-langage (ESGI 3A)
___
Baptise COQUET - Loris RAMEAU

## 🗂️ Arborescence du projet

___

```txt
src/
│
├── ast_lang/
│   ├── node/
│   └── statement/
│
├── grammar/
│
├── runtime/
│   ├── values/
│   ├── exception/
│   └── trace/
│
└── graph_ast/
```
___

## 📁 Contenu détaillé des dossiers
___

### 📦 `ast_lang/node/` --- Nœuds d'expression

|         Fichier         |                      Rôle                      |
|:-----------------------:|:----------------------------------------------:|
|      `__init__.py`      |           Initialisation du package            |
|     `args_node.py`      |       Liste d'arguments lors d'un appel        |
|    `binary_node.py`     | Opérations binaires(`+`,`-`,`*`,`%`,`==`,etc.) |
|     `bool_node.py`      |                Littéral booléen                |
|     `call_node.py`      |               Appel de fonction                |
|     `float_node.py`     |               Littéral flottant                |
|     `group_node.py`     |               Parenthèse `(...)`               |
|     `name_node.py`      |             identifiant (variable)             |
 |      `number_node`      |                Littéral entier                 |
|    `params_node.py`     |              Liste de paramètres               |
|    `pointer_node.py`    |               Déférencement `*x`               |
 | `pointer_param_node.py` |            Paramètre pointeur `*x`             |
|      `ref_node.py`      |                 Référence `&x`                 |
|    `string_node.py`     |                Littéral chaîne                 |
|     `unary_node.py`     |               Opérations unaires               |    
___

### 📦 `ast_lang/statement/` --- Nœuds d'instructions

|         Fichier          |                 Rôle                 |
|:------------------------:|:------------------------------------:|
|      `__init__.py`       |      Initialisation du package       |
|     `assign_node.py`     |        Affectation `x = expr`        |
|     `block_node.py`      |             Bloc `{...}`             |
|      `elif_node.py`      |            Branche `elif`            |
|      `else_node.py`      |            Branche `else`            |
|     `empty_node.py`      |           Instruction vide           | 
|    `expression_node`     | Expression utilisée comme statement  |
|      `for_node.py`       |             Boucle `for`             |
|      `func_node.py`      |        Definition de fonction        |
|       `if_node.py`       |           Instruction `if`           |
| `pointer_assign_node.py` | Affectation via pointeur `*x = expr` |
|     `print_node.py`      |      Instruction `print(expr)`       |
|     `return_node.py`     |         Instruction `return`         |
|     `while_node.py`      |            Boucle `while`            |
___

### 📦 `grammar/` --- Analyse lexicale et syntaxique

|    Fichier    |           Rôle            |
|:-------------:|:-------------------------:|
| `__init__.py` | Initialisation du package |
|  `lexer.py`   | Découpe le code en tokens |
|  `parser.py`  |  Construit l'AST via PLY  |
___

### 📦 `runtime/` --- Exécution du langage

|        Fichier         |              Rôle              |
|:----------------------:|:------------------------------:|
|     `__init__.py`      |   Initialisation du package    |
|      `runtime.py`      |      Evaluateur principal      |
| `runtime_exception.py` |  Exception runtime générique   |
|       `stack.py`       | Gestion de la pile d'exécution |
|       `frame.py`       |   Frame d'exécution (scope)    |

___

### 📁 `runtime/values/` --- Types runtime
|     Fichier      |           Rôle            |
|:----------------:|:-------------------------:|
|  `__init__.py`   | Initialisation du package |
|  `calc_bool.py`  |       Type booléen        |
| `calc_float.py`  |       Type flottant       |
|  `calc_null.py`  |         Type null         |
| `calc_number.py` |        Type entier        |
| `calc_string.py` |        Type chaîne        |
|  `reference.py`  |   Gestion des pointeurs   |
___

### 📁 `runtime/exception/` --- Exceptions spécialisées

|             Fichier             |           Rôle            |
|:-------------------------------:|:-------------------------:|
|          `__init__.py`          | Initialisation du package |
|    `attribute_exception.py`     |     Attribut invalide     | 
| `division_by_zero_exception.py` |     Division par zéro     |
|       `name_exception.py`       |     Variable inconnue     | 
|      `value_exception.py`       |      Valeur invalide      |
|       `type_exception.py`       |       Type invalide       |
___

### 📁 `runtime/trace/` --- Stack trace
|     Fichier      |               Rôle               |
|:----------------:|:--------------------------------:|
|  `__init__.py`   |    Initialisation du package     |
| `stack_trace.py` |    Trace complète d'éxécution    |
| `trace_frame.py` | Frame individuelle dans la trace |
___

### 📁 `graph_ast/` --- Visualisation AST

|         Fichier          |                   Rôle                   |
|:------------------------:|:----------------------------------------:|
|      `__init__.py`       |        Initialisation du package         |
| `genereTreeGraphviz2.py` | Génération d'un graphe Graphviz de l'AST |
___

## Exemple de code 
### 🔎 Test d'une condition :

```
x = 15; if(x > 10) { print("x est plus grand que 10 : "+x); } elif( x == 10 ) { print( "x vaut : " + x); } else { print("x est plus petit que 10 : " + x);};
```
___

### 🔁 Boucle `while`:

```
i = 0; while (i < 5) {  print(i);  i = i + 1; };
```
___

### 🔁 Boucle `for`:

```
for (i = 0; i < 5; i = i + 1) { print(i); };
```
___

### 🧮 Fonction `hello` qui ne retourne aucun type
```
def hello(name){print("Hello " + name);};
```
___

### 🧮 Fonction `is_even` qui retourne un type

```
def is_even(x){ return (x%2) == 0;};
```
___

### 🌀 Fonction récursive `fibo`

```
def fibo(x){ if(x == 0 || x == 1){  return x; }; return fibo(x-1) + fibo(x-2); };
```
___

### 🌀 Fonction récursive terminale `fibo_ter`

```
def fibo_ter(n, som, som2){  if (n != 1){ return fibo_ter(n-1, som+som2, som); };  return som; };
```
___

### 🔄 Fonction `swap` sans pointeurs
```
def swap_copy(x,y){ temp = x; x = y; y = temp; };
```
___

### 🔄 Fonction `swap` avec pointeurs
```
def swap(*x, *y) { temp = *x; *x = *y;  *y = temp; };
```
___

### 🔍 Exemple : différence entre variable globale et locale 
```
x = 10;  def f() {     x = 99;     print(x); };  f(); print(x); 
```

___

### Tableaux (littéral, indexation, affectation)
```
t = [1, 2, 3];
print(t);
print(t[0]);
t[1] = 42;
print(t);

u = [[1,2],[3,4]];
print(u[1]);
print(u[1][0]);
```
___

## 📁 Contenu détaillé des dossiers
___

### 📦 `ast_lang/node/` --- Nœuds d'expression

|         Fichier         |                      Rôle                      |
|:-----------------------:|:----------------------------------------------:|
|      `__init__.py`      |           Initialisation du package            |
|     `args_node.py`      |       Liste d'arguments lors d'un appel        |
|    `binary_node.py`     | Opérations binaires(`+`,`-`,`*`,`%`,`==`,etc.) |
|     `bool_node.py`      |                Littéral booléen                |
|     `call_node.py`      |               Appel de fonction                |
|     `float_node.py`     |               Littéral flottant                |
|     `group_node.py`     |               Parenthèse `(...)`               |
|     `name_node.py`      |             identifiant (variable)             |
 |      `number_node`      |                Littéral entier                 |
|    `params_node.py`     |              Liste de paramètres               |
|    `pointer_node.py`    |               Déférencement `*x`               |
 | `pointer_param_node.py` |            Paramètre pointeur `*x`             |
|      `ref_node.py`      |                 Référence `&x`                 |
|    `string_node.py`     |                Littéral chaîne                 |
|     `unary_node.py`     |               Opérations unaires               |    
___

### 📦 `ast_lang/statement/` --- Nœuds d'instructions

|         Fichier          |                 Rôle                 |
|:------------------------:|:------------------------------------:|
|      `__init__.py`       |      Initialisation du package       |
|     `assign_node.py`     |        Affectation `x = expr`        |
|     `block_node.py`      |             Bloc `{...}`             |
|      `elif_node.py`      |            Branche `elif`            |
|      `else_node.py`      |            Branche `else`            |
|     `empty_node.py`      |           Instruction vide           | 
|    `expression_node`     | Expression utilisée comme statement  |
|      `for_node.py`       |             Boucle `for`             |
|      `func_node.py`      |        Definition de fonction        |
|       `if_node.py`       |           Instruction `if`           |
| `pointer_assign_node.py` | Affectation via pointeur `*x = expr` |
|     `print_node.py`      |      Instruction `print(expr)`       |
|     `return_node.py`     |         Instruction `return`         |
|     `while_node.py`      |            Boucle `while`            |
___

### 📦 `grammar/` --- Analyse lexicale et syntaxique

|    Fichier    |           Rôle            |
|:-------------:|:-------------------------:|
| `__init__.py` | Initialisation du package |
|  `lexer.py`   | Découpe le code en tokens |
|  `parser.py`  |  Construit l'AST via PLY  |
___

### 📦 `runtime/` --- Exécution du langage

|        Fichier         |              Rôle              |
|:----------------------:|:------------------------------:|
|     `__init__.py`      |   Initialisation du package    |
|      `runtime.py`      |      Evaluateur principal      |
| `runtime_exception.py` |  Exception runtime générique   |
|       `stack.py`       | Gestion de la pile d'exécution |
|       `frame.py`       |   Frame d'exécution (scope)    |

___

### 📁 `runtime/values/` --- Types runtime
|     Fichier      |           Rôle            |
|:----------------:|:-------------------------:|
|  `__init__.py`   | Initialisation du package |
|  `calc_bool.py`  |       Type booléen        |
| `calc_float.py`  |       Type flottant       |
|  `calc_null.py`  |         Type null         |
| `calc_number.py` |        Type entier        |
| `calc_string.py` |        Type chaîne        |
|  `reference.py`  |   Gestion des pointeurs   |
___

### 📁 `runtime/exception/` --- Exceptions spécialisées

|             Fichier             |           Rôle            |
|:-------------------------------:|:-------------------------:|
|          `__init__.py`          | Initialisation du package |
|    `attribute_exception.py`     |     Attribut invalide     | 
| `division_by_zero_exception.py` |     Division par zéro     |
|       `name_exception.py`       |     Variable inconnue     | 
|      `value_exception.py`       |      Valeur invalide      |
|       `type_exception.py`       |       Type invalide       |
___

### 📁 `runtime/trace/` --- Stack trace
|     Fichier      |               Rôle               |
|:----------------:|:--------------------------------:|
|  `__init__.py`   |    Initialisation du package     |
| `stack_trace.py` |    Trace complète d'éxécution    |
| `trace_frame.py` | Frame individuelle dans la trace |
___

### 📁 `graph_ast/` --- Visualisation AST

|         Fichier          |                   Rôle                   |
|:------------------------:|:----------------------------------------:|
|      `__init__.py`       |        Initialisation du package         |
| `genereTreeGraphviz2.py` | Génération d'un graphe Graphviz de l'AST |
___

## Exemple de code 
### 🔎 Test d'une condition :

```
x = 15; if(x > 10) { print("x est plus grand que 10 : "+x); } elif( x == 10 ) { print( "x vaut : " + x); } else { print("x est plus petit que 10 : " + x);};
```
___

### 🔁 Boucle `while`:

```
i = 0; while (i < 5) {  print(i);  i = i + 1; };
```
___

### 🔁 Boucle `for`:

```
for (i = 0; i < 5; i = i + 1) { print(i); };
```
___

### 🧮 Fonction `hello` qui ne retourne aucun type
```
def hello(name){print("Hello " + name);};
```
___

### 🧮 Fonction `is_even` qui retourne un type

```
def is_even(x){ return (x%2) == 0;};
```
___

### 🌀 Fonction récursive `fibo`

```
def fibo(x){ if(x == 0 || x == 1){  return x; }; return fibo(x-1) + fibo(x-2); };
```
___

### 🌀 Fonction récursive terminale `fibo_ter`

```
def fibo_ter(n, som, som2){  if (n != 1){ return fibo_ter(n-1, som+som2, som); };  return som; };
```
___

### 🔄 Fonction `swap` sans pointeurs
```
def swap_copy(x,y){ temp = x; x = y; y = temp; };
```
___

### 🔄 Fonction `swap` avec pointeurs
```
def swap(*x, *y) { temp = *x; *x = *y;  *y = temp; };
```
___

### 🔍 Exemple : différence entre variable globale et locale 
```
x = 10;  def f() {     x = 99;     print(x); };  f(); print(x); 
```