from tkinter import ttk


def styleTreview():
    # 1. Création et configuration globale du Style (À mettre juste avant self.tree)
    style = ttk.Style()
    style.theme_use(
        "default"
    )  # Force le thème par défaut pour pouvoir le personnaliser

    # Personnalisation de la police des lignes de données (Le corps du tableau)
    style.configure(
        "Treeview",
        font=("Segoe UI", 8),  # ← CHOISIS TA POLICE ET TA TAILLE ICI
        background="#1e1e2e",  # Couleur de fond des cellules
        fieldbackground="#1e1e2e",  # Couleur de fond globale du composant
        foreground="white",  # Couleur du texte
        rowheight=20,  # Hauteur des lignes (optionnel, utile si tu augmentes la taille de la police)
        rowwidth=100,  # Largeur des lignes (optionnel, peut être ajusté pour un look plus épuré)
    )

    # Personnalisation de la police des En-têtes (Les titres des colonnes)
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),  # ← CHOISIS TA POLICE DE TITRE ICI
        background="#313244",  # Couleur de fond des en-têtes
        foreground="white",  # Couleur du texte des en-têtes
    )
