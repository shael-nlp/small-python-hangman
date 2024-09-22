def start():
    """
    Démarrage du jeu
    """
    print("Bienvenue dans la devinette de mots")
    # L'exercice demandant une difficulté et un fichier spécifique, ces variables sont programmées en "dur"
    # Mais elles pourraient être remplacées par des fonctions "input()" pour modifier les règles
    path = "lexique.txt"
    length = 5
    tries = 6
    # permet à l'utilisateur de vérifier les paramètres
    print(f"""Les paramètres suivants seront utilisés :
       - Localisation du fichier : 
    (dossier principal)/{path}
       - Longueur du mot : {length} lettres.
       - Tentatives : {tries} essais.
        (Entrer un mot inconnu du lexique ne fait pas perdre d'essai.)
    Bonne chance !""")

    # Extraction du contenu
    lexicon = extract_content(path)

    # Choix du mot
    word = word_pick(lexicon, length)

    # Neutralise les accents
    game_word = replace_special(word)

    # Démarre le jeu avec les paramètres suivant :
    # Le mot neutralisé "game_word"
    # Le mot original, "word" (pour une question d'affichage)
    # Le contenu non neutralisé "lexicon"
    # La longueur du mot "length"
    # Le nombre d'essais possible "tries"
    game_loop(game_word, word, lexicon, length, tries)


def extract_content(path):
    """
    Extraction du lexique depuis le fichier
    Remplacement des caractères spéciaux "œ" et "Œ"
    Traitement d'une potentielle erreur d'encodage sur demande de l'utilisateur
    """

    with (open(path, "r", encoding="utf-8") as f):
        # Compréhension de liste qui supprime les retour à la ligne dans le fichier
        lexicon = [line.rstrip() for line in f.readlines()]

        # Demande à l'utilisateur s'il souhaite faire une opération potentiellement instable
        answer = input("""* Voulez-vous traiter le problème d'encodage ? (OUI / NON)
* Cela pourrait causer un crash :
""").upper()

        # Dans le cas du traitement de l'encodage, compte le nombre de mots précédemment victime de l'erreur
        encode_count = 0

        # observation de chaque mot dans le lexique
        for word in lexicon:
            # Si le cas particulier "œ" est détecté
            # Hélas les mots comme "moelle" et "oeufs" contenus dans le lexique ont un problème d'encodage
            # La vérification reste quand même là
            for oe in "œŒ":
                if oe in word:
                    # Le caractère unique est remplacé par deux caractères
                    # Cette opération est faite ici pour ne pas gêner pendant le choix du mot
                    # Car le mot "gagne" un caractère
                    new_word = word.replace(oe, "oe")
                    # Suppression de l'ancien mot du contenu
                    lexicon.remove(word)
                    # Et ajout du nouveau
                    lexicon.append(new_word)
            if answer == "OUI":
                # Traitement du problème d'encodage
                # Le caractère "inconnu" a été copié depuis Notepad++
                # Il correspondrait spécifiquement aux erreurs d'encodage sur le caractère "œ"
                if "" in word:
                    # Remplacement du caractère par les deux lettres correspondantes
                    new_word = word.replace("", "oe")
                    lexicon.remove(word)
                    lexicon.append(new_word)
                    encode_count += 1

        # Avertis l'utilisateur que tout s'est bien passé, si la procédure a été lancée
        if encode_count > 0:
            print(f"""Encodage traité avec succès !
    mots traités : {encode_count} """)
        else:
            print("Le problème d'encodage n'a pas été traité.")

    # Fermeture du fichier et renvoi du contenu
    return lexicon


def word_pick(lexicon, length):
    """
    Sélection d'un mot au hasard, selon les paramètres
    """
    # Import local parce que la fonction "choice()" n'est pas utile en dehors de cette fonction
    from random import choice
    # Création d'une nouvelle liste locale qui contient uniquement les mots de 5 lettres
    word_pool = [word for word in lexicon if len(word) == length]
    # Tirage au sort
    word = choice(word_pool)
    return word


