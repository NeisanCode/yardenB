import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers import EleveController


class GestionEcran(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1e1e2e")
        self.controller = controller

        # Variables d'état de l'interface (Champs de saisie)
        self.var_mat = ctk.StringVar()
        self.var_nom = ctk.StringVar()
        self.var_pre = ctk.StringVar()
        self.var_cla = ctk.StringVar()
        self.var_adr = ctk.StringVar()
        self.var_mail = ctk.StringVar()
        self.var_tel = ctk.StringVar()
        self.var_cyc = ctk.StringVar(value="Lycée")
        self.var_sex = ctk.StringVar(value="Masculin")
        self.var_sit = ctk.StringVar()

        # Variables pour le bloc recherche
        self.var_recherche = ctk.StringVar()
        self.filtre_recherche = ctk.StringVar(value="Matricule")

        # --- TITRE ---
        ctk.CTkLabel(
            self,
            text="ENREGISTREMENT DES ÉLÈVES",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#89b4fa",
        ).pack(pady=20)

        # --- ZONE FORMULAIRE ---
        self.form_frame = ctk.CTkFrame(self, fg_color="#2b2b3b", corner_radius=15)
        self.form_frame.pack(padx=20, pady=10, fill="x")

        # Ligne 0 : Matricule, Nom + Bloc Recherche
        ctk.CTkLabel(
            self.form_frame, text="MATRICULE :", font=("Arial", 11, "bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_mat, width=180).grid(
            row=0, column=1, padx=10, pady=10
        )

        ctk.CTkLabel(self.form_frame, text="NOM :", font=("Arial", 11, "bold")).grid(
            row=0, column=2, padx=10, pady=10, sticky="w"
        )
        ctk.CTkEntry(self.form_frame, textvariable=self.var_nom, width=180).grid(
            row=0, column=3, padx=10, pady=10
        )

        # Bloc Recherche (Disposé selon ton image)
        recherche_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        recherche_frame.grid(row=0, column=4, padx=30, pady=10, sticky="nsew")

        recherche_input_frame = ctk.CTkFrame(recherche_frame, fg_color="transparent")
        recherche_input_frame.pack(side="top", fill="x", pady=(0, 5))

        ctk.CTkEntry(
            recherche_input_frame,
            placeholder_text="Rechercher...",
            textvariable=self.var_recherche,
            width=150,
        ).pack(side="left", padx=(0, 5))
        ctk.CTkComboBox(
            recherche_input_frame,
            values=["Matricule", "Nom"],
            variable=self.filtre_recherche,
            width=110,
        ).pack(side="left")

        ctk.CTkButton(
            recherche_frame,
            text="OK",
            command=self.action_rechercher,
            fg_color="#89b4fa",
            text_color="black",
            font=("Arial", 12, "bold"),
        ).pack(side="top", fill="x")

        # Ligne 1 : Prénom, Classe
        ctk.CTkLabel(self.form_frame, text="PRÉNOM :", font=("Arial", 11, "bold")).grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        ctk.CTkEntry(self.form_frame, textvariable=self.var_pre, width=180).grid(
            row=1, column=1, padx=10, pady=10
        )
        ctk.CTkLabel(self.form_frame, text="CLASSE :", font=("Arial", 11, "bold")).grid(
            row=1, column=2, padx=10, pady=10, sticky="w"
        )
        ctk.CTkEntry(self.form_frame, textvariable=self.var_cla, width=180).grid(
            row=1, column=3, padx=10, pady=10
        )

        # Ligne 2 : Adresse, Email
        ctk.CTkLabel(
            self.form_frame, text="ADRESSE :", font=("Arial", 11, "bold")
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_adr, width=180).grid(
            row=2, column=1, padx=10, pady=10
        )
        ctk.CTkLabel(self.form_frame, text="EMAIL :", font=("Arial", 11, "bold")).grid(
            row=2, column=2, padx=10, pady=10, sticky="w"
        )
        ctk.CTkEntry(self.form_frame, textvariable=self.var_mail, width=180).grid(
            row=2, column=3, padx=10, pady=10
        )

        # Ligne 3 : Téléphone, Cycle
        ctk.CTkLabel(
            self.form_frame, text="TÉLÉPHONE :", font=("Arial", 11, "bold")
        ).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_tel, width=180).grid(
            row=3, column=1, padx=10, pady=10
        )
        ctk.CTkLabel(self.form_frame, text="CYCLE :", font=("Arial", 11, "bold")).grid(
            row=3, column=2, padx=10, pady=10, sticky="w"
        )
        ctk.CTkComboBox(
            self.form_frame,
            values=["Primaire", "Collège", "Lycée", "Université"],
            variable=self.var_cyc,
            width=180,
        ).grid(row=3, column=3, padx=10, pady=10)

        # Ligne 4 : Sexe, Situation
        ctk.CTkLabel(self.form_frame, text="SEXE :", font=("Arial", 11, "bold")).grid(
            row=4, column=0, padx=10, pady=10, sticky="w"
        )
        ctk.CTkComboBox(
            self.form_frame,
            values=["Masculin", "Féminin"],
            variable=self.var_sex,
            width=180,
        ).grid(row=4, column=1, padx=10, pady=10)
        ctk.CTkLabel(
            self.form_frame, text="SITUATION :", font=("Arial", 11, "bold")
        ).grid(row=4, column=2, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(
            self.form_frame,
            textvariable=self.var_sit,
            width=180,
            placeholder_text="/9 mois",
        ).grid(row=4, column=3, padx=10, pady=10)

        # --- ACTIONS (BOUTONS LOOPS) ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        boutons = [
            {
                "text": "Ajouter",
                "color": "#a6e3a1",
                "command": self.action_ajouter,
                "text_color": "black",
            },
            {
                "text": "Modifier",
                "color": "#f9e2af",
                "command": self.action_modifier,
                "text_color": "black",
            },
            {
                "text": "Supprimer",
                "color": "#f38ba8",
                "command": self.action_supprimer,
                "text_color": "black",
            },
            {
                "text": "Annuler",
                "color": "#6c7086",
                "command": self.reinitialiser,
                "text_color": "white",
            },
            {
                "text": "RETOUR",
                "color": "#45475a",
                "command": self.action_retour,
                "text_color": "white",
            },
            {
                "text": "Afficher",
                "color": "#b4befe",
                "command": self.action_afficher,
                "text_color": "black",
            },
        ]

        for i, btn_config in enumerate(boutons):
            ctk.CTkButton(
                self.btn_frame,
                text=btn_config["text"],
                fg_color=btn_config["color"],
                text_color=btn_config["text_color"],
                width=110,
                font=("Arial", 12, "bold"),
                command=btn_config["command"],
                cursor="hand2",
            ).grid(row=0, column=i, padx=5)

        # --- TABLEAU DES DONNÉES (TREEVIEW) ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        cols = ("id", "nom", "pre", "cla", "sex", "cyc", "sit")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show="headings")

        for c, h in zip(
            cols,
            [
                "ID",
                "NOM",
                "PRÉNOM",
                "DATE NAISSANCE",
                "EMAIL",
                "TÉLÉPHONE",
                "ADRESSE",
                "CLASSE",
                "CYCLE",
                "MATRICULE",
                "SITUATION FINANCIÈRE",
                "DATE INSCRIPTION",
            ],
        ):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

    # ================= INTERACTION AVEC LE CONTROLEUR =================

    def action_ajouter(self):
        # 1. On récupère les valeurs sous forme de dictionnaire clair
        donnees = {
            "Matricule": self.var_mat.get(),
            "Nom": self.var_nom.get(),
            "Prénom": self.var_pre.get(),
            "Classe": self.var_cla.get(),
            "Adresse": self.var_adr.get(),
            "Email": self.var_mail.get(),
            "Téléphone": self.var_tel.get(),
            "Situation": self.var_sit.get(),
        }

        # 2. On demande validation au contrôleur
        est_valide, message_erreur = EleveController.valider_tous_les_champs(donnees)

        if not est_valide:
            # S'il manque un champ, on affiche l'alerte et on s'arrête
            messagebox.showwarning("Champs obligatoires", message_erreur)
            return

        # 3. Si c'est valide (intégration DB à faire ici plus tard)
        # Pour le test visuel, on ajoute la ligne validée dans le tableau
        self.tree.insert(
            "",
            "end",
            values=(
                donnees["Matricule"],
                donnees["Nom"],
                donnees["Prénom"],
                donnees["Classe"],
                self.var_sex.get(),
                self.var_cyc.get(),
                donnees["Situation"],
            ),
        )
        self.reinitialiser()

    def action_modifier(self):
        pass

    def action_supprimer(self):
        pass

    def action_rechercher(self):
        if not self.var_recherche.get().strip():
            messagebox.showwarning(
                "Recherche", "Veuillez saisir un terme à rechercher."
            )
            return

    def action_afficher(self):
        pass

    def reinitialiser(self):
        for v in [
            self.var_mat,
            self.var_nom,
            self.var_pre,
            self.var_cla,
            self.var_adr,
            self.var_mail,
            self.var_tel,
            self.var_sit,
            self.var_recherche,
        ]:
            v.set("")

    def action_retour(self):
        from view.connexion_ecran import ConnexionEcran

        self.controller.show_frame(ConnexionEcran)
