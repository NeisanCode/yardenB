import datetime
from models import Eleve, Cycle  # Import de ton modèle et de l'énumération
from services import EleveService


class EleveController:
    def __init__(self):
        # Initialisation du service métier qui communique avec le DAO
        self.service = EleveService()

    def _convertir_en_enum_cycle(self, chaine_cycle: str) -> Cycle:
        """
        Convertit la chaîne de caractères issue de la ComboBox UI
        en un membre de l'Enum Cycle attendu par le modèle Eleve.
        """
        for membre in Cycle:
            if membre.value == chaine_cycle:
                return membre

        # Par sécurité, si aucune correspondance, renvoie la valeur par défaut (ex: LYCEE)
        return Cycle.LYCEE

    def verifier_et_ajouter_eleve(
        self, donnees_formulaire, cycle_chaine, sexe_selectionne
    ):
        """
        1. Valide que toutes les chaînes textuelles du formulaire sont remplies.
        2. Convertit le cycle (String) en Enum Cycle.
        3. Convertit le dictionnaire en entité métier 'Eleve'.
        4. Applique les règles de validation via EleveService et l'insère en Base de Données.
        """
        # --- ÉTAPE 1 : Validation de surface (tous les champs Entry requis) ---
        for nom_champ, valeur in donnees_formulaire.items():
            if not valeur or valeur.strip() == "":
                return False, f"Le champ '{nom_champ}' est obligatoire."

        try:
            # --- ÉTAPE 2 : Traitement des données et Conversion en Enum Cycle ---
            nom = donnees_formulaire["Nom"].strip()
            prenom = donnees_formulaire["Prénom"].strip()
            email = donnees_formulaire["Email"].strip()
            telephone = donnees_formulaire["Téléphone"].strip()
            adresse = donnees_formulaire["Adresse"].strip()
            classe = donnees_formulaire["Classe"].strip()
            matricule = donnees_formulaire["Matricule"].strip()
            situation_financiere = donnees_formulaire["Situation"].strip()

            # Transformation de la String UI ("Lycée", "Collège"...) en Enum Cycle (Cycle.LYCEE...)
            enum_cycle = self._convertir_en_enum_cycle(cycle_chaine)

            # Dates exigées par la base de données (valeurs par défaut)
            date_naissance = datetime.date.today()
            date_inscription = datetime.datetime.now()

            # --- ÉTAPE 3 : Instanciation du modèle Eleve avec l'Enum Cycle ---
            nouvel_eleve = Eleve(
                id=None,  # Géré automatiquement par l'AUTO_INCREMENT MariaDB
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                email=email,
                telephone=telephone,
                adresse=adresse,
                classe=classe,
                matricule=matricule,
                cycle=enum_cycle,  # Ici, l'objet reçoit bien l'instance de l'Enum (ex: Cycle.LYCEE)
                situation_financiere=situation_financiere,
                date_inscription=date_inscription,
            )

            # --- ÉTAPE 4 : Envoi à la couche Service ---
            # Le service effectuera la validation métier (unicité du matricule)
            self.service.ajouter_eleve(nouvel_eleve)

            return True, "L'élève a été enregistré avec succès en base de données !"

        except ValueError as e:
            # Capture les exceptions métiers levées par le service (ex: "Ce matricule existe déjà")
            return False, str(e)
        except Exception as e:
            # Capture les pannes de base de données ou de connexion
            return False, f"Une erreur technique est survenue : {str(e)}"

    def verifier_et_modifier_eleve(self, id: int, donnees_formulaire, cycle_chaine: str):
        """
        1. Valide que tous les champs sont remplis.
        2. Convertit le cycle en Enum.
        3. Construit l'entité Eleve mise à jour.
        4. Délègue la modification au service.
        """
        for nom_champ, valeur in donnees_formulaire.items():
            if not valeur or str(valeur).strip() == "":
                return False, f"Le champ '{nom_champ}' est obligatoire."

        try:
            nom = donnees_formulaire["Nom"].strip()
            prenom = donnees_formulaire["Prénom"].strip()
            email = donnees_formulaire["Email"].strip()
            telephone = donnees_formulaire["Téléphone"].strip()
            adresse = donnees_formulaire["Adresse"].strip()
            classe = donnees_formulaire["Classe"].strip()
            matricule = donnees_formulaire["Matricule"].strip()
            situation_financiere = donnees_formulaire["Situation"].strip()

            # Parsing de la date de naissance
            brut_date = donnees_formulaire.get("Date_naissance", "").strip()
            date_naissance = None
            for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    date_naissance = datetime.datetime.strptime(brut_date, fmt).date()
                    break
                except ValueError:
                    continue
            if date_naissance is None:
                return False, f"Date de naissance invalide : « {brut_date} »"

            enum_cycle = self._convertir_en_enum_cycle(cycle_chaine)

            eleve_maj = Eleve(
                id=id,
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                email=email,
                telephone=telephone,
                adresse=adresse,
                classe=classe,
                matricule=matricule,
                cycle=enum_cycle,
                situation_financiere=situation_financiere,
                date_inscription=datetime.datetime.now(),
            )
            self.service.modifier_eleve(id, eleve_maj)
            return True, "L'élève a été mis à jour avec succès."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Une erreur technique est survenue : {str(e)}"

    def supprimer_eleve(self, id: int):
        """Délègue la suppression au service."""
        try:
            self.service.supprimer_eleve(id)
            return True, "L'élève a été supprimé avec succès."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Une erreur technique est survenue : {str(e)}"

    def rechercher_eleves(self, terme: str, filtre: str):
        """
        Recherche des élèves par matricule ou par nom.
        Retourne toujours une liste (vide si aucun résultat).
        """
        try:
            if filtre == "Matricule":
                res = self.service.rechercher_par_matricule(terme)
                return True, [res] if res else []
            else:
                return True, self.service.rechercher_par_nom(terme)
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Une erreur technique est survenue : {str(e)}"

    def recuperer_tous_les_eleves(self):
        """Récupère l'ensemble des élèves de la DB pour alimenter l'interface."""
        try:
            return self.service.afficher_eleves()
        except Exception as e:
            print(f"Erreur lors de la récupération des élèves : {e}")
            return []