def replace_special(data):
    """
    Analyse et remplace les caractères spéciaux français
    """
    # Définition des caractères spéciaux français et de leurs remplaçants
    # Avec deux "string" pour la simplicité
    french_special = "àâäéèêëïîôöùûüÿÀÂÄÉÈÊËÏÎÔÖÙÛÜŸç"
    # Définition de leur équivalent sur le même index
    french_standard = "aaaeeeeiioouuuyAAAEEEEIIOOUUUYc"

    # Comme cette fonction va accueillir des mots ou une liste
    # Séparation de la fonction selon le type de contenu:

    # Si le type est un string simple
    if type(data) is str:
        # remplacement de "data" par "word" pour la clarté du code
        word = data
        # déclaration de new_word avant de procéder à la concaténation
        new_word = ""

        for i in range(len(word)):
            # vérification de toutes les lettres du mot dans le string des accents "french_special"
            if word[i] in french_special:
                # Remplacement de l'accent par le caractère neutralisé correspondant
                # Nouvelle variable string car les strings en Python sont immuables
                # ci-dessous, ajoute une lettre neutralisée à la place de l'accent
                new_word += french_standard[french_special.index(word[i])]
            else:
                # sinon, ajoute la lettre normale suivante
                new_word += word[i]

        # "Return" est conditionné au type pour la clarté du code (permet de garder le même nom de variable)
        # Sinon, on aurait pu en placer un seul à la fin
        return new_word

    # Si le type est une liste
    if type(data) is list:
        # déclaration d'une nouvelle liste pour pouvoir ajouter les mots
        # Je n'ai pas réussi à faire une compréhension de liste ici
        # mais c'est peut être possible
        new_data = []

        # Vérification de chaque mot de la liste
        for word in data:
            # même processus que pour le type "string" au dessus
            new_word = ""
            for i in range(len(word)):
                if word[i] in french_special:
                    new_word += french_standard[french_special.index(word[i])]
                else:
                    new_word += word[i]
            # ajout du mot à la nouvelle liste neutralisée qui sera renvoyée à la place du lexique original
            new_data.append(new_word)
        return new_data


