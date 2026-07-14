# Fiche de conformité — Application mobile passagers Anfa

> Gabarit fourni. Complétez chaque section **en 2-4 lignes**, en vous appuyant sur le CM.
> Il n'y a pas de "bonne réponse" unique sur certains points — l'important est le raisonnement.

## 1. Finalité du traitement
<Pourquoi collecte-t-on ces données ? À quel usage précis, et à aucun autre ?>
Les données sont collectées pour améliorer l’expérience utilisateur des passagers. La position GPS permet de proposer les trajets les plus proches en temps réel, tandis que l’historique de paiements sert à gérer les abonnements. Le numéro de téléphone agit comme identifiant unique pour authentifier et contacter l’utilisateur. Les données ne doivent pas être utilisées à des fins commerciales sans consentement explicite.

## 2. Données collectées et leur sensibilité
<Lister les 3 données du scénario. Laquelle est la plus sensible et pourquoi ?>
Les données collectées sont : la position GPS, l’historique de paiements mobile money et le numéro de téléphone. La donnée la plus sensible est la position GPS, car elle permet de suivre les déplacements d’un individu en temps réel, ce qui peut porter atteinte à sa vie privée. L’historique de paiement est également sensible car il révèle des habitudes financières.

## 3. Base légale applicable
<Quel texte togolais s'applique à quelle donnée ? (Loi 2019-014 ? Loi 2017-007/2023-012 ?
Les deux peuvent s'appliquer à une même donnée — expliquez pourquoi.)>
La loi togolaise n°2019-014 relative à la protection des données personnelles s’applique à l’ensemble des données collectées, car elles permettent d’identifier directement ou indirectement une personne. La loi n°2017-007 modifiée par 2023-012 peut aussi s’appliquer pour les aspects liés aux transactions électroniques (paiements mobile money). Le traitement doit reposer sur le consentement explicite de l’utilisateur.

## 4. Durée de conservation
<Combien de temps ces données devraient-elles être gardées ? Justifiez en lien
avec le principe de "minimisation" vu en CM.>
Les données doivent être conservées uniquement pendant la durée nécessaire à leur finalité. La position GPS pourrait être conservée très brièvement (quelques minutes ou heures), tandis que les données de paiement peuvent être conservées plus longtemps pour des obligations comptables. Cela respecte le principe de minimisation des données vu en CM.

## 5. Hébergement et souveraineté
<Où ces données doivent-elles être hébergées pour rester conformes à la loi
togolaise ? Quel est le risque si on héberge chez un cloud américain ? (Patriot Act)>
Les données devraient idéalement être hébergées au Togo ou dans un pays offrant un niveau de protection équivalent. Héberger les données chez un fournisseur américain expose au risque d’accès par les autorités via des lois comme le Patriot Act. Cela peut compromettre la souveraineté des données et la confidentialité des utilisateurs.

## 6. Droit des personnes concernées
<Un passager doit-il pouvoir demander la suppression de ses données ? Le système
technique actuel d'Anfa (tel que vous l'avez construit depuis la séance 1) le
permettrait-il facilement ? Pourquoi ?>
Oui, un passager doit pouvoir demander l’accès, la modification ou la suppression de ses données. Dans le système actuel d’Anfa (basé sur stockage S3 et base de données), cela peut être complexe sans mécanisme spécifique de gestion des droits. Il faudrait prévoir des fonctionnalités dédiées pour répondre efficacement aux demandes des utilisateurs.
