import customtkinter as ctk
from view.connexion_ecran import ConnexionEcran
from view.gestion_ecran import GestionEcran


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.geometry("750x550")
        self.title("GESTIONDR1")

        container = ctk.CTkFrame(self, fg_color="#1e1e2e")
        container.pack(fill="both", expand=True)

        self.frames = {}
        # stocke les écrans dans un dictionnaire pour pouvoir les afficher facilement
        for F in (ConnexionEcran, GestionEcran):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(GestionEcran)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
