from bokeh.plotting import figure
from database import DBconnection

from bokeh.embed import components

def plotex():
    plot = figure(width=600, height=300)

    # - L'argument [1,2,3] représente les coordonnées sur l'axe des abscisses (x).
    # - L'argument [4,5,6] représente les coordonnées sur l'axe des ordonnées (y).
    # La largeur de la ligne tracée est de 2 pixels grâce à `line_width=2`.
    plot.line([1, 2, 3], [4, 5, 6], line_width=2)

    # `components(plot)` génère un script et un div pour intégrer le graphique dans une page HTML.
    # - `script` contient le code JavaScript nécessaire pour afficher le graphique.
    # - `div` contient le HTML nécessaire pour afficher le graphique dans un élément div spécifique.
    script, div = components(plot)

    # Retourne un dictionnaire avec le script et le div générés
    return {"script": script, "div": div}


def evolutionTemp():
    db = DBconnection()
    
    # Température et jours
    query = "SELECT jour, valeur FROM temperature ORDER BY jour ASC"
    
    try:
        connection = db.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print("Erreur lors de la récupération des données :", e)
        return {"script": "", "div": ""}
    
    # Séparer les résultats en deux listes : x (jours), y (valeurs)
    jours = [row[0] for row in result]
    valeurs = [row[1] for row in result]

    # Créer le graphique Bokeh
    plot = figure(width=500, height=300, title="Évolution des températures")
    plot.line(jours, valeurs, line_width=2)
    plot.xaxis.axis_label = "Jour"
    plot.yaxis.axis_label = "Température (°C)"
    plot.legend.location = "top_left"

    script, div = components(plot)
    return {"script": script, "div": div}


 #`components(plot)` génère un script et un div pour intégrer le graphique dans une page HTML.
 # - `script` contient le code JavaScript nécessaire pour afficher le graphique.
 # - `div` contient le HTML nécessaire pour afficher le graphique dans un élément div spécifique.
def evolutionTemp2():
    plot = figure(width=500, height=300)
    plot.line([1,2,3],[4,5,6], line_width=2)
    script, div = components(plot)
    return {"script" : script, "div": div}
