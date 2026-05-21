class EleveController:
    
    @staticmethod
    def valider_tous_les_champs(donnees_formulaire):
        """
        Vérifie dynamiquement si l'un des champs transmis est vide.
        Retourne (True, None) si tout est rempli, ou (False, message) au premier champ vide trouvé.
        """
        for nom_champ, valeur in donnees_formulaire.items():
            # .strip() permet d'éviter que l'utilisateur valide le champ en tapant juste des espaces
            if not valeur or valeur.strip() == "":
                return False, f"Le champ '{nom_champ}' est obligatoire. Veuillez le renseigner."
        return True, "Tous les champs sont valides"