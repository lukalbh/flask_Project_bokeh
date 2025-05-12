from bokeh.plotting import figure
from database import DBconnection
import numpy as np

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
    plot = figure(width=500, height=300)
    plot.line([1,2,3],[4,5,6], line_width=2)
    script, div = components(plot)
    return {"script" : script, "div": div}

def evolutionTemp2():
    plot = figure(width=500, height=300)
    plot.line([1,2,3],[4,5,6], line_width=2)
    script, div = components(plot)
    return {"script" : script, "div": div}
