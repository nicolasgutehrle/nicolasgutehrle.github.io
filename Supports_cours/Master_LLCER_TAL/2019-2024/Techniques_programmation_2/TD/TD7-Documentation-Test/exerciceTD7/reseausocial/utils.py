def plusPopulaire(list_reseaux):
    """
    Compare la popularité de plusieurs réseau, et retourne 
    le plus populaire

    :param list_reseaux: liste des réseaux à comparer
    :type list_reseaux: list[Reseau]
    :return: le réseau le plus populaire
    :rtype: Reseau
    """

    list_popularite = []
    for reseau in list_reseaux:
        list_popularite.append(reseau.popularite)
    max_value = max(list_popularite)
    for reseau in list_reseaux:
        if reseau.popularite == max_value:
            return reseau