import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def mobius_strip(n=10000, w=0.1):
    """
    Génère un ruban de Möbius.
    
    Paramètres:
    n (int): Nombre de points pour générer le ruban.
    w (float): Largeur du ruban.
    
    Retourne:
    tuple: Coordonnées x, y, z du ruban de Möbius.
    """
    theta = np.linspace(0, 2 * np.pi, n)
    width = np.linspace(-w, w, 2)
    theta, width = np.meshgrid(theta, width)
    
    # Paramétrisation du ruban de Möbius
    x = (1 + width * np.cos(theta / 2)) * np.cos(theta)
    y = (1 + width * np.cos(theta / 2)) * np.sin(theta)
    z = width * np.sin(theta / 2)
    
    return x, y, z

def plot_mobius_strip(x, y, z):
    """
    Affiche un ruban de Möbius en 3D.
    
    Paramètres:
    x, y, z (array): Coordonnées du ruban de Möbius.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, color='b', edgecolor='k', alpha=0.7)
    ax.set_title("Ruban de Möbius")
    plt.show()

# Génération et visualisation du ruban de Möbius
x, y, z = mobius_strip()
plot_mobius_strip(x, y, z)