import mysql.connector


#Class pour le singleton : ASSURE qu'une seul instance de DBconnection est créée
class Singleton(object):

    # Méthode __new__ : Permet de contrôler la création d'une instance de la classe.
    def __new__(cls, *args, **kw):
        # Vérifie si l'instance de la classe n'a pas déjà été créée
        if not hasattr(cls, '_instance'): 
            # Si aucune instance n'existe, on crée une nouvelle instance
            org = super(Singleton, cls)  # Appelle le constructeur de la classe parente (object)
            cls._instance = org.__new__(cls, *args, **kw)  # Crée l'instance et la stocke dans '_instance'
        # Retourne toujours la même instance
        return cls._instance

"""
Création d'une classe DBConnection qui hérite de la classe Singleton
class composé de méthodes:
    - connect, pour se connecter a la bd
    - fetch_one,  pour executé une requête et la réqupérer en une seul ligne
    - close, pour fermer la connexion a la bd
"""
class DBconnection(Singleton):

    def __init__(self, host="babylone",database="lambrech",user="lambrech",password="lambrech", ssl_disabled=True):
        self.host = host  # Hôte du serveur MySQL
        self.database = database  # Nom de la base de données
        self.user = user  # Utilisateur MySQL
        self.password = password  # Mot de passe MySQL
        self.ssl_disabled = ssl_disabled  # Désactivation de SSL
        self.connection = None  # Initialisation de la connexion à None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host, # Hote du serveur MySQL
            database=self.database, # Nom de la base de donnée
            user=self.user, # Nom de l'utilisateur pour se connecter
            password=self.password, # MDP de l'utilisateur pour se connecter
            ssl_disabled=self.ssl_disabled  # Désactiver SSL
        )
        if self.connection.is_connected():
            print("connecter a la bd") # Affiche si la connexion est réussie
        else:
            print("pas connecter") # Affiche si la connexion échoue

    #Pour SELECT
    def fetch_one(self, query, params):
        self.connect()  # Se connecte à la base de données
        cursor = self.connection.cursor()  # Crée un curseur pour exécuter la requête
        cursor.execute(query, params)  # Exécute la requête avec les paramètres
        result = cursor.fetchone()  # Récupère la première ligne du résultat
        cursor.close()  # Ferme le curseur après l'exécution de la requête
        return result  # Retourne la première ligne récupérée
    

    #Pour INSERT UPDATE DELETE
    def execute_query(self, query, params):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print("Erreur lors de l'exécution :", err)
            return False
        finally:
            cursor.close()


    def close(self):
        self.connection.close()  # Ferme la connexion à la base de données
        print("Connexion fermée")  # Affiche que la connexion est fermée