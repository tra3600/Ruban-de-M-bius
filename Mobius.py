"""Ruban de Möbius : génération, visualisation 3D, animation et vérifications.

Usage :
    python Mobius.py                      # fenêtre interactive
    python Mobius.py --save mobius.png    # image
    python Mobius.py --gif mobius.gif     # animation (rotation + fourmi)
    python Mobius.py --demi-tours 2       # variantes (0 = cylindre, 2 = anneau tordu)
"""
import argparse

import numpy as np
import matplotlib

# (backend choisi plus bas selon --save / --gif)


def mobius_strip(n=400, m=24, w=0.3, R=1.0, demi_tours=1):
    """Génère la surface paramétrée du ruban.

    x = (R + v cos(k u/2)) cos u
    y = (R + v cos(k u/2)) sin u
    z =      v sin(k u/2)          avec u in [0, 2π], v in [-w, w]

    Paramètres:
        n: points le long du ruban, m: points sur la largeur,
        w: demi-largeur, R: rayon de la ligne médiane,
        demi_tours: nombre de demi-tours (1 = Möbius, 0 = cylindre).
    Retourne (x, y, z, u, v), tableaux de forme (m, n).
    """
    if w >= R:
        raise ValueError("w doit être < R pour éviter l'auto-intersection")
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, n), np.linspace(-w, w, m))
    k = demi_tours / 2
    r = R + v * np.cos(k * u)
    return r * np.cos(u), r * np.sin(u), v * np.sin(k * u), u, v


def normal(u, v=0.0, R=1.0, demi_tours=1):
    """Vecteur normal unitaire en (u, v) = produit vectoriel ∂u × ∂v."""
    k = demi_tours / 2
    u = np.asarray(u, dtype=float)
    c, s = np.cos(k * u), np.sin(k * u)
    r = R + v * c
    du = np.array([-r * np.sin(u) - v * k * s * np.cos(u),
                   r * np.cos(u) - v * k * s * np.sin(u),
                   v * k * c])
    dv = np.array([c * np.cos(u), c * np.sin(u), s])
    nrm = np.cross(du, dv, axis=0)
    return nrm / np.linalg.norm(nrm, axis=0)


def verifier(R=1.0, demi_tours=1):
    """Vérifie numériquement les propriétés du ruban (une seule face, un seul bord)."""
    n0, n1 = normal(0.0, R=R, demi_tours=demi_tours), normal(2 * np.pi, R=R, demi_tours=demi_tours)
    return {
        "normale_au_depart": n0,
        "normale_apres_un_tour": n1,
        "orientable": bool(np.allclose(n0, n1)),   # False pour Möbius
        "nb_bords": 1 if demi_tours % 2 else 2,
    }


def plot_mobius_strip(x, y, z, u, ax=None, ant=True, demi_tours=1, R=1.0):
    """Trace le ruban (couleur = position u) avec sa ligne médiane et son bord."""
    import matplotlib.pyplot as plt
    from matplotlib import cm
    if ax is None:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(x, y, z, facecolors=cm.viridis(u / (2 * np.pi)), rstride=2,
                    cstride=4, linewidth=0.1, edgecolor=(0, 0, 0, 0.15), shade=False)
    ax.plot(x[0], y[0], z[0], "r", lw=2)
    ax.plot(x[-1], y[-1], z[-1], "r", lw=2)  # même courbe pour Möbius : un seul bord
    mid = len(x) // 2
    ax.plot(x[mid], y[mid], z[mid], "w--", lw=1)
    ax.set_box_aspect((1, 1, 0.45)); ax.view_init(elev=35, azim=-60)
    ax.set_axis_off()
    ax.set_title("Ruban de Möbius" if demi_tours % 2 else f"Ruban à {demi_tours} demi-tour(s)")
    return ax


def animate(save_gif=None, n_frames=120, **kw):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    x, y, z, u, v = mobius_strip(**kw)
    R, dt = kw.get("R", 1.0), kw.get("demi_tours", 1)
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    plot_mobius_strip(x, y, z, u, ax, demi_tours=dt)
    ant, = ax.plot([], [], [], "ro", ms=9)
    state = {"q": None}

    def update(i):
        t = 4 * np.pi * i / n_frames          # deux tours : retour sur la même face
        px, py, pz = (R * np.cos(t), R * np.sin(t), 0 * t)
        off = 0.03 * normal(t, 0.0, R, dt)    # fourmi posée sur la face
        ant.set_data([px + off[0]], [py + off[1]])
        ant.set_3d_properties([pz + off[2]])
        if state["q"] is not None:
            state["q"].remove()
        state["q"] = ax.quiver(px, py, pz, *(0.4 * normal(t, 0.0, R, dt)), color="red")
        ax.view_init(elev=28, azim=-60 + 360 * i / n_frames)
        return ant,

    anim = FuncAnimation(fig, update, frames=n_frames, interval=40)
    if save_gif:
        anim.save(save_gif, writer="pillow", fps=25)
    return anim


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n", type=int, default=400)
    p.add_argument("--largeur", type=float, default=0.3, help="demi-largeur w")
    p.add_argument("--demi-tours", type=int, default=1)
    p.add_argument("--save", help="enregistre une image (png, svg...)")
    p.add_argument("--gif", help="enregistre une animation gif")
    p.add_argument("--verifier", action="store_true", help="affiche les propriétés vérifiées")
    a = p.parse_args()
    if a.save or a.gif:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    kw = dict(n=a.n, w=a.largeur, demi_tours=a.demi_tours)
    info = verifier(demi_tours=a.demi_tours)
    if a.verifier:
        for k_, v_ in info.items():
            print(f"{k_}: {v_}")
    if a.gif:
        animate(a.gif, **kw)
        print("écrit", a.gif)
        return
    x, y, z, u, v = mobius_strip(**kw)
    plot_mobius_strip(x, y, z, u, demi_tours=a.demi_tours)
    if a.save:
        plt.savefig(a.save, dpi=150, bbox_inches="tight")
        print("écrit", a.save)
    else:
        plt.show()


if __name__ == "__main__":
    main()
