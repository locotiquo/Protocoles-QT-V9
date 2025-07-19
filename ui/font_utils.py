from PySide6.QtGui import QFont
from ui.filtrage import filtrer_motifs

def appliquer_taille_police(self, sender=None):
    # Si sender fourni, récupère la taille dans sender.data()
    if sender and sender.data():
        self.taille_police = sender.data()
    else:
        self.taille_police = 12

    # Met à jour les cases cochées dans le menu
    for action in self.taille_actions:
        action.setChecked(action.data() == self.taille_police)

    font = QFont("Helvetica", self.taille_police)
    self.tree.setFont(font)

    if hasattr(self, 'bilans_tab'):
        self.bilans_tab.set_font_size(self.taille_police)

    if hasattr(self, 'plateau_tab'):
        self.plateau_tab.set_font_size(self.taille_police)

    # Relance le filtrage pour appliquer la nouvelle taille
    filtrer_motifs(self)

    self.status_bar.showMessage(f"Taille de police : {self.taille_police} pt", 3000)
    self.afficher_etat_options()


def afficher_etat_options(self):
    etats = [
        f"Images {'✅' if self.afficher_images.isChecked() else '❌'}",
        f"Couleurs {'✅' if self.afficher_couleurs.isChecked() else '❌'}",
        f"Police {'✅' if self.afficher_mise_en_forme.isChecked() else '❌'}",
        f"Taille {self.taille_police}"
    ]
    self.status_right_label.setText(" | ".join(etats))
