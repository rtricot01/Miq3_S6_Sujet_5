Système de Réservation d'Hôtel - Sujet 5
Ce projet est une application de gestion hôtelière complète développée en Python. Elle permet de gérer les chambres, les clients et les réservations via une interface graphique PySide6 ainsi qu'une base de données SQLAlchemy

- Auteurs
Quentin LEVEQUE
Louane SIALELLI
Raphael TRICOT
Ahmet TUNC

- Installation
1. Cloner le dépôt
Bash
git clone <https://github.com/rtricot01/Miq3_S6_Sujet_5>
cd Miq3_S6_Sujet_5
2. Installer le package
L'installation est possible en mode éditable ou non.

Bash
pip install -e . Pour le mode éditable
pip install . Sinon
Ceci permet d'installer les dépendances PySide6 et sqlalchemy nécessaires au bon fonctionnement du projet
pip install -e .[dev] Pour installer les dépendances développeur telles que ruff, pytest ou build

- Initialisation de la Base de Données
Conformément aux consignes, la base de données doit être initialisée avant le premier lancement via un script dédié.

Bash
python init_db.py
Ce script génère le fichier hotel.db, crée les tables et insère des données pré-exitsantes (chambres et clients par défaut).
Si une base de donnée hotel.db existe déjà elle sera réinitialisée à l'aide de ce script

- Utilisation
Lancement de l'application
Une fois installé, vous pouvez lancer l'interface graphique avec la commande suivante :

Bash
python -m hotel_manager.

Fonctionnalités principales
Gestion des chambres : Ajouter, modifier ou supprimer des chambres (prix, capacité, équipements).

Gestion des clients : Enregistrer de nouveaux clients avec validation des coordonnées.

Réservations : Créer une réservation en sélectionnant un client, une chambre et une période.

- Tests et Qualité
Exécuter les tests unitaires
Les tests couvrent la logique métier et les modèles de données (hors interface graphique).

Bash
pytest tests/
Standards de qualité


Journalisation : Les événements critiques sont consignés dans Application.log.

- Pipeline CI/CD
Le projet utilise GitHub Actions pour automatiser la qualité :

Linter : Vérification de la syntaxe et du style (Ruff).

Tests : Exécution automatique de pytest à chaque push ou Pull Request sur main.

Packaging : Construction automatique du package et publication des artefacts (.whl et .tar.gz) en cas de succès.

