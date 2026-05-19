import mysql.connector
from tkinter import messagebox

def connecter():
    """Établit la connexion avec MySQL sur XAMPP."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="",          
            database="gestiondr1" 
            )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur de Connexion", 
                             f"Impossible de se connecter à MySQL.\n"
                             f"Assurez-vous que le module MySQL est démarré sur XAMPP.\n"
                             f"Erreur : {err}")
        return None