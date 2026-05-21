import customtkinter as ctk
from tkinter import ttk, messagebox
import os

# Gestion de l'import du module de fonctions
try:
    import fonctions
except ImportError:
    try:
        import fonction as fonctions
    except ImportError:
        fonctions = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GestionEleves(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Système de Gestion Moderne - GESTIONDR1")
        self.geometry("1200x800")
        self.configure(fg_color="#1e1e2e")

        # Variables de contrôle
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

        # Titre
        ctk.CTkLabel(self, text="ENREGISTREMENT DES ÉLÈVES", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="#89b4fa").pack(pady=20)

        # --- ZONE FORMULAIRE ---
        self.form_frame = ctk.CTkFrame(self, fg_color="#2b2b3b", corner_radius=15)
        self.form_frame.pack(padx=20, pady=10, fill="x")

        
        ctk.CTkLabel(self.form_frame, text="MATRICULE :", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_mat, width=160).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.form_frame, text="NOM :", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_nom, width=160).grid(row=0, column=3, padx=10, pady=10)

        # Barre de recherche (Horizontale après le NOM)
        search_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        search_container.grid(row=0, column=4, padx=20, pady=10)
        ctk.CTkComboBox(search_container, values=["Matricule", "Nom"], variable=self.filtre_recherche, width=100).pack(side="left", padx=5)
        ctk.CTkEntry(search_container, placeholder_text="Rechercher...", textvariable=self.var_recherche, width=140).pack(side="left", padx=5)
        ctk.CTkButton(search_container, text="OK", width=40, command=self.executer_recherche, fg_color="#89b4fa", text_color="black").pack(side="left", padx=5)

        # Ligne 1 : PRÉNOM et CLASSE
        ctk.CTkLabel(self.form_frame, text="PRÉNOM :", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_pre, width=160).grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.form_frame, text="CLASSE :", font=("Arial", 11, "bold")).grid(row=1, column=2, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_cla, width=160).grid(row=1, column=3, padx=10, pady=10)

        # Ligne 2 : ADRESSE et EMAIL
        ctk.CTkLabel(self.form_frame, text="ADRESSE :", font=("Arial", 11, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_adr, width=160).grid(row=2, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.form_frame, text="EMAIL :", font=("Arial", 11, "bold")).grid(row=2, column=2, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_mail, width=160).grid(row=2, column=3, padx=10, pady=10)

        # Ligne 3 : TÉLÉPHONE et CYCLE
        ctk.CTkLabel(self.form_frame, text="TÉLÉPHONE :", font=("Arial", 11, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_tel, width=160).grid(row=3, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.form_frame, text="CYCLE :", font=("Arial", 11, "bold")).grid(row=3, column=2, padx=10, pady=10, sticky="w")
        ctk.CTkComboBox(self.form_frame, values=["Primaire", "Collège", "Lycée"], variable=self.var_cyc, width=160).grid(row=3, column=3, padx=10, pady=10)

        # Ligne 4 : SEXE et SITUATION
        ctk.CTkLabel(self.form_frame, text="SEXE :", font=("Arial", 11, "bold")).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkComboBox(self.form_frame, values=["Masculin", "Féminin"], variable=self.var_sex, width=160).grid(row=4, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.form_frame, text="SITUATION (/9 mois) :", font=("Arial", 11, "bold")).grid(row=4, column=2, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(self.form_frame, textvariable=self.var_sit, width=160).grid(row=4, column=3, padx=10, pady=10)

        # --- ZONE BOUTONS ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        boutons_list = [
            ("Ajouter", "#a6e3a1", self.ajouter_data), ("Modifier", "#f9e2af", self.modifier_data),
            ("Supprimer", "#f38ba8", self.supprimer_data), ("Afficher", "#b4befe", self.afficher_details),
            ("Annuler", "#6c7086", self.reset_champs), ("RETOUR", "#45475a", self.quitter_page)
        ]

        for i, (txt, color, cmd) in enumerate(boutons_list):
            ctk.CTkButton(self.btn_frame, text=txt, fg_color=color, text_color="black" if i < 4 else "white", 
                          width=110, font=("Arial", 12, "bold"), command=cmd).grid(row=0, column=i, padx=5)

        # --- ZONE TABLEAU ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        cols = ("id", "nom", "pre", "cla", "sex", "cyc", "sit", "Mat")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show="headings")
        entetes = ["ID", "NOM", "PRÉNOM", "CLASSE", "SEXE", "CYCLE", "SOLDE", "MATRICULE"]
        for col, head in zip(cols, entetes):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda e: self.auto_remplir())
        
        # Chargement initial des données
        self.actualiser_tableau()

    # --- LOGIQUE ---
    def actualiser_tableau(self):
        """Remplit le tableau en évitant l'erreur 'index out of range'."""
        if fonctions:
            try:
                for item in self.tree.get_children(): self.tree.delete(item)
                donnees = fonctions.recuperer_tous_les_eleves()
                if donnees:
                    for r in donnees:
                        # SECURITÉ : On crée une liste de données propre
                        # On vérifie la taille de 'r' avant d'accéder aux index
                        id_e = r[0] if len(r) > 0 else ""
                        nom = r[1] if len(r) > 1 else ""
                        pre = r[2] if len(r) > 2 else ""
                        cla = r[7] if len(r) > 7 else ""
                        sex = r[12] if len(r) > 12 else (r[5] if len(r) > 5 else "") # Fallback si colonnes décalées
                        cyc = r[10] if len(r) > 10 else ""
                        sit = r[11] if len(r) > 11 else ""
                        Mat = r[12] if len(r) > 12 else ""
                        self.tree.insert("", "end", values=(id_e, nom, pre, cla, sex, cyc, sit))
            except Exception as e:
                print(f"Erreur lors du chargement : {e}")

    def ajouter_data(self):
        if self.var_nom.get() == "" or self.var_mat.get() == "":
            messagebox.showerror("Erreur", "Nom et Matricule requis !")
            return
        if fonctions and fonctions.ajouter_eleve(self.var_nom.get(), self.var_pre.get(), "", "", self.var_tel.get(), self.var_adr.get(), self.var_cla.get(), self.var_mat.get(), self.var_cyc.get(), self.var_sit.get()):
            self.actualiser_tableau()
            self.reset_champs()

    def modifier_data(self):
        if fonctions and fonctions.modifier_eleve(self.var_nom.get(), self.var_pre.get(), "", "", self.var_tel.get(), self.var_adr.get(), self.var_cla.get(), self.var_mat.get(), self.var_cyc.get(), self.var_sit.get()):
            self.actualiser_tableau()

    def supprimer_data(self):
        if self.var_mat.get() and messagebox.askyesno("Confirmation", "Supprimer cet élève ?"):
            # fonctions.supprimer_eleve(self.var_mat.get()) # Dépend de fonctions.py
            self.actualiser_tableau()

    def executer_recherche(self):
        if fonctions:
            resultats = fonctions.rechercher_filtrer(self.filtre_recherche.get(), self.var_recherche.get())
            for item in self.tree.get_children(): self.tree.delete(item)
            for r in resultats: self.tree.insert("", "end", values=r)

    def auto_remplir(self):
        try:
            selection = self.tree.selection()[0]
            valeurs = self.tree.item(selection)['values']
            res = fonctions.rechercher_eleve(valeurs[0])
            if res:
                self.var_nom.set(res[1]); self.var_pre.set(res[2]); self.var_mat.set(res[9])
                self.var_cla.set(res[7]); self.var_cyc.set(res[10]); self.var_sit.set(res[11])
        except: pass

    def afficher_details(self):
        messagebox.showinfo("Détails", f"Élève sélectionné : {self.var_nom.get()}")

    def reset_champs(self):
        for v in [self.var_mat, self.var_nom, self.var_pre, self.var_cla, self.var_adr, self.var_mail, self.var_tel, self.var_sit]: v.set("")

    def quitter_page(self):
        self.destroy()
        os.system("python connexion.py")

if __name__ == "__main__":
    app = GestionEleves()
    app.mainloop()