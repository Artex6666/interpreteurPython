from genereTreeGraphviz2 import printTreeGraph

from grammar import parse
from logic import eval_program


def main():
    print("Entrez votre programme (ligne vide pour terminer) :")
    lignes = []
    while True:
        try:
            ligne = input()
        except EOFError:
            break
        if ligne.strip() == "":
            break
        lignes.append(ligne)

    source = "\n".join(lignes)

    if not source.strip():
        print("Aucun programme fourni.")
        return

    ast = parse(source)
    print("AST :", ast)
    printTreeGraph(ast)

    print("\n--- Exécution ---")
    eval_program(ast)


if __name__ == "__main__":
    main()