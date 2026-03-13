import sys

from genereTreeGraphviz2 import printTreeGraph
from grammar import parse
from logic import eval_program


def lire_source_depuis_stdin():
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
    return "\n".join(lignes)


def lire_source_depuis_fichier(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        print(f"Impossible de lire le fichier '{path}': {e}")
        return ""


def main():
    # Si un chemin est passé en argument, on lit depuis ce fichier,
    # sinon on passe en mode interactif (STDIN).
    if len(sys.argv) >= 2:
        source = lire_source_depuis_fichier(sys.argv[1])
    else:
        source = lire_source_depuis_stdin()

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