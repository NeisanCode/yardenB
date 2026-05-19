import database
from tkinter import messagebox

# Logique au niveau de l'interface de l'admin 
def verifier_admin(nom, mdp):
    db = database.connecter()
    if db:
        cursor = db.cursor()
        # On utilise tes noms de colonnes : nom_admin et mdp_admin
        query = "SELECT * FROM admin WHERE nom_admin = %s AND mdp_admin = %s"
        cursor.execute(query, (nom, mdp))
        resultat = cursor.fetchone()
        db.close()
        return resultat

# Logoique pour la gestion des élèves
def ajouter_eleve(nom, prenom, classe, adresse, email, tel, cycle, sexe, situation):
    db = database.connecter()
    if db:
        try:
            cursor = db.cursor()
            
            sql = """INSERT INTO ELEVE 
                     (Nom_El, Prenom_El, Classe_El, Adresse_El, Email_El, Tel_El, Cycle_El, Sexe_E, SituationF_El) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            valeurs = (nom, prenom, classe, adresse, email, tel, cycle, sexe, situation)
            cursor.execute(sql, valeurs)
            db.commit()
            messagebox.showinfo("Succès", f"L'élève {nom} a été enregistré avec le matricule {cursor.lastrowid}")
            return True
        except Exception as e:
            messagebox.showerror("Erreur SQL", f"Erreur lors de l'insertion : {e}")
            return False
        finally:
            db.close()

def supprimer_eleve(matricule):
    db = database.connecter()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM ELEVE WHERE Mat_El = %s", (matricule,))
            db.commit()
            messagebox.showinfo("Supprimé", "L'élève a été retiré du système.")
        finally:
            db.close()