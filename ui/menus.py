from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction

def creer_menus(parent):
    menu_bar = QMenuBar(parent)

    fichier_menu = menu_bar.addMenu("Fichier")
    fichier_menu.addAction("Effacer la recherche", parent.effacer_recherche)
    fichier_menu.addSeparator()
    fichier_menu.addAction("Quitter", parent.close)

    options_menu = menu_bar.addMenu("Options")
    parent.afficher_couleurs = QAction("Afficher les couleurs", parent, checkable=True, checked=True)
    parent.afficher_images = QAction("Afficher les images", parent, checkable=True, checked=True)
    parent.afficher_mise_en_forme = QAction("Afficher la mise en forme police", parent, checkable=True, checked=True)
    for a in [parent.afficher_couleurs, parent.afficher_images, parent.afficher_mise_en_forme]:
        a.triggered.connect(parent.filtrer_motifs)
        a.triggered.connect(parent.afficher_etat_options)
        options_menu.addAction(a)

    taille_menu = options_menu.addMenu("Taille police")
    parent.taille_actions = []
    for taille in range(8, 25, 2):
        action = QAction(f"{taille} {'(défaut)' if taille==12 else ''}", parent, checkable=True)
        action.setData(taille)
        action.triggered.connect(lambda checked=False, a=action: parent.appliquer_taille_police(a))
        parent.taille_actions.append(action)
        taille_menu.addAction(action)
    parent.taille_actions[2].setChecked(True)

    aide_menu = menu_bar.addMenu("Aide")
    aide_menu.addAction("À propos", parent.ouvrir_fenetre_info)

    return menu_bar
