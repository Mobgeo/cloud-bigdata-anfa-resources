# Rendu Séance 1
**Nom et prénom :** MABOUDOU Georges N'nabi
## Résumé de la séance
Au cours de cette seance nous avons eu à deployer une image docker denommé Minio. Minio permet de creer des bucket à l'image de ce qui est fait sur s3. Nous avons par la suite definis les parametres de connexions à notre image et le port sur lequel notre image doit tourner. Nous avons par la suite creer un bucket Minio denommé anfa-raw. et uploader des fichier dans ce bucket en utilisant un script python et la librairie boto3. 
## Étapes principales
1-Telechargement de l'image Minio dans le dossier "seance-01"
2-Configuration des parametres de connexion et du port d'ecoute de notre image Docker Minio
3-Creation d'une access et d'une secret key pour notre image Minio
4-Creation d'un bucket Minio "anfa-raw"
5-Creation d'un fichier python "upload_referentiel.py" dans le dossier "seance-01" permettant d'uploader les fichiers contenues dans le dossier "data" vers le bucket "anfa-raw" créeé
6- Chargement des fichiers vers notre Bucket Minio depuis le dossier "seance-01" en utilisant la commande: "python upload_referentiel.py"
## Capture d'écran
-./seance-01/captures/bucket-anfa-raw.png
## Difficultés rencontrées
Pour cet exercice, aucune difficultés n'a été rencontré
## Exercices d'application
**EXERCICE 1**
1-D, car le cloud computing n'est pas obligatoirement open source
2-C, car gmail est un logiciel fournissant des services facturés
3-D, car un Function as a service permettrait d'implementer cette fonction.
4-C, car le cloud hybride permettrait la disponibilité des données confidentielle on premise et ceux à caractère non public sur un cloud public.
5-B, car tout l'infrastructure de l'entreprise est basé chez le fournisseur ce qui crée une dependance et l'empèche de migrer à court terme vers des possibilités open source.
6-C, car ce n'est le faite qu'un service soit managé qui lui rend plus perfomant par rapport à une solution open source.

**EXERCICE 2**
---------------------------------------------------------------
Service | Modele | Justification
`Google Compute Engine (machine virtuelle)` | IAAS | Fournit l'infrastructure neccessaire pour l'entreprise
`AWS Lambda` | FAAS | Permet l'execution de bout de code pour faire une action specifique à un moment donné
`Snowflake (entrepôt de données)` | SAAS | fournit des services d'analyses de données 
`Heroku` | PAAS | fournit une plateforme prète à acceuillir votre application
`Microsoft 365 (Word, Excel en ligne)` | SAAS | Fournit des logiciels d'edition de texte moyennant un abonnement
`Databricks (Spark managé)` | PAAS | fournit un service spark managé le tout sur une plateforme prète
`Microsoft Azure Functions`| FAAS |  Permet l'execution de bout de code de faire une action specifique
`Tableau Online` | SAAS | Permet la visualisation des donneés dans le cloud moyennant un paiement mensuel

**EXERCICE 3**
-3.1
Decortiquons la commande suivante :
docker run -d --name analyse-anfa -p 8888:8888 -v /home/koffi/notebooks:/notebooks \
-e JUPYTER_TOKEN=anfa-token \
jupyter/pyspark-notebook

`-d`: permet executer le conteneur Docker en arriere plan tout en donnant accès à l'invite de commande.
`--name analyse-anfa`: permet de definir le nom de l'image Docker à demarrer.
`-p 8888:8888`: permet de definir le port d'ecoute du conteneur Docker et le port par lequel nous pouvons au ce conteneur à travers le navigateur.
`-v /home/koffi/notebooks:/notebooks`: lie le dossier /home/koffi/notebooks au /notebooks du conteneur.
`-e JUPYTER_TOKEN=anfa-token`: définit un mot de passe pour Jupyter.
`jupyter/pyspark-notebook`: definit l'image que Docker doit demarrer

-3.2
a- l'url est accessible au niveau du navigateur à `http://localhost:9001/`
b- Lors de la suppression du conteneur `anfa-minio` avec la commande `docker rm anfa-minio` puis de la relance avec la commande `docker compose up -d`, le conteneur supprimé, est recrée à partir du fichier `yml`. Les données deposées dans Minio ne sont pas perdues car après la suppression du conteneur, l'image Minio reste et le volume Minio sur lequel sont stockés les données restent également.
c- L'un des problèmes de securité les plus fraglent est le mot de passe en clair dans le fichier `yaml` presenté.

**EXERCICE 4**
a- La paire de clés applicatives générée par le script `mc` n'est pas la bonne
b- il regeneré une clé applicative via la commande 
`mc admin user svcacct add local anfa-admin \
--access-key "anfa-app-key" \
--secret-key "anfa-app-secret-2026" `
c- les identifiants `anfa-admin / anfa-password-2026` sont definis pour une connexion à l'interface web alors qu'ici dans notre code python on definit une clé paire applicative.

**EXERCICE 5**
a-Deux limites concrètes:
- Que tous les analystes accèdent à un tableau de bord partagé, sans installation locale.
- Pouvoir augmenter la capacité de calcul lors des pics (vendredi soir, fêtes).
b- Les 5 caracteristiques du cloud (NIST) correspondant aux besoins de la société
- Pouvoir augmenter la capacité de calcul lors des pics (vendredi soir, fêtes): Elasticité rapide car le cloud permettait de pouvoir augmenter la puissance de calcul ou le nombre de machine à la demande.
- Que tous les analystes accèdent à un tableau de bord partagé, sans installation locale: Accès réseau étendu car chacun des analystes pour acceder aux tableaux depuis sa localisation
- Maîtriser les coûts et conserver la possibilité de changer de fournisseur cloud à terme: Service mesuré car avec le cloud te permet de payer selon ta consommation.
- Recevoir des prédictions de la demande en quasi temps réel (chaque heure): Elasticité rapide car le système doit pouvoir s'adapter à la demande ce qui neccessite une mise à disposition des ressources à la demande.
-  Conserver les données clients dans un environnement contrôlé pour des raisons de conformité: Mutualisation des ressources car les données sont stockées chez le fournisseur cloud. Le fournisseur se charge securisé et de rendre disponible ces données à la demande.
c- 
-----------------------------------------------------------------
Composant | Modele de Service | Justification
le tableau de bord partagé | SAAS | il permet à chacun des analystes l'accès à un tableau partagé sans installation
le calcul des prédictions à l'heure | FAAS | il permet la mise en place d'un bout de code permettant l'execution d'un service.
le stockage des données clients | IAAS | il permet l'administration de l'infrastructure des clients tout en fournissant des services comme le stockage de données.
-------------------------------------------------------------------
d- Je recommenderais le modèle de deploiement en cloud privé car il garantis un meilleur controle sur les données et leur conformités

e- Pratique pour eviter le vendor lock-in:
- utiliser des outils alternatives open source à ceux disponible dans le cloud
- adopter une architecture multicloud
- encapsuler ses applications dans des conteneurs ( Docker / Kubernetes)