# Fonction principale
def game_loop(word_neutralized, word, lexicon, length, tries):
    """
    fonction principale:
    - Lance la boucle qui va contenir la partie
    - Demande l'input utilisateur et vérifie sa validité
    - Maintiens plusieurs variables qui comptent les lettres "à jour"
    """

    print("_____N_E_W_______G_A_M_E_____")

    # Variable pour la boucle while qui contient la partie
    # Elle permet aussi de compter les essais
    game_tries = 0

    # Définition des listes pour les lettres saisies
    # "not_found" pour les lettres qui ne sont pas dans le mot
    not_found = []

    # "partial_char" pour les lettres partiellement correctes mais au mauvais endroit
    partial_char = []

    # "match_char" pour les lettres trouvées à la bonne position
    match_char = []

    # Création des "étoiles" en fonction de la longueur du mot définie dans les règles pour l'afficher sur l'écran
    game_screen = ("* " * length)

    # Boucle while principale qui vérifie que l'utilisateur n'a pas perdu
    while game_tries < tries:

        # définition de la variable qui permet d'éviter de répéter l'affichage toutes les données
        # à chaque erreur d'input dans la boucle "while" plus bas
        invalid_input = True

        # Prévient l'utilisateur si celui-ci est à son dernier essai
        # "game_tries + 1" parce qu'il faut prévenir l'utilisateur un tour avant la fin !
        if game_tries + 1 == tries:
            print(f"""Entrez un mot de {length} lettres :
! Attention, un seul essai restant !
        {game_screen}""")

        # Sinon, affichage du message normal
        else:
            print(f"""Entrez un mot de {length} lettres :   ({tries - game_tries} essais restants)
        {game_screen}""")

        # Conditions "if" pour empêcher l'affichage du texte si la variable est vide
        if not_found:
            print("Lettres non présentes dans le mot :", ' '.join(not_found))
        if partial_char:
            print("Lettres présentes dans le mot, mais mal placées :", ' '.join(partial_char))
        if match_char:
            print("Lettres trouvées :", ' '.join(match_char))

        # Boucle pour la vérification de l'input utilisateur
        while invalid_input:

            # l'input de l'utilisateur est immédiatement neutralisé et mis en minuscules
            player_input = (replace_special(input())).lower()

            # Si le joueur veut abandonner, il peut entrer la commande "?"
            if player_input == "?":
                # Utilisation du mot original "word" pour conserver les accents
                print(f"""Vous avez abandonné.
Le mot était '{word.capitalize()}'.
_____________________________________________""")
                # Redémarrage de la partie
                restart()

            # Vérifie que l'input utilisateur fait bien la bonne longueur
            # Affichage de l'aide "(entrez "?" pour quitter)" au bout d'un essai raté seulement
            # C'est un choix graphique pour ne pas encombrer l'écran
            elif len(player_input) != length:
                print(f"""Erreur : le mot doit être composé de {length} lettres, réessayez : 
(ou entrez '?' pour quitter)""")

            # Vérifie que l'input utilisateur fait parti du lexique neutralisé
            elif player_input not in replace_special(lexicon):
                print("""Erreur, mot inconnu du lexique, réessayez :
(ou entrez '?' pour quitter)""")

            # Si le mot est valide
            else:
                # l'input utilisateur est maintenant valide, il sera renvoyé au début
                invalid_input = False

                # Déclenchement de la comparaison entre l'input utilisateur et le mot mystère
                # Renvoie deux dictionnaires, une pour les lettres trouvées "match"
                # l'autre pour les lettres partiellement trouvées "partial"
                # Les dictionnaires ont pour clé l'index, et comme valeur la lettre trouvée dans le mot
                # Cette fonction est définie plus bas.
                match, partial = compare(player_input, word_neutralized)

                # Les trois listes ci-dessous fournissent les lettres déjà utilisées à l'utilisateur
                # Dans le texte au début de la boucle

                # Extraction depuis les valeurs du dictionnaire
                for char in match.values():
                    match_char.append(char)

                # Conversion en "set" pour supprimer les doublons
                # Puis conversion en "list" pour utiliser la fonction "sorted"
                match_char = sorted(list(set(match_char)))

                for char in partial.values():
                    partial_char.append(char)
                partial_char = sorted(list(set(partial_char)))

                # Pour les lettres qui ne correspondent pas
                # Seulement les lettres restantes de l'input utilisateur sont ajoutées
                for char in player_input:
                    # Si la lettre n'est dans aucun des dictionnaire précédent
                    if char not in match.values() and char not in partial.values():
                        # ajoute la lettre dans la liste
                        not_found.append(char)
                not_found = sorted(list(set(not_found)))

                # Mise à jour des "étoiles" sur l'écran
                # Cette fonction est définie plus bas
                game_screen = update_screen(game_screen, match, partial)

                # Création d'une variable qui met toutes les lettres
                # de l'écran en minuscule pour la comparaison ci-dessous
                game_screen_lower = game_screen.lower()

                # Itération des caractères dans la liste partial_char, qui contient des caractères uniques
                for char1 in partial_char:
                    # Si la lettre est déjà trouvée
                    # et que cette lettre est comptée autant de fois (ou plus) sur l'écran que sur le mot mystère
                    # Alors la ou les lettres sont bien placées et déjà trouvée
                    if char1 in match_char and word_neutralized.count(char1) <= game_screen_lower.count(char1):
                        # on peut donc supprimer cette lettre de la liste "partial_char"
                        # Pour ne pas tromper l'utilisateur sur les lettres restantes à trouver
                        partial_char.remove(char1)
                        # suppression de ce caractère s'il est toujours sur l'écran sous la forme minuscule
                        game_screen = game_screen.replace(char1, "*")

                # Augmente le compteur d'essais, ce qui rapproche le joueur du maximum d'essais
                # si la valeur est "length" est dépassée, l'utilisateur sort entièrement de la boucle
                game_tries += 1

        # Vérifie si le mot qui remplace les étoiles correspond au mot mystère
        # Si c'est le cas, le joueur a gagné
        if game_screen.replace(" ", "").lower() == word_neutralized:
            print(f"""_____________________________________________
Félicitations, vous avez remporté la partie !
Vous avez trouvé '{word.capitalize()}' en {game_tries} essais.
_____________________________________________""")
            # Redémarrage de la partie
            # Cette fonction est définie plus bas
            restart()

    # Si l'utilisateur a utilisé trop d'essais, il sort de la boucle et arrive ici
    print(f"""Désolé, vous n'avez plus d'essais.
Vous avez perdu. Dommage !
_____________________________________________
Le mot était '{word.capitalize()}'.""")
    # Redémarrage du jeu
    restart()


