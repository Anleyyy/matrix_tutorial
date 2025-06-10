import math

def rotation(A, B, alpha):
    """
    Fait tourner le point A autour du point B d'un angle alpha (en radians).

    Paramètres :
    - A : tuple (x, y) représentant les coordonnées du point A
    - B : tuple (x, y) représentant les coordonnées du point B (centre de rotation)
    - alpha : angle de rotation en radians

    Retour :
    - tuple (x, y) représentant les coordonnées du point C, image de A après rotation
    """
    xa, ya = A
    xb, yb = B

    # Translation du point A pour que B devienne l'origine
    x_trans = xa - xb
    y_trans = ya - yb

    # Rotation autour de l'origine
    x_rot = x_trans * math.cos(alpha) - y_trans * math.sin(alpha)
    y_rot = x_trans * math.sin(alpha) + y_trans * math.cos(alpha)

    # Re-translation pour remettre le centre à B
    x_final = x_rot + xb
    y_final = y_rot + yb

    return (x_final, y_final)

def translation(A, u):
    """
    Translate le point A selon le vecteur u.

    Paramètres :
    - A : tuple (x, y) représentant les coordonnées du point A
    - u : tuple (ux, uy) représentant le vecteur de translation

    Retour :
    - tuple (x, y) représentant les coordonnées du point B après translation
    """
    xa, ya = A
    ux, uy = u

    xb = xa + ux
    yb = ya + uy

    return (xb, yb)

def symetrie(A, P, u):
    """
    Calcule l'image du point A par symétrie par rapport à la droite affine D
    passant par le point P et dirigée par le vecteur u.

    Paramètres :
    - A : tuple (x, y), le point à refléter
    - P : tuple (xp, yp), un point appartenant à la droite
    - u : tuple (ux, uy), le vecteur directeur de la droite (non nul)

    Retour :
    - tuple (x, y), le point symétrique de A par rapport à la droite affine
    """
    ax, ay = A
    px, py = P
    ux, uy = u

    # Vecteur AP
    apx = ax - px
    apy = ay - py

    # Norme au carré de u
    norme_u2 = ux**2 + uy**2
    if norme_u2 == 0:
        raise ValueError("Le vecteur directeur de la droite ne peut pas être nul.")

    # Projection scalaire de AP sur u
    dot = apx * ux + apy * uy

    # Coordonnées du projeté de A sur la droite (P + u)
    proj_x = px + (dot / norme_u2) * ux
    proj_y = py + (dot / norme_u2) * uy

    # Calcul du point symétrique : S = 2*proj - A
    sym_x = 2 * proj_x - ax
    sym_y = 2 * proj_y - ay

    return (sym_x, sym_y)

def f(num_cote1, num_cote2, bool_symetrie, pentagone):
    """
    Calcule le correspondant du point X sur le pentagone obtenu en collant cote1 et cote2 et en faisant ou non une symétrie

    Paramètres :
    - X_i : l'indice du point dont on cherche le correspondant dans la liste des points de pentagone
    - num_cote1 : le numéro du coté 1
    - num_cote2 : le numéro du coté 2
        EA a pour numéro 0, AB pour numéro 1, etc ...
    - symetrie : un booléen vrai s'il faut faire une symétrie
    - pentagone : un tuple (points, angles)
        en nommant le pentagone ABCDE où la liste points est dans l'ordre A, B, C, D, E alors il faut que 
            - angles soit dans le même ordre
        - points[i] = (x, y) coordonées du point correspondant
        - cotés[i] est la longueur du coté correspondant
        - angles[i] est l'angle du point d'indice i en radian

    Retour :
    - tuple (x, y), le point correspondant à X
    """
    points = list(pentagone[0])
    angles = pentagone[1]

    num_cote = num_cote1
    while num_cote != num_cote2:
        new_points = []
        for point in points:
            new_points.append(rotation(point, points[num_cote], -(math.pi - angles[num_cote])))
        points = new_points
        num_cote += 1
        if num_cote == 5:
            num_cote = 0

    ux = pentagone[0][num_cote1][0] - points[num_cote2][0]
    uy = pentagone[0][num_cote1][1] - points[num_cote2][1]

    new_points = []
    for point in points:
        new_points.append(translation(point, (ux, uy)))
    points = new_points

    print(points)

    if bool_symetrie:
        ux = points[num_cote2][0] - points[num_cote2-1][0]
        uy = points[num_cote2][1] - points[num_cote2-1][1]
        new_points = []
        for point in points:
            new_points.append(symetrie(point, points[num_cote2], (ux, uy)))
        points = new_points

    else:
        new_points = []
        x, y = (points[num_cote2][0] + points[num_cote2-1][0])/2, (points[num_cote2][1] + points[num_cote2-1][1])/2
        for point in points:
            new_points.append(rotation(point, (x, y), math.pi))
        points = new_points
    return points

deg_to_rad = lambda x: x*math.pi/180
angles_deg = [36, 144, 108, 36, 216]

pentagone = ([(0.95, 2.94), (5,0), (16.91, 0), (20, 9.51), (10.95, 2.94)], [deg_to_rad(angle) for angle in angles_deg])
print([(round(i, 2), round(j, 2)) for i,j in f(3, 0, True, pentagone)])
