import os
from flask import Flask, request, jsonify
from flask import render_template
from flask import redirect, url_for, session
from database import DBconnection # Importation de la classe DBconnection pour gérer la connexion à la base de données
from bokeh.resources import CDN # Importation de CDN pour charger les ressources de Bokeh
from plot import * # Importation des fonctions liées aux graphiques (evolutionTemp, plotex, etc.)
from plotGraphique import *
import json
from plot2 import *

# Création de l'application Flask
app = Flask(__name__)
app.secret_key = 'luka'

# Objet instancié
db = DBconnection()
# Connexion a la DB
db.connect()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'static/config', 'config.json')

"""
Route /login qui renvoie vers un formulaire de connexion
"""
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Enregistre les données du formulaire
        username = request.form["username"]
        password = request.form["password"]

        #permet de faire une requete
        user = db.fetch_one("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        if user:      
            session["username"] = username # Stockage du nom d'utilisateur dans la session
            return redirect(url_for("dash")) # redirection vers la route du dashboard
        else:
            """
            Si la session n'est pas authentifié alors je renvoie vers la meme page
            """
            return render_template("login/login.html") 
    return render_template("login/login.html")

"""
Route pour permettre au Technicien de se connecter pour configurer l'IHM
"""
@app.route('/loginTech', methods=["GET", "POST"])
def loginTech():
    if request.method == "POST":
        # Enregistre les données du formulaire
        username = request.form["username"]
        password = request.form["password"]

        # Requete stocker dans user qui cherche le mdp et l'user
        user = db.fetch_one("SELECT * FROM techniciens WHERE username = %s AND password = %s", (username, password))
        db.close() #fermeture de la db
        if user:      
            session["username"] = username
            return redirect(url_for("configTech"))
        else:
            """
            Si la session n'est pas authentifié alors je renvoie vers la meme page
            """
            return render_template("login/loginTech.html", message="identifiant incorrect") 
    return render_template("login/loginTech.html")



#rediriger vers /login/
@app.route('/')
def home():
    return redirect(url_for('login'))

"""
Route vers le Dashboard
"""
@app.route('/dashboard')
def dash():
    if "username" in session: # vérification si l'utilisateur est connecté
        # Requête pour récuperer la moyenne des températures
        moyTemp = db.fetch_one("SELECT AVG(temperature) AS moyenne_temperature FROM temp_data", ()) 
        tempMoyenne = moyTemp[0] # récuperation de la valeur tuple et stocker dans une variable
        if tempMoyenne is not None:
            tempMoyenne = round(tempMoyenne, 2)
        else:
            tempMoyenne = "Aucune donnée"

        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_fermes = len(data)
        # Compter le nombre total de SHIELD
        total_shields = sum(len(shields) for shields in data.values())
        
        #génération des graphiques Bokeh
        bokeh_components = evolutionTemp()
        bokeh_components2 = evolutionTemp2()

        """
        Renvoie de la page avec :
            - les graphiques (script, script2,div, div2)
            - la moyenne de température
        """
        return render_template("dashboard/dashboard.html", username=session["username"],ressources=CDN.render(), 
                               script=bokeh_components["script"], 
                               div=bokeh_components["div"],
                               script2=bokeh_components2["script"], 
                               div2=bokeh_components2["div"],
                               tempMoyenne=tempMoyenne,
                               total_shields=total_shields, details=data,
                               total_fermes=total_fermes)
    else: 
        """
        Si la session est pas authentifié on renvoie vers login
        """
        print("no session")
        return redirect(url_for("login"))


"""
Route pour le chemin de déconnexion
"""
@app.route('/logout')
def logout():
    session.pop("username", None)  # Supprime l'utilisateur de la session
    return redirect(url_for("login")) # Retourne vers login

"""
Route pour afficher les graphiques des capteurs
"""
@app.route('/graphique')
def graph():
    if "username" in session :
        bar_script, bar_div = create_bar_chart()
        line_script, line_div = create_line_chart()
        pie_script, pie_div = create_pie_chart()
        return render_template("graphique.html", ressources=CDN.render(), bar_script=bar_script, bar_div=bar_div,
                           line_script=line_script, line_div=line_div,
                           pie_script=pie_script, pie_div=pie_div)
    else:
        return redirect(url_for("login"))


def load_config():
    with open('./static/config/config.json', 'r') as f:
        return json.load(f)
    

"""
Route pour la localisation des capteurs
"""
@app.route('/localisation')
def localisation():
    if "username" in session :
        
        return render_template("localisation.html")
    else:
        return redirect(url_for("login"))
    
@app.route('/get_sensors/<group>')
def get_sensors(group):
    config = load_config()
    return jsonify(config.get(group, []))  # Retourne les capteurs du SHIELD sélectionné

@app.route('/get_data/<shield_id>')
def get_sensor_data(shield_id):
    config = load_config()
    for group in config.values():
        for shield in group:
            if shield['id'] == shield_id:
                return jsonify(shield)  # Retourne les données du capteur
    return jsonify({'error': 'Capteur non trouvé'}), 404  # Si le capteur n'est pas trouvé


"""
Route qui renvoie vers la page de configuration pour le technicien
"""
@app.route('/configTech', methods=["GET", "POST"])
def configTech():
    if "username" in session:
        print(session["username"])
        return render_template("config.html", username=session["username"])
    else:
        return redirect(url_for("loginTech"))

@app.route('/get-config')
def get_config():
    if not os.path.exists(CONFIG_PATH):
        return jsonify({"error": "Le fichier config est introuvable."}), 404

    with open(CONFIG_PATH, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/save-config', methods=['POST'])
def save_config():
    data = request.get_json()
    os.makedirs('config', exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "ok"})


@app.route('/integration', methods=["POST", "GET"])
def get_event():
     # Récupérer les données JSON de la requête
    data = request.get_json()
    
    # Récupérer l'objet JSON en tant que dictionnaire
    object_data = json.loads(data['objectJSON'])
    
    # Extraire la température
    temp = object_data["temp°C"]
    # Insérer la température dans la base de données
    try:
        db.execute_query("INSERT INTO temperature_data (temperature) VALUES (%s)", (temp,))
    except Exception as e:
        print("Erreur DB :", e)
        return jsonify({"error": "Erreur lors de l'insertion"}), 500
    
    return jsonify({
        "message": "Data received successfully",
        "temperature": temp
    }), 200

@app.route('/checkbox')
def checkbox_plot():
    script, div = create_date_slider_plot()
    return render_template('checkbox_plot.html',ressources=CDN.render(), script=script, div=div)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)