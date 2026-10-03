# Ruban de Möbius

- `index.html` : visualisation interactive (aucune dépendance, ouvrir dans un navigateur).
  Rotation à la souris, zoom, largeur, nombre de demi-tours (0 = cylindre, 1 = Möbius),
  fourmi qui parcourt la ligne médiane (la normale s'inverse après un tour),
  découpe au milieu, bords en rouge.
- `Mobius.py` : version Python (`numpy`, `matplotlib`).
  `python Mobius.py --verifier --save mobius.png`, `python Mobius.py --gif mobius.gif`.
