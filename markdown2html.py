#!/usr/bin/python3
"""Un script pour convertir des fichiers écrits en langage Markdown en fichiers HTML"""

import hashlib
import os
import re
import sys


def replace_bold(match):
    """Une fonction qui retourne une chaîne en gras formatée en HTML"""
    bold_text = match.group(1)
    return f'<b>{bold_text}</b>'


def replace_em(match):
    """Une fonction qui retourne une chaîne en italique formatée en HTML"""
    em_text = match.group(1)
    return f'<em>{em_text}</em>'


def encode_md5(match):
    """Une fonction qui retourne une chaîne encodée en MD5"""
    text_to_encode = match.group(1)
    return hashlib.md5(text_to_encode.encode()).hexdigest()


def remove_c(match):
    """Une fonction qui retourne une chaîne sans les caractères 'c'"""
    text_with_c = match.group(1)
    return text_with_c.replace('c', '').replace('C', '')


def main():
    """La fonction principale qui exécute le script

    Soulève:
            "Usage: ./markdown2html.py README.md README.html" dans STDERR:
            Si le nombre d'arguments dans la CLI est différent de 2
            "Fichier <nom_du_fichier> manquant" dans STDERR: Si le fichier Markdown n'existe pas
    """

    # Vérifie si le nombre d'arguments CLI est correct
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    # Vérifie si le fichier markdown existe
    if not os.path.isfile(md_file):
        print(f"Fichier manquant {md_file}", file=sys.stderr)
        sys.exit(1)

    # Analyse le fichier markdown et écrit le HTML dans un nouveau fichier HTML
    with open(md_file, "r", encoding='UTF-8') as markdown:
        with open(html_file, "w", encoding='UTF-8') as html:

            # Balises HTML
            ol_open = False
            ul_open = False
            p_open = False

            # Modèles spéciaux
            pattern_bold = re.compile(r'\*\*(.*?)\*\*')
            pattern_em = re.compile(r'__(.*?)__')
            pattern_md5 = re.compile(r'\[\[(.*?)\]\]')
            pattern_c = re.compile(r'\(\((.*?)\)\)')

            # La boucle pour analyser le fichier
            while True:
                line = markdown.readline()

                # Vérifie si on est dans une liste non ordonnée
                if ul_open and not line.startswith("-"):
                    html.write("</ul>\n")
                    ul_open = False

                # Vérifie si on est dans une liste ordonnée
                if ol_open and not line.startswith("* "):
                    html.write("</ol>\n")
                    ol_open = False

                # Vérifie si on est dans un paragraphe
                if p_open and (line.startswith("-") or
                               line.startswith("* ,") or
                               line.startswith("#") or
                               line.startswith("\n")):
                    html.write("</p>\n")
                    p_open = False

                # Atteint la fin du fichier (EOF)
                if not line:
                    break

                # Évalue et modifie le contenu de la ligne avec les balises em, bold, md5, et enlève les caractères "c"
                line = re.sub(pattern_bold, replace_bold, line)
                line = re.sub(pattern_em, replace_em, line)
                line = re.sub(pattern_md5, encode_md5, line)
                line = re.sub(pattern_c, remove_c, line)

                # Génère les titres
                if line.startswith("#"):
                    count = line.count("#")
                    text = line.rsplit('# ', 1)[1].strip()
                    html.write(f"<h{count}>{text}</h{count}>\n")

                # Génère une liste non ordonnée
                elif line.startswith("-"):
                    if not ul_open:
                        html.write("<ul>\n")
                        ul_open = True
                    text = line.rsplit('- ', 1)[1].strip()
                    html.write(f"<li>{text}</li>\n")

                # Génère une liste ordonnée
                elif line.startswith('* '):
                    if not ol_open:
                        html.write("<ol>\n")
                        ol_open = True
                    text = line.rsplit('*
