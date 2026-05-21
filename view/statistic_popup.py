import customtkinter as ctk
import tkinter as tk
import numpy as np  # Nécessaire pour positionner les barres en 3D
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatisticPopup(ctk.CTkToplevel):
    def __init__(self, parent, eleve_controller):
        super().__init__(parent)
        self.title("Statistiques — Situation financière")
        self.geometry("880x600")
        self.resizable(False, False)
        self.update()
        self.grab_set()
        self.eleve_controller = eleve_controller
        
        # --- ÉTAT DU GRAPHIQUE ---
        # Options disponibles : "Camembert", "Barres 2D", "Barres 3D"
        self.type_graphique = "Camembert"  

        # --- TITRE ---
        ctk.CTkLabel(
            self,
            text="Situation financière des élèves",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#89b4fa",
        ).pack(pady=(20, 5))

        # --- BOUTON DE CHANGEMENT DE FORME ---
        self.btn_switch = ctk.CTkButton(
            self,
            text="Changer la forme (Barres 2D)",
            command=self._basculer_forme,
            fg_color="#89b4fa",
            text_color="#1e1e2e",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            width=220,
            height=28
        )
        self.btn_switch.pack(pady=(0, 10))

        # --- FRAME GRAPHIQUE ---
        self.graph_frame = ctk.CTkFrame(self, fg_color="#2b2b3b", corner_radius=15)
        self.graph_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self._afficher_graphique()

        # --- BOUTON FERMER ---
        ctk.CTkButton(
            self,
            text="Fermer",
            command=self.destroy,
            fg_color="#f38ba8",
            text_color="black",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            width=120,
        ).pack(pady=(5, 20))

    def _basculer_forme(self):
        """Alterne cycliquement entre Camembert -> Barres 2D -> Barres 3D."""
        if self.type_graphique == "Camembert":
            self.type_graphique = "Barres 2D"
            self.btn_switch.configure(text="Changer la forme (Barres 3D)")
        elif self.type_graphique == "Barres 2D":
            self.type_graphique = "Barres 3D"
            self.btn_switch.configure(text="Changer la forme (Camembert)")
        else:
            self.type_graphique = "Camembert"
            self.btn_switch.configure(text="Changer la forme (Barres 2D)")
        
        # Nettoyage et reconstruction
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        self._afficher_graphique()

    def _afficher_graphique(self):
        eleves = self.eleve_controller.recuperer_tous_les_eleves()

        if not eleves:
            ctk.CTkLabel(
                self.graph_frame,
                text="Aucune donnée disponible.",
                font=("Segoe UI", 13),
                text_color="#cdd6f4",
            ).pack(expand=True)
            return

        # Comptage par situation
        comptage = {}
        for eleve in eleves:
            situation = eleve.get("situation_financiere", "Inconnu") or "Inconnu"
            comptage[situation] = comptage.get(situation, 0) + 1

        labels = list(comptage.keys())
        valeurs = list(comptage.values())
        couleurs = ["#a6e3a1", "#f38ba8", "#f9e2af", "#94e2d5", "#b4befe", "#cba6f7"]

        # --- CONFIGURATION MATPLOTLIB ---
        fig = Figure(figsize=(6.5, 4.8), dpi=100, facecolor="#2b2b3b")
        
        # --- MODE 3D ---
        if self.type_graphique == "Barres 3D":
            # On ajoute la projection 3D ici
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor("#2b2b3b")
            
            # Paramètres de positionnement des barres 3D
            x_pos = np.arange(len(labels))
            y_pos = np.zeros(len(labels))
            z_pos = np.zeros(len(labels))
            
            # Dimensions des barres (largeur, profondeur, hauteur)
            dx = 0.5 * np.ones(len(labels))
            dy = 0.5 * np.ones(len(labels))
            dz = valeurs
            
            # Dessin des barres en 3D
            ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=couleurs[:len(labels)], shade=True)
            
            # Configuration des axes en 3D
            ax.set_xticks(x_pos + 0.25)
            ax.set_xticklabels(labels, color="#cdd6f4", fontsize=9)
            
            # On masque ou ajuste l'axe Y (inutile ici puisqu'on n'a qu'une seule rangée de barres)
            ax.set_yticks([0])
            ax.set_yticklabels([])
            
            # Axe Z (les valeurs)
            ax.tick_params(axis='z', colors="#cdd6f4", labelsize=9)
            ax.set_zlabel("Nombre d'élèves", color="#cdd6f4", fontsize=10)
            
            # Couleur des vitres du cube 3D (panneaux de fond)
            ax.xaxis.set_pane_color((0.17, 0.17, 0.23, 1.0)) # #2b2b3b
            ax.yaxis.set_pane_color((0.17, 0.17, 0.23, 1.0))
            ax.zaxis.set_pane_color((0.12, 0.12, 0.18, 1.0)) # Un poil plus sombre pour le sol

        # --- MODE CAMEMBERT ---
        elif self.type_graphique == "Camembert":
            ax = fig.add_subplot(111)
            ax.set_facecolor("#2b2b3b")
            
            wedges, texts, autotexts = ax.pie(
                valeurs,
                labels=labels,
                colors=couleurs[: len(labels)],
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "#1e1e2e", "linewidth": 2},
            )
            ax.axis('equal')

            for text in texts:
                text.set_color("#cdd6f4")
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_color("#1e1e2e")
                autotext.set_fontsize(9)
                autotext.set_fontweight("bold")
        
        # --- MODE BARRES 2D ---
        else:  
            ax = fig.add_subplot(111)
            ax.set_facecolor("#2b2b3b")
            
            bars = ax.bar(labels, valeurs, color=couleurs[: len(labels)], edgecolor="#1e1e2e", linewidth=1)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color("#cdd6f4")
            ax.spines['bottom'].set_color("#cdd6f4")
            ax.tick_params(colors="#cdd6f4", labelsize=10)
            ax.grid(axis='y', linestyle='--', alpha=0.2, color="#cdd6f4")
            
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', color="#cdd6f4", fontweight='bold')

        # Titre global de la Figure Matplotlib
        ax.set_title(
            f"Total : {len(eleves)} élève(s)",
            color="#cdd6f4",
            fontsize=11,
            pad=15,
        )

        fig.tight_layout()

        # --- INTEGRATION TKINTER ---
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        
        # Active l'interactivité (rotation à la souris pour la 3D)
        canvas.get_tk_widget().pack(expand=True, padx=10, pady=10)