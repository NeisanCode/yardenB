import tkinter as tk
from tkinter import CENTER, messagebox
from PIL import Image, ImageTk

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import App


class ConnexionEcran(tk.Frame):
    def __init__(self, parent: tk.Tk, controller: App):
        super().__init__(parent, bg="#2b2b3b")
        self.controller = controller
        self._build()

    def _build(self):
        self.card = tk.Frame(self, bg="#2b2b3b", highlightthickness=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=350)

        self.label_titre = tk.Label(
            self.card,
            text="CONNEXION",
            font=("Segoe UI", 18, "bold italic"),
            fg="#89b4fa",
            bg="#2b2b3b",
        )
        self.label_titre.place(relx=0.5, y=30, anchor=CENTER)
        self.canvas_photo = tk.Canvas(
            self.card, width=180, height=180, bg="white", highlightthickness=0
        )
        self.canvas_photo.place(x=30, y=85)

        # Charger image
        img = Image.open("assets/img/profil.png")

        # Redimensionner
        img = img.resize((180, 180))

        # Convertir pour Tkinter
        self.photo = ImageTk.PhotoImage(img)

        # Afficher dans canvas
        self.canvas_photo.create_image(0, 0, anchor="nw", image=self.photo)
        self.lbl_auth = tk.Label(
            self.card,
            text="Authentification",
            font=("Segoe UI", 11, "italic"),
            fg="#cdd6f4",
            bg="#2b2b3b",
        )
        self.lbl_auth.place(x=240, y=75)

        tk.Label(
            self.card,
            text="Utilisateur :",
            font=("Segoe UI", 10, "bold"),
            fg="#89b4fa",
            bg="#2b2b3b",
        ).place(x=240, y=110)

        self.entry_user = tk.Entry(
            self.card,
            font=("Segoe UI", 11),
            bg="#313244",
            fg="white",
            insertbackground="white",
            highlightthickness=0,
        )
        self.entry_user.place(x=360, y=110, width=250, height=25)

        tk.Label(
            self.card,
            text="Mot de passe :",
            font=("Segoe UI", 10, "bold"),
            fg="#89b4fa",
            bg="#2b2b3b",
        ).place(x=240, y=160)

        self.entry_pass = tk.Entry(
            self.card,
            font=("Segoe UI", 11),
            bg="#313244",
            fg="white",
            insertbackground="white",
            highlightthickness=0,
            show="●",
        )
        self.entry_pass.place(x=360, y=160, width=250, height=25)

        self.btn_connecter = tk.Button(
            self.card,
            text="Connecter",
            bg="#a6e3a1",
            fg="#11111b",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.tenter_connexion,
        )
        self.btn_connecter.place(x=360, y=210, width=120, height=35)

        self.btn_annuler = tk.Button(
            self.card,
            text="Annuler",
            bg="#f38ba8",  # ← fg_color → bg
            fg="#11111b",  # ← text_color → fg
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground="#f2869d",  # ← hover_color → activebackground
            activeforeground="#11111b",
            command=self.reset_fields,
        )
        self.btn_annuler.place(x=490, y=210, width=120, height=35)

        self.btn_quitter = tk.Button(
            self.card,
            text="✖ Quitter",
            font=("Segoe UI", 10, "bold"),
            bg="#45475a",  # ← fg_color → bg
            fg="#f38ba8",  # ← text_color → fg
            activebackground="#5c5f7a",  # ← hover_color → activebackground
            activeforeground="#f38ba8",
            relief="flat",
            cursor="hand2",
            command=self.winfo_toplevel().destroy,
        )
        self.btn_quitter.place(relx=0.5, y=300, anchor=CENTER, width=300, height=35)

    def tenter_connexion(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        if not (user == "admin" and password == "1234"):
            messagebox.showerror("Erreur", "Identifiant de connexion incorrect")
            return
        self.seconnecter()

    def seconnecter(self):
        from .gestion_ecran import GestionEcran

        self.controller.show_frame(GestionEcran)

    def reset_fields(self):
        self.entry_user.delete(0, "end")
        self.entry_pass.delete(0, "end")
