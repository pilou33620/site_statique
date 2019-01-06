import os
from os import listdir
from os.path import isfile, join, splitext
import click
import re

@click.command()

@click.option('--input_directory', '-i', help ="Dossier des fichier source (./ par défaut)", default=".")
@click.option('--output_directory', '-o', help ="Sous-dossier de destination (./site par défaut)", default="site")
@click.option('--template_directory', '-t', help ="Dossier contenant le template html et css (./un dossier)", default="./")
@click.option('--log_level', '-l', help ="Niveau de verbosité des logs (Nombre entier positif)", default=1)


def main(input_directory, output_directory, template_directory, log_level):

    def log_message(message, niveau):
        if niveau<int(log_level):
            print(message)

    src = [file for file in listdir(input_directory) if re.match(r'.*\.md', file)]

    log_message("Le dossier des sources est ["+str(input_directory+"]"), 2)
    log_message("Le dossier destination est ["+str(output_directory+"]"), 2)
    log_message("Le dossier des template est ["+str(template_directory+"]"), 2)

    log_message("Liste des fichiers à traiter : "+str(src), 0)

    mdpath=0
    src_md=0
    target_html=0

    title1 = re.compile("^# ")
    title2 = re.compile("^## ")
    title3 = re.compile("^### ")
    puce = re.compile("^\* ")
    para = re.compile("[A-Z]")

    def emphase(line):
        bold=0
        ital=0
        strong=0

        #trouver la position du mark
        #split la chaine
        #effacer le mark
        #vérifier si c'est la balise de début ou de fin
        #rassembler la chaine avec la bonne balise

        return line

    def structure(line, list):
        log_message(str(list), 5)
        if re.match(puce, line):
            log_message("Element de chaine", 4)
            line = 4*" "+"<ul>"+line[2:-1]+"</ul>"
            if list == 0:
                list=1
                line = "<li>\n"+line
            else:
                pass
        else:
            if re.match(title1, line):
                log_message("Titre 1", 4)
                line = "<h1>"+line[2:-1]+"</h1>"
            elif re.match(title2, line):
                log_message("Titre 2", 4)
                line = "<h2>"+line[3:-1]+"</h2>"
            elif re.match(title3, line):
                log_message("Titre 3", 4)
                line = "<h3>"+line[4:-1]+"</h3>"
            elif re.match(para, line):
                log_message("Chaine normale", 4)
                line = "<p>"+line[:-1]+"</p>"
            else:
                return 0, list
            log_message("Rien", 4)
            if list == 1:
                list=0
                line = "</li>\n"+line
            else:
                pass
        return line, list


    for mdfile in src:
        mdpath = str(input_directory) + "/" + mdfile
        src_md = open(mdpath, "r")
        target = os.path.splitext(mdfile)[0]
        target = target + ".html"
        target =  str(input_directory) + "/" + str(output_directory) + "/" + target
        if not os.path.exists(str(input_directory) + "/" + str(output_directory)):
            os.makedirs(str(input_directory) + "/" + str(output_directory))
        target_html = open(target, "w")

        list=0
        log_message("Début conversion ["+str(mdfile)+"]", 1)
        for line in src_md:
            log_message(str(line[:-1]), 3)
            new_line, list=structure(line, list)

            if new_line:
                log_message(new_line, 3)
                target_html.write(new_line+"\n")
            else:
                pass
        log_message("Conversion finie ["+str(target)+"]", 0)
        src_md.close()
        target_html.close()

    log_message("Les fichiers html sont disponible dans : ["+str(output_directory+"]"), 0)

# Converti un fichier markdown en fichier html

if __name__ == "__main__":
    main()
