import os
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


def chemin_fichier_sortie():
    os.makedirs("output", exist_ok=True)
    if len(sys.argv) >= 2:
        base = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        nom = f"{base}_output.txt"
    else:
        nom = "stdin_output.txt"
    return os.path.join("output", nom)


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
    output = eval_program(ast)

    # Écriture de tous les messages d'exécution dans un fichier dans output/
    path_out = chemin_fichier_sortie()
    with open(path_out, "w", encoding="utf-8") as f:
        for line in output.lines:
            f.write(line + "\n")
    print(f"Sortie d'exécution écrite dans : {path_out}")


if __name__ == "__main__":
    main()