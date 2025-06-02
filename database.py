import mysql.connector

# Classe pour le singleton : ASSURE qu'une seule instance de DBconnection est créée
class Singleton(object):
    def __new__(cls, *args, **kw):
        # Vérifie si l'instance de la classe n'a pas déjà été créée
        if not hasattr(cls, '_instance'):
            org = super(Singleton, cls)  # Appelle le constructeur de la classe parente (object)
            cls._instance = org.__new__(cls, *args, **kw)  # Crée l'instance et la stocke dans '_instance'
        # Retourne toujours la même instance
        return cls._instance

"""
Création d'une classe DBConnection qui hérite de la classe Singleton
class composé de méthodes:
    - connect, pour se connecter à la BD
    - fetch_one, pour exécuter une requête et la récupérer en une seule ligne
    - close, pour fermer la connexion à la BD
"""
class DBconnection(Singleton):
    def __init__(self, host="babylone", database="lambrech", user="lambrech", password="lambrech", ssl_disabled=True):
        self.host = host  # Hôte du serveur MySQL
        self.database = database  # Nom de la base de données
        self.user = user  # Utilisateur MySQL
        self.password = password  # Mot de passe MySQL
        self.ssl_disabled = ssl_disabled  # Désactivation de SSL
        self.connection = None  # Initialisation de la connexion à None

    def connect(self):
        # Si la connexion n'est pas déjà établie
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=self.host,  # Hôte du serveur MySQL
                database=self.database,  # Nom de la base de données
                user=self.user,  # Nom de l'utilisateur pour se connecter
                password=self.password,  # Mot de passe de l'utilisateur pour se connecter
                ssl_disabled=self.ssl_disabled  # Désactiver SSL
            )
            if self.connection.is_connected():
                print("Connecté à la base de données")  # Affiche si la connexion est réussie
            else:
                print("Échec de la connexion à la base de données")  # Affiche si la connexion échoue
        return self.connection  # Retourne la connexion existante ou nouvellement créée

    # Pour SELECT
    def fetch_one(self, query, params):
        connection = self.connect()  # Se connecte à la base de données si ce n'est pas déjà fait
        cursor = connection.cursor()  # Crée un curseur pour exécuter la requête
        cursor.execute(query, params)  # Exécute la requête avec les paramètres
        result = cursor.fetchone()  # Récupère la première ligne du résultat
        cursor.close()  # Ferme le curseur après l'exécution de la requête
        return result  # Retourne la première ligne récupérée

    # Pour INSERT, UPDATE, DELETE
    def execute_query(self, query, params):
        connection = self.connect()  # Se connecte à la base de données
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()  # Confirme la transaction
            return True
        except mysql.connector.Error as err:
            print("Erreur lors de l'exécution :", err)
            return False
        finally:
            cursor.close()

    def close(self):
        # Ferme la connexion à la base de données si elle est encore ouverte
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connexion fermée")
        else:
            print("Aucune connexion à fermer")