def compare(user_input, word):
    """
    Recherche de correspondance
    user_input/word, renvoie
    {lettres_trouvées}, {lettres_presque_trouvées}
    défini {index : str}
    """
    # définition des dictionnaires ici pour simplifier la syntaxe plus bas
    match = {}
    partial_match = {}

    # fonction enumerate() pour récupérer l'index et la lettre sur une seule ligne
    for i, char in enumerate(user_input):
        # si la lettre est au bon endroit
        if char == word[i]:
            # une clé est créé sous la forme {index : lettre}
            match[i] = char
        # sinon, si la lettre est au moins dans le mot
        elif char in word:
            # une clé est créé avec le même format
            partial_match[i] = char
        # les autres lettres sont ignorées

    # Renvoie les dictionnaires
    return match, partial_match


def update_screen(game_screen, match, partial):
    """
    Remplace les étoiles par les lettres
    Ou remet des étoiles là où c'est nécessaire
    """

    # Pour ne pas saturer l'écran
    # J'ai fait le choix d'effacer les caractères trouvés mais mal placés au bout d'un tour
    # Ils sont quand même conservés dans la liste "partial"
    # pour que l'utilisateur possède toujours l'information lors des essais suivants

    # Si le caractère est une minuscule, il est remplacé par une étoile.
    game_screen = ['*' if char.islower() else char for char in game_screen]

    # Si la lettre est juste, elle remplace tout, même une ancienne lettre
    for i, char in match.items():
        # L'index est multiplié par deux, car "l'écran" contient un espace après chaque étoile
        # la lettre est également mise en majuscule
        game_screen[i * 2] = char.upper()
    # Si la lettre est partiellement juste
    for i, char in partial.items():
        # Cette lettre ne peut que remplacer une étoile, par sécurité
        if game_screen[i * 2] == "*":
            game_screen[i * 2] = char

    # Reconversion de l'écran en string
    game_screen = ''.join(game_screen)

    return game_screen


def restart():
    """
    Redémarre la partie ou ferme le programme
    - est exécutée quand la partie est finie
    - peu importe l'issue de celle-ci
    """
    # Par simplicité, j'ai choisi de faire une boucle "infinie" et d'utiliser la fonction exit
    while True:
        print("Voulez vous rejouer avec les mêmes paramètres ? (OUI / NON)")
        # L'input est converti en majuscules
        # Pour que l'utilisateur puisse écrire oui ou non en minuscules
        answer = input("").upper()
        if answer == "OUI":
            # Si l'utilisateur veut rejouer, retour à la fonction initiale
            start()
        elif answer == "NON":
            # Sinon, la fonction "exit()" met fin au programme
            exit()
        else:
            print("Commande non reconnue, utilisez 'OUI' ou 'NON'")


# Démarrage du programme
if __name__ == '__main__':
    start()
