from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
import unittest


class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role


class Tache:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
        dependances: List["Tache"] = None,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = dependances or []

    def ajouter_dependance(self, tache: "Tache"):
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        self.statut = statut


class Equipe:
    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        return self.membres


class Jalon:
    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date


class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    def __init__(self, description: str, version: int):
        self.description = description
        self.version = version
        self.date = datetime.now()


class NotificationStrategy(ABC):
    @abstractmethod
    def envoyer_message(self, message: str, destinataire: Membre):
        pass


class EmailNotificationStrategy(NotificationStrategy):
    def envoyer_message(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par email: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    def envoyer_message(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par SMS: {message}")


class PushNotificationStrategy(NotificationStrategy):
    def envoyer_message(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par Push: {message}")


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notifier(self, message: str, destinataires: List[Membre]):
        for destinataire in destinataires:
            self.strategy.envoyer_message(message, destinataire)


class Projet:
    def __init__(
        self, nom: str, description: str, date_debut: datetime, date_fin: datetime
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = 0.0
        self.taches = []
        self.equipe = Equipe()
        self.risques = []
        self.jalons = []
        self.version = 1
        self.changements = []
        self.chemin_critique = []
        self.notification_context = None

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context = NotificationContext(strategy)

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_membre_equipe(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe")

    def definir_budget(self, budget: float):
        self.budget = budget
        self.notifier(
            f"Le budget du projet a été défini à {self.budget} Unité Monétaire"
        )

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(f"Nouveau risque ajouté: {risque.description}")

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(f"Nouveau jalon ajouté: {jalon.nom}")

    def enregistrer_changement(self, description: str):
        changement = Changement(description, self.version)
        self.changements.append(changement)
        self.version += 1
        self.notifier(f"Changement enregistré: {description} (version {self.version})")

    def calculer_chemin_critique(self):
        def find_longest_path(tache, memo):
            if tache in memo:
                return memo[tache]
            if not tache.dependances:
                memo[tache] = (0, [tache])
                return memo[tache]
            max_length, max_path = 0, []
            for dep in tache.dependances:
                dep_length, dep_path = find_longest_path(dep, memo)
                if dep_length > max_length:
                    max_length = dep_length
                    max_path = dep_path
            total_length = max_length + (tache.date_fin - tache.date_debut).days
            memo[tache] = (total_length, max_path + [tache])
            return memo[tache]

        memo = {}
        all_paths = [find_longest_path(tache, memo) for tache in self.taches]
        self.chemin_critique = max(all_paths, key=lambda x: x[0])[1]

    def notifier(self, message: str):
        if self.notification_context:
            self.notification_context.notifier(message, self.equipe.membres)

    def generer_rapport(self):
        rapport = f"Rapport d'activités du Projet '{self.nom}':\n"
        rapport += f"Version: {self.version}\n"
        rapport += f"Dates: {self.date_debut} à {self.date_fin}\n"
        rapport += f"Budget: {self.budget} Unité Monétaire\n"
        rapport += "Équipe:\n"
        for membre in self.equipe.membres:
            rapport += f"- {membre.nom} ({membre.role})\n"
        rapport += "Tâches:\n"
        for tache in self.taches:
            rapport += f"- {tache.nom} ({tache.date_debut} à {tache.date_fin}), Responsable: {tache.responsable.nom}, Statut: {tache.statut}\n"
        rapport += "Jalons:\n"
        for jalon in self.jalons:
            rapport += f"- {jalon.nom} ({jalon.date})\n"
        rapport += "Risques:\n"
        for risque in self.risques:
            rapport += f"- {risque.description} (Probabilité: {risque.probabilite}, Impact: {risque.impact})\n"
        rapport += "Chemin Critique:\n"
        for tache in self.chemin_critique:
            rapport += f"- {tache.nom} ({tache.date_debut} à {tache.date_fin})\n"
        return rapport


# Tests unitaires
class TestProjet(unittest.TestCase):
    def setUp(self):
        self.modou = Membre("Brahim", "Chef de projet")
        self.christian = Membre("Pape", "Développeur")
        self.projet = Projet(
            "Nouveau Produit",
            "Développement d'un nouveau produit",
            datetime(2024, 1, 1),
            datetime(2024, 12, 31),
        )
        self.email_strategy = EmailNotificationStrategy()
        self.projet.set_notification_strategy(self.email_strategy)

    def test_ajouter_membre_equipe(self):
        self.projet.ajouter_membre_equipe(self.modou)
        self.assertIn(self.modou, self.projet.equipe.obtenir_membres())

    def test_ajouter_tache(self):
        tache1 = Tache(
            "Analyse des besoins",
            "Description de l'analyse des besoins",
            datetime(2024, 1, 1),
            datetime(2024, 1, 31),
            self.modou,
            "Terminée",
        )
        self.projet.ajouter_tache(tache1)
        self.assertIn(tache1, self.projet.taches)

    def test_definir_budget(self):
        self.projet.definir_budget(50000.0)
        self.assertEqual(self.projet.budget, 50000.0)

    def test_ajouter_risque(self):
        risque = Risque("Retard de livraison", 0.3, "Élevé")
        self.projet.ajouter_risque(risque)
        self.assertIn(risque, self.projet.risques)

    def test_ajouter_jalon(self):
        jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
        self.projet.ajouter_jalon(jalon)
        self.assertIn(jalon, self.projet.jalons)

    def test_enregistrer_changement(self):
        self.projet.enregistrer_changement("Changement de la portée du projet")
        self.assertEqual(len(self.projet.changements), 1)
        self.assertEqual(
            self.projet.changements[0].description, "Changement de la portée du projet"
        )

    def test_calculer_chemin_critique(self):
        tache1 = Tache(
            "Analyse des besoins",
            "Description de l'analyse des besoins",
            datetime(2024, 1, 1),
            datetime(2024, 1, 31),
            self.modou,
            "Terminée",
        )
        tache2 = Tache(
            "Développement",
            "Description du développement",
            datetime(2024, 2, 1),
            datetime(2024, 6, 30),
            self.christian,
            "Non démarrée",
            dependances=[tache1],
        )
        self.projet.ajouter_tache(tache1)
        self.projet.ajouter_tache(tache2)
        self.projet.calculer_chemin_critique()
        self.assertEqual(self.projet.chemin_critique, [tache1, tache2])

    def test_generer_rapport(self):
        self.projet.ajouter_membre_equipe(self.modou)
        self.projet.ajouter_membre_equipe(self.christian)
        tache1 = Tache(
            "Analyse des besoins",
            "Description de l'analyse des besoins",
            datetime(2024, 1, 1),
            datetime(2024, 1, 31),
            self.modou,
            "Terminée",
        )
        self.projet.ajouter_tache(tache1)
        self.projet.definir_budget(50000.0)
        risque = Risque("Retard de livraison", 0.3, "Élevé")
        self.projet.ajouter_risque(risque)
        jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
        self.projet.ajouter_jalon(jalon)
        self.projet.enregistrer_changement("Changement de la portée du projet")
        self.projet.calculer_chemin_critique()
        rapport = self.projet.generer_rapport()
        self.assertIn("Rapport d'activités du Projet 'Nouveau Produit'", rapport)
        self.assertIn("Version: 2", rapport)
        self.assertIn("Brahim (Chef de projet)", rapport)
        self.assertIn("Pape (Développeur)", rapport)
        self.assertIn(
            "Analyse des besoins (2024-01-01 00:00:00 à 2024-01-31 00:00:00), Responsable: Brahim, Statut: Terminée",
            rapport,
        )
        self.assertIn("Phase 1 terminée (2024-01-31 00:00:00)", rapport)
        self.assertIn("Retard de livraison (Probabilité: 0.3, Impact: Élevé)", rapport)
        self.assertIn(
            "Analyse des besoins (2024-01-01 00:00:00 à 2024-01-31 00:00:00)", rapport
        )


if __name__ == "__main__":
    unittest.main()
