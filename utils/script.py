class script(object):
    START = """{},

Je suis un bot de recherche de publications,
je vais filtrer automatiquement les publications de votre canal et les envoyer dans votre groupe lorsqu’un utilisateur les recherche.

<b>Envoyez /help pour plus d’informations</b>"""

    HELP = """<b>‼️  Comment m’utiliser dans un groupe  ‼️</b>

❂ Ajoutez-moi en tant qu’admin dans votre groupe et votre canal.
❂ Tapez /verify dans le groupe.

❂ Attendez que votre demande soit vérifiée par <b><a href="https://telegram.me/ZeeXDevBot">le propriétaire</a></b>

❂ Après vérification, envoyez /connect suivi de l’ID de votre canal
<b>⤨ Exemple -</b>

/connect -100xxxxxxxxxxx

❂ Supprimer un canal avec
/disconnect -100xxxxxxxxxxx
Cela vous permettra de retirer un canal indexé de votre groupe.

❂ Pour ajouter une souscription forcée dans le groupe, tapez /fsub suivi de l’ID de votre canal
<b>⤨ Exemple -</b>

/fsub -100xxxxxxxxxx

❂ Pour supprimer la souscription forcée, tapez /nofsub

❂ Obtenez la liste des canaux connectés avec
/connections

<b>NOTE:</b> Ces fonctionnalités sont uniquements dispo pour les membres VIP 2nd"""

    ABOUT = """<b>➣ Mon nom ⋟  {}</b>
<b>➢ Créateur ⋟  <a href=https://telegram.me/ZeeXDevBot>Kingcey</a></b>
<b>➢ Canal ⋟  <a href=https://t.me/ZeeXDev>ZeeX Dev</a></b>
<b>➢ Canal Animes⋟  <a href=https://t.me/Godanimes>Animes God</a></b>
<b>➢ Langage ⋟  <a href=https://www.python.org>Python 3</a></b>
<b>➣ Base de données ⋟  <a href=https://www.mongodb.com>MongoDB</a></b>
<b>➢ Serveur du bot ⋟  <a href=https://heroku.com>Heroku</a></b>
<b>➣ Statut de build ⋟  v3.0.1 (bêta)</b>"""

    STATS = """<b>Statut actuel   📊</b>

👤 <b>Total utilisateurs : {}</b>
♻️ <b>Total groupes : {}</b>"""

    BROADCAST = """<u>{}</u>

Total : {}
Restant : {}
Réussis : {}
Échecs : {}"""