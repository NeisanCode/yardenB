import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.eleve_controller import EleveController
from .utils import styleTreview
from .datepicker import DatePickerWidget


class GestionEcran(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1e1e2e")
        self.controller = controller
        self.eleve_controller: EleveController = EleveController()
        self.id_eleve_selectionne = None

        # --- Variables textuelles ---
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
        self.var_recherche = ctk.StringVar()
        self.filtre_recherche = ctk.StringVar(value="Matricule")

        # --- TITRE ---
        ctk.CTkLabel(
            self, text="ENREGISTREMENT DES ÉLÈVES",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#89b4fa"
        ).pack(pady=15)

        # --- FORMULAIRE ---
        self.form_frame = ctk.CTkFrame(self, fg_color="#2b2b3b", corner_radius=15)
        self.form_frame.pack(padx=20, pady=5, fill="x")

        # Helper functions for grid placement
        def lbl(txt, row, col):
            ctk.CTkLabel(self.form_frame, text=txt, font=("Segoe UI", 11, "bold")
                         ).grid(row=row, column=col, padx=10, pady=8, sticky="w")

        def ent(var, row, col, ph=""):
            ctk.CTkEntry(self.form_frame, textvariable=var, width=180,
                         font=("Segoe UI", 11), placeholder_text=ph
                         ).grid(row=row, column=col, padx=10, pady=8, sticky="w")

        # Ligne 0 : Matricule | Nom | [Zone Recherche]
        lbl("MATRICULE : ", 0, 0)
        ent(self.var_mat, 0, 1)
        lbl("NOM : ", 0, 2)
        ent(self.var_nom, 0, 3)

        recherche_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        recherche_frame.grid(row=0, column=4, rowspan=2, padx=20, pady=8, sticky="nsew")
        
        ctk.CTkEntry(recherche_frame, placeholder_text="Mot clé...",
                     textvariable=self.var_recherche, width=140,
                     font=("Segoe UI", 11)).grid(row=0, column=0, padx=(0, 5), pady=(0, 5))
        ctk.CTkComboBox(recherche_frame, values=["Matricule", "Nom"],
                        variable=self.filtre_recherche, width=100,
                        font=("Segoe UI", 11)).grid(row=0, column=1, pady=(0, 5))
        ctk.CTkButton(recherche_frame, text="OK", command=self.action_rechercher,
                      fg_color="#89b4fa", text_color="black",
                      font=("Segoe UI", 12, "bold")).grid(row=1, column=0, columnspan=2, sticky="ew")

        # Ligne 1 : Prénom | Classe
        lbl("PRÉNOM : ", 1, 0)
        ent(self.var_pre, 1, 1)
        lbl("CLASSE : ", 1, 2)
        ent(self.var_cla, 1, 3)

        # Ligne 2 : Adresse | Email
        lbl("ADRESSE : ", 2, 0)
        ent(self.var_adr, 2, 1)
        lbl("EMAIL : ", 2, 2)
        ent(self.var_mail, 2, 3)

        # Ligne 3 : Téléphone | Cycle
        lbl("TÉLÉPHONE : ", 3, 0)
        ent(self.var_tel, 3, 1)
        lbl("CYCLE : ", 3, 2)
        ctk.CTkComboBox(self.form_frame, values=["Primaire", "Collège", "Lycée", "Université"],
                        variable=self.var_cyc, width=180,
                        font=("Segoe UI", 11)).grid(row=3, column=3, padx=10, pady=8, sticky="w")

        # Ligne 4 : Sexe | Situation
        lbl("SEXE : ", 4, 0)
        ctk.CTkComboBox(self.form_frame, values=["Masculin", "Féminin"],
                        variable=self.var_sex, width=180,
                        font=("Segoe UI", 11)).grid(row=4, column=1, padx=10, pady=8, sticky="w")
        lbl("SITUATION : ", 4, 2)
        ent(self.var_sit, 4, 3, "/9 mois")

        # Ligne 5 : Dates
        lbl("DATE NAISSANCE : ", 5, 0)
        self.dp_naissance = DatePickerWidget(self.form_frame)
        self.dp_naissance.grid(row=5, column=1, padx=10, pady=8, sticky="w")

        lbl("DATE INSCRIPTION : ", 5, 2)
        self.dp_inscription = DatePickerWidget(self.form_frame)
        self.dp_inscription.grid(row=5, column=3, padx=10, pady=8, sticky="w")

        # Configure column weights so the form stretches nicely
        for i in range(5):
            self.form_frame.grid_columnconfigure(i, weight=1)

        # --- BOUTONS (2 rangées de 3) ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        boutons = [
            {"text": "Ajouter",   "color": "#a6e3a1", "command": self.action_ajouter,   "text_color": "black"},
            {"text": "Modifier",  "color": "#f9e2af", "command": self.action_modifier,  "text_color": "black"},
            {"text": "Supprimer", "color": "#f38ba8", "command": self.action_supprimer, "text_color": "black"},
            {"text": "RETOUR",    "color": "#45475a", "command": self.action_retour,    "text_color": "white"},
            {"text": "Afficher",  "color": "#b4befe", "command": self.action_afficher,  "text_color": "black"},
            {"text": "Annuler",   "color": "#6c7086", "command": self.reinitialiser,    "text_color": "white"},
        ]

        for i, b in enumerate(boutons):
            row_idx = i // 3
            col_idx = i % 3
            ctk.CTkButton(self.btn_frame, text=b["text"], fg_color=b["color"],
                          text_color=b["text_color"], width=120,
                          font=("Segoe UI", 12, "bold"),
                          command=b["command"]).grid(row=row_idx, column=col_idx, padx=10, pady=5)

        # --- TABLEAU ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        styleTreview()
        style = ttk.Style()
        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_ligne_selectionnee)

        self.charger_donnees_depuis_db()

    # ================= LOGIQUE =================

    def charger_donnees_depuis_db(self, donnees_filtrees=None):
        liste_eleves = (donnees_filtrees if donnees_filtrees is not None
                        else self.eleve_controller.recuperer_tous_les_eleves())

        colonnes_db = (
            list(liste_eleves[0].keys()) if liste_eleves
            else ["id", "nom", "prenom", "date_naissance", "email", "telephone",
                  "adresse", "classe", "date_inscription", "matricule",
                  "cycle", "situation_financiere"]
        )

        self.tree["columns"] = colonnes_db
        for col in colonnes_db:
            self.tree.heading(col, text=col.replace("_", " ").upper())
            self.tree.column(col, width=110, anchor="center")

        for r in self.tree.get_children():
            self.tree.delete(r)

        for eleve_dict in liste_eleves:
            self.tree.insert("", "end", values=[eleve_dict[c] for c in colonnes_db])

    def on_ligne_selectionnee(self, event):
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        eleve = dict(zip(self.tree["columns"], item["values"]))
        self.id_eleve_selectionne = eleve.get("id")

        self.var_mat.set(eleve.get("matricule", ""))
        self.var_nom.set(eleve.get("nom", ""))
        self.var_pre.set(eleve.get("prenom", ""))
        self.var_cla.set(eleve.get("classe", ""))
        self.var_adr.set(eleve.get("adresse", ""))
        self.var_mail.set(eleve.get("email", ""))
        self.var_tel.set(eleve.get("telephone", ""))
        self.var_cyc.set(eleve.get("cycle", "Lycée"))
        self.var_sit.set(eleve.get("situation_financiere", ""))
        self.dp_naissance.set(str(eleve.get("date_naissance", "")))
        self.dp_inscription.set(str(eleve.get("date_inscription", "")))

    def _build_donnees(self):
        return {
            "Matricule": self.var_mat.get(),
            "Nom": self.var_nom.get(),
            "Prénom": self.var_pre.get(),
            "Classe": self.var_cla.get(),
            "Adresse": self.var_adr.get(),
            "Email": self.var_mail.get(),
            "Téléphone": self.var_tel.get(),
            "Situation": self.var_sit.get(),
            "Date_naissance": self.dp_naissance.get(),  # transmise au controller
        }

    def action_ajouter(self):
        donnees = self._build_donnees()
        succes, message = self.eleve_controller.verifier_et_ajouter_eleve(
            donnees,
            cycle_chaine=self.var_cyc.get(),
            sexe_selectionne=self.var_sex.get(),
        )
        if succes:
            messagebox.showinfo("Succès", message)
            self.reinitialiser()
            self.charger_donnees_depuis_db()
        else:
            messagebox.showwarning("Erreur de validation", message)

    def action_modifier(self):
        if self.id_eleve_selectionne is None:
            messagebox.showwarning(
                "Sélection requise",
                "Veuillez sélectionner un élève dans le tableau."
            )
            return

        donnees = self._build_donnees()
        succes, message = self.eleve_controller.verifier_et_modifier_eleve(
            self.id_eleve_selectionne,
            donnees,
            cycle_chaine=self.var_cyc.get(),
        )
        if succes:
            messagebox.showinfo("Succès", message)
            self.reinitialiser()
            self.charger_donnees_depuis_db()
        else:
            messagebox.showerror("Erreur de modification", message)

    def action_supprimer(self):
        if self.id_eleve_selectionne is None:
            messagebox.showwarning(
                "Sélection requise",
                "Veuillez sélectionner un élève dans le tableau."
            )
            return
        confirme = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer définitivement cet élève ?"
        )
        if confirme:
            succes, message = self.eleve_controller.supprimer_eleve(
                self.id_eleve_selectionne
            )
            if succes:
                messagebox.showinfo("Succès", message)
                self.reinitialiser()
                self.charger_donnees_depuis_db()
            else:
                messagebox.showerror("Erreur technique", message)

    def action_rechercher(self):
        terme = self.var_recherche.get().strip()
        filtre = self.filtre_recherche.get()

        # Champ vide → on réaffiche tout sans message d'erreur
        if not terme:
            self.charger_donnees_depuis_db()
            return

        succes, resultat = self.eleve_controller.rechercher_eleves(terme, filtre)
        if not succes:
            messagebox.showerror("Erreur de recherche", resultat)
            return

        if not resultat:
            messagebox.showinfo("Recherche", "Aucun résultat trouvé.")

        self.charger_donnees_depuis_db(donnees_filtrees=resultat)

    def action_afficher(self):
        self.var_recherche.set("")
        self.filtre_recherche.set("Matricule")
        self.charger_donnees_depuis_db()

    def reinitialiser(self):
        self.id_eleve_selectionne = None
        for v in [self.var_mat, self.var_nom, self.var_pre, self.var_cla,
                  self.var_adr, self.var_mail, self.var_tel, self.var_sit,
                  self.var_recherche]:
            v.set("")
        self.var_cyc.set("Lycée")
        self.var_sex.set("Masculin")
        self.filtre_recherche.set("Matricule")
        self.dp_naissance.reset()
        self.dp_inscription.reset()

    def action_retour(self):
        from view.connexion_ecran import ConnexionEcran
        self.controller.show_frame(ConnexionEcran)