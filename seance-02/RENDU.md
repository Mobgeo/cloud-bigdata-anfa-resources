# Rendu - Séance 2
**Nom et prénom :** <MABOUDOU Georges N'Nabi>
**Identifiant GitHub :** <Mobgeo>
**Date de soumission :** <23/06/2026>
## Résumé de la séance
<2-4 lignes : Dockerfile écrit, image construite et exécutée, stack Compose à 3 services orchestrée, notebook Jupyter lisant MinIO.>
## Étapes principales
1. Écriture du Dockerfile et construction de l'image `anfa-analyse:v1` (taille observée : 1.17 Go).
2. Mise en place du `.dockerignore` et observation du cache de Docker.
3. Écriture du `docker-compose.yml` orchestrant MinIO, Jupyter, et l'image custom.
4. Création du notebook `exploration_minio.ipynb` qui lit les données depuis MinIO via boto3 et pandas.

## Captures d'écran
### docker compose ps
![docker compose ps](captures/docker-ps.png)
### Notebook Jupyter
![Notebook Jupyter](captures/jupyter-pandas.png)
## Bonus multi-stage (optionnel)
< Nous pouvons voir que la taille de l'image v1 (1.17 GO) est equivalente à la taille de l'image v2-multistage (1.17 GO), ce qui montre un gain de pourcentage nulle.>
## Réponses aux exercices d'application
**EXERCICE 1**
1-C
2-B
3-B
4-A
5-B
6-B
7-C
8-B
**EXERCICE 2**
1-
`FROM python:3.11`: permet de specifier la version de l'image python utilisé
`WORKDIR /application` : définit le repertoire de travail dans le conteneur
`COPY . /application`: copie tout le contenue de ton projet local vers le conteneur
`RUN pip install -r requirements.txt` : installe les bibliothèques python neccessaire.
`EXPOSE 5000` : indique que l'application ecoute sur le port 5000 .
`CMD ["python", "main.py"]` : lance ton application au demarrage du conteneur.
2- 
`EXPOSE 5000`Indique que le conteneur écoute sur le port 5000 mais n'ouvre pas réellement le port vers l’extérieur alors que `-p 5000:5000` lie le port du conteneur à celui de ta machine.
3-deux problèmes dans ce Dockerfile:
- tout le projet est copié avant d’installer les dépendances. Pour resoudre ce problème, il faut que les dépendances ne sont réinstallées que si requirements.txt change. 
`
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
`
- l'image python choisie est lourde et complète. Pour corriger ce problème, il faut choisir une image python plus leger.
`
    FROM python:3.11-slim
`

4-
`
    FROM python:3.11-slim

# Créer un utilisateur non-root
    RUN useradd -m appuser

# Définir le dossier de travail
    WORKDIR /application

# Copier uniquement les dépendances pour optimiser le cache
    COPY requirements.txt .

# Installer les dépendances
    RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
    COPY . .

# Changer le propriétaire des fichiers
    RUN chown -R appuser:appuser /application

# Utiliser l'utilisateur non-root
    USER appuser

# Exposer le port
    EXPOSE 5000

# Lancer l'application
    CMD ["python", "main.py"]
`
**EXERCICE 3**
1-
a- le pip install est executé avant la copie
b- Pour corriger ce dockerfile il faut faire la copie des fichiers neccessaires avant l'execution du code. 
`
    FROM python:3.11-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD ["python", "main.py"]
`
c- Cette erreur illustre une mauvaise compréhension du fonctionnement de Docker, car elle montre que l’utilisateur ne prend pas en compte l’exécution séquentielle des instructions et le système de couches. La commande RUN est exécutée avant que la l'image Docker.
2-
a- chaque image du docker-compose.yml ayant son localhost , il serait une erreur d'utiliser `DATABASE_URL: "postgresql://user:password@localhost:5432/anfa"`
b- pour corriger l'erreur il faut remplacer `DATABASE_URL: "postgresql://user:password@localhost:5432/anfa"` par `DATABASE_URL: "postgresql://user:password@db:5432/anfa"`
**EXERCICE 4**
a- Identifions quatre problèmes dans ce Dockerfile:
- ubuntu:22.04 est volumineuse car elle augmente la taille de l’image finale et ralentit le build.
- plusieurs `RUN` crée une multitude de couches ce qui alourdit la taille de l'image.
- l'execution `RUN apt-get update` crée un cache APT non nettoyé ce qui crée des depots de fichiers temporaires et un gaspillage d'espace disque. 
- Mauvaise gestion du cache Docker : si un fichier change toutes les dépendances de l'application sont completement reinstallées.

b- Proposition d'une amelioration du Dockerfile
`
# Image légère optimisée pour Python
    FROM python:3.11-slim

# Définir le dossier de travail
    WORKDIR /app

# Copier uniquement les dépendances pour profiter du cache Docker
    COPY requirements.txt .

# Installer les dépendances sans cache pour réduire la taille
    RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
    COPY . .

# Créer un utilisateur non-root pour la sécurité
    RUN useradd -m appuser
    USER appuser

# Commande de démarrage
    CMD ["python", "downloader.py"]
`
**EXERCICE 5**
a-
| Service | Image de base | Rôle |
|---|---|---|
| `ftp-reader` | `python:3.11-slim` | Script Python qui se déclenche chaque nuit pour lire les fichiers GPS depuis le FTP, nettoyer les données et écrire les résultats agrégés dans MinIO. |
| `minio` | `minio/minio` | Stockage objet compatible S3 qui joue le rôle de data lake central, persistant les fichiers agrégés accessibles à toute l'équipe. |
| `jupyter` | `jupyter/scipy-notebook` | Environnement notebook interactif permettant à Kossi d'explorer les données MinIO et de produire des visualisations. |
| `airflow` | `apache/airflow` | Orchestrateur qui planifie l'exécution nocturne du pipeline et permet de **rejouer manuellement** une journée précise en quelques clics. |
| `postgres` | `postgres:15` | Base de données relationnelle utilisée par Airflow pour stocker ses métadonnées (DAGs, logs d'exécution, état des tâches). |
b-
**Politique recommandée : `on-failure`**
Le script est une **tâche batch ponctuelle** (il tourne, termine, et s'arrête) : une politique `always` ou `unless-stopped` le relancerait en boucle infinie dès qu'il se termine normalement (exit code `0`), ce qui est absurde pour un job nocturne.

Avec `on-failure`, Docker ne le redémarre qu'en cas de crash inattendu (exit code `≠ 0`), offrant un filet de sécurité sans créer de boucle — sachant que c'est de toute façon **l'orchestrateur (Airflow) qui doit gérer les relances** et la logique de retry métier.
c-
- Mecanisme 1: Variable d'environnement
`docker run --rm -e RUN_DATE=2025-06-15 anfa/ftp-reader`
- Mecanisme 2: dans docker-compose
`
    # docker-compose.override.yml ou à la main
    services:
    ftp-reader:
        command: ["python", "pipeline.py", "--date", "2025-06-15"]
`
Je recommande le mecanisme par variable d'environnement.
d-
Mélanger le script de production et le notebook dans le même conteneur viole le principe de responsabilité unique : Jupyter est un outil interactif d'exploration, pas un runner de jobs batch, et le faire tourner en permanence juste pour exécuter un script nocturne gaspille des ressources.

Sur le plan opérationnel, un crash ou une mise à jour du script affecterait la disponibilité du notebook, et inversement — les cycles de vie des deux composants sont indépendants et doivent le rester.

Enfin, le conteneur ftp-reader peut être lancé, exécuté et détruit par Airflow (--rm) de façon propre et traçable, ce qui est impossible si le script vit dans un Jupyter toujours actif.
e-
`
    version: "3.9"

    services:

    ftp-reader:
        build: ./ftp-reader
        environment:
        - RUN_DATE=${RUN_DATE:-}         # injecté par Airflow ou manuellement
        - MINIO_ENDPOINT=minio:9000
        depends_on:
        - minio
        restart: on-failure

    minio:
        image: minio/minio
        command: server /data --console-address ":9001"
        volumes:
        - minio-data:/data
        ports:
        - "9000:9000"
        - "9001:9001"

    jupyter:
        image: jupyter/scipy-notebook
        volumes:
        - ./notebooks:/home/jovyan/work
        ports:
        - "8888:8888"
        depends_on:
        - minio

    airflow:
        image: apache/airflow:2.9.1
        depends_on:
        - postgres
        environment:
        - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
        volumes:
        - ./dags:/opt/airflow/dags
        ports:
        - "8080:8080"

    postgres:
        image: postgres:15
        environment:
        - POSTGRES_USER=airflow
        - POSTGRES_PASSWORD=airflow
        - POSTGRES_DB=airflow
        volumes:
        - postgres-data:/var/lib/postgresql/data

    volumes:
    minio-data:
    postgres-data:
`
## Difficultés rencontrées
j'ai rencontré des difficultés au niveau du build du stack v1 concernant les ports d'ecoutes pour l'image Minio et pour le jupyter Notebook