from tkinter import *
from tkinter import ttk, messagebox

#NB: j'ai commenté  pour te faciliter la tache en cas de modification
# Les fonctions qui dynamisent les boutons .

def survol_entree(event):
    event.widget.config(bg="#f9e2af") 
    event.widget.place_configure(y=event.widget.winfo_y() - 3)

def survol_sortie(event):
    if "Connecter" in event.widget["text"]:
        event.widget.config(bg="#a6e3a1")
    elif "Annuler" in event.widget["text"]:
        event.widget.config(bg="#f38ba8")
    else:
        event.widget.config(bg="#45475a")
    event.widget.place_configure(y=event.widget.winfo_y() + 3)

# Ici, pour l'ouverture de l'interface 2
def ouvrir_gestion():
    # Création d'une nouvelle fenêtre
    gestion = Toplevel()
    gestion.title("GESTIONDR1 - Enregistrement des Élèves")
    gestion.geometry("1100x750")
    gestion.configure(bg='#1e1e2e')

    
    Label(gestion, text="ENREGISTREMENT DES ÉLÈVES", font=("Segoe UI", 20, "bold"), 
          bg='#1e1e2e', fg='#89b4fa').pack(pady=20)

   
    main_frame = Frame(gestion, bg='#2b2b3b', bd=1, relief=FLAT)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Colonne Gauche 
    form_frame = Frame(main_frame, bg='#2b2b3b')
    form_frame.place(x=20, y=20)

    champs = ["MATRICULE :", "NOM :", "PRÉNOM :", "CLASSE :", "ADRESSE :", "EMAIL :", "TÉLÉPHONE :", "CYCLE :"]
    for i, texte in enumerate(champs):
        Label(form_frame, text=texte, font=("Segoe UI", 10, "bold"), bg='#2b2b3b', fg='#89b4fa').grid(row=i, column=0, pady=8, sticky="w")
        Entry(form_frame, font=("Segoe UI", 11), bg='#313244', fg="white", bd=0).grid(row=i, column=1, padx=10, pady=8)

    # Le sexe 
    Label(form_frame, text="SEXE :", font=("Segoe UI", 10, "bold"), bg='#2b2b3b', fg='#89b4fa').grid(row=8, column=0, pady=8, sticky="w")
    var_sexe = StringVar(value="Masculin")
    OptionMenu(form_frame, var_sexe, "Masculin", "Féminin").grid(row=8, column=1, padx=10, pady=8, sticky="ew")

    # La situation 
    Label(form_frame, text="SITUATION (/9 mois) :", font=("Segoe UI", 10, "bold"), bg='#2b2b3b', fg='#89b4fa').grid(row=9, column=0, pady=8, sticky="w")
    Entry(form_frame, font=("Segoe UI", 11), bg='#313244', fg="white", width=5).grid(row=9, column=1, padx=10, pady=8, sticky="w")

    # Colonne Droite , les boutons 
    btn_frame = Frame(main_frame, bg='#2b2b3b')
    btn_frame.place(x=450, y=20)

    #  le boutton de Recherche
    Entry(btn_frame, font=("Segoe UI", 11), bg='#313244', fg="white").pack(pady=5)
    Button(btn_frame, text="Recherche Matricule", bg="#89b4fa", font=("Segoe UI", 9, "bold")).pack(fill="x", pady=5)

    for txt, col in [("Ajouter", "#a6e3a1"), ("Modifier", "#f9e2af"), ("Supprimer", "#f38ba8"), ("Afficher", "#b4befe"), ("Annuler", "#6c7086"), ("RETOUR", "#45475a")]:
        Button(btn_frame, text=txt, bg=col, font=("Segoe UI", 9, "bold"), bd=0).pack(fill="x", pady=5, ipady=5)

    # Le Tableau (Bas)
    table_frame = Frame(main_frame, bg='white')
    table_frame.place(x=20, y=450, width=1020, height=200)
    
    cols = ("ID", "Nom", "Prénom", "Classe", "Sexe", "Cycle", "Solde")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(fill="both", expand=True)
# fonction de connexion 
def tenter_connexion():
    user = entry_user.get()
    pw = entry_pass.get()
    
    # On vérifie les accès (ex: Admin / 1234)
    if user == "Admin" and pw == "1234":
        fenetre.withdraw() # Cache la fenêtre de connexion
        ouvrir_gestion()   # Lance la page de gestion
    else:
        messagebox.showerror("Erreur", "Identifiants incorrects\n(Utilisez Admin / 1234)")


fenetre = Tk()
fenetre.geometry('750x550')
fenetre.title('Connexion Sécurisée - GESTIONDR1')
fenetre.configure(bg='#1e1e2e')

main_card = Frame(fenetre, bg='#2b2b3b', bd=0, highlightthickness=1, highlightbackground="#45475a")
main_card.place(relx=0.5, rely=0.5, anchor=CENTER, width=650, height=350)

label_titre = Label(main_card, text="CONNEXION", font=("Segoe UI", 18, "bold italic"), 
                  bg='#2b2b3b', fg='#89b4fa')
label_titre.place(relx=0.5, y=30, anchor=CENTER)

canvas_photo = Canvas(main_card, width=180, height=180, bg="white", highlightthickness=0)
canvas_photo.place(x=30, y=85)
canvas_photo.create_oval(20, 20, 160, 160, fill="#0078d7", outline="")

lbl_auth = Label(main_card, text="Authentification", font=("Segoe UI", 11, "italic"), bg='#2b2b3b', fg='#cdd6f4')
lbl_auth.place(x=240, y=75)

Label(main_card, text="Utilisateur :", font=("Segoe UI", 10, "bold"), bg='#2b2b3b', fg='#89b4fa').place(x=240, y=110)
entry_user = Entry(main_card, font=("Segoe UI", 11), bg='#313244', fg="white", bd=0, insertbackground="white")
entry_user.place(x=360, y=110, width=250, height=25)

Label(main_card, text="Mot de passe :", font=("Segoe UI", 10, "bold"), bg='#2b2b3b', fg='#89b4fa').place(x=240, y=160)
entry_pass = Entry(main_card, font=("Segoe UI", 11), bg='#313244', fg="white", bd=0, insertbackground="white", show="●")
entry_pass.place(x=360, y=160, width=250, height=25)

btn_style = {"font": ("Segoe UI", 9, "bold"), "bd": 0, "cursor": "hand2", "fg": "#11111b"}


btn_connecter = Button(main_card, text="Connecter", bg="#a6e3a1", **btn_style, command=tenter_connexion)
btn_connecter.place(x=360, y=210, width=120, height=35)

btn_annuler = Button(main_card, text="Annuler", bg="#f38ba8", **btn_style)
btn_annuler.place(x=490, y=210, width=120, height=35)

btn_quitter = Button(main_card, text="✖ Quitter", font=("Segoe UI", 10, "bold"), 
                  bg="#45475a", fg="#f38ba8", bd=0, cursor="hand2", command=fenetre.quit)
btn_quitter.place(relx=0.5, y=300, anchor=CENTER, width=300, height=35)

# le Dynamisme toujours 
for b in [btn_connecter, btn_annuler]:
    b.bind("<Enter>", survol_entree)
    b.bind("<Leave>", survol_sortie)

fenetre.mainloop()