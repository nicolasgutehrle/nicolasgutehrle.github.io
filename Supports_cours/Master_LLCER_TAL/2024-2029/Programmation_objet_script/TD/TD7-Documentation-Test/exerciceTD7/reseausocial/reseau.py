class ReseauSocial:
    """
    Classe abstraite représentant un réseau social
    """
    def __init__(self, nom : str, nbr_adherents = 0, nbr_posts = 0):
        """
        Constructeur de la classe

        :param nom: nom du réseau
        :type nom: str
        :param nbr_adherents: nombre d'adhérents au réseau, defaults to 0
        :type nbr_adherents: int, optional
        :param nbr_posts: nombre de posts dans le réseau, defaults to 0
        :type nbr_posts: int, optional
        """
        self.nom = nom
        self.nbr_adherents = nbr_adherents
        self.nbr_posts = nbr_posts
        self.popularite = self.calculerPopularite()
    
    def calculerPopularite(self):
        """
        Méthode abstraite pour calculer la popularité du réseau.
        Doit être implémenté dans les sous-classes
        """
        pass
    
    def ajouterAdherent(self, nbr_adherents : int):
        """
        Ajoute un certain nombre d'adhérents au réseau

        :param nbr_adherents: nombre d'adhérents à ajouter
        :type nbr_adherents: int
        """
        self.nbr_adherents += nbr_adherents
    
    def retirerAdherent(self, nbr_adherents: int):
        """
        Retire un certain nombre d'adhérents au réseau

        :param nbr_adherents: nombre d'adhérents à retirer
        :type nbr_adherents: int
        """
        self.nbr_adherents -= nbr_adherents
        
    def ajouterPosts(self, nbr_posts: int):
        """
        Ajoute un certain nombre de posts au réseau
        

        :param nbr_posts: nombre de posts à ajouter
        :type nbr_posts: int
        """
        self.nbr_posts += nbr_posts
    
    def retirerPosts(self, nbr_adherents: int):
        """
        Retire un certain nombre de posts au réseau

        :param nbr_adherents: nombre de posts à retirer
        :type nbr_adherents: int
        """
        self.nbr_posts -= nbr_adherents

    def __str__(self) -> str:
        """
        Représentation sous forme de str

        :return: retourne le nom du réseau
        :rtype: str
        """
        return self.nom
        

class Perso(ReseauSocial):
    """
    Classe Perso, qui hérite de ReseauSocial

    """
    def __init__(self, nom: int, nbr_adherents: int, nbr_posts: int):
        """
        Constructeur de la classe

        :param nom: nom du réseau
        :type nom: str
        :param nbr_adherents: nombre d'adhérents au réseau, defaults to 0
        :type nbr_adherents: int, optional
        :param nbr_posts: nombre de posts dans le réseau, defaults to 0
        :type nbr_posts: int, optional
        """
        super().__init__(nom, nbr_adherents, nbr_posts)
    
    def calculerPopularite(self):
        """
        Calcule popularité du réseau, ici correspond au nombre d'adhérents

        :return: la popularité du réseau == nombre d'adhérents
        :rtype: int
        """
        return self.nbr_adherents
    
class Images(ReseauSocial):
    """
    Classe Image, qui hérite de ReseauSocial

    """
    def __init__(self, nom: int, nbr_adherents: int, nbr_posts: int):
        """
        Constructeur de la classe

        :param nom: nom du réseau
        :type nom: str
        :param nbr_adherents: nombre d'adhérents au réseau, defaults to 0
        :type nbr_adherents: int, optional
        :param nbr_posts: nombre de posts dans le réseau, defaults to 0
        :type nbr_posts: int, optional
        """
        super().__init__(nom, nbr_adherents, nbr_posts)
    
    def calculerPopularite(self):
        """
        Calcule popularité du réseau, ici correspond au nombre de posts

        :return: la popularité du réseau == nombre de posts
        :rtype: int
        """
        return self.nbr_posts
    
class Blogging(ReseauSocial):
    """
    Classe Blogging, qui hérite de ReseauSocial

    """    
    def __init__(self, nom: int, nbr_adherents: int, nbr_posts: int):
        """
        Constructeur de la classe

        :param nom: nom du réseau
        :type nom: str
        :param nbr_adherents: nombre d'adhérents au réseau, defaults to 0
        :type nbr_adherents: int, optional
        :param nbr_posts: nombre de posts dans le réseau, defaults to 0
        :type nbr_posts: int, optional
        """
        super().__init__(nom, nbr_adherents, nbr_posts)
    
    def calculerPopularite(self):
        """
        Calcule popularité du réseau, ici correspond au nombre d'adhérents * nombre de posts

        :return: la popularité du réseau == nombre d'adhérents * nombre de posts
        :rtype: int
        """
        return  self.nbr_adherents * self.nbr_posts
    
if __name__ == "__main__":
    
    perso = Perso('facebook', 1000, 500)
    print('Popularité Perso :', perso.calculerPopularite())

    images = Images('instagram', 500, 1000)
    print('Popularité Images :', images.calculerPopularite())

    blog = Blogging('twitter', 1000, 1000)
    print('Popularité Blog :', blog.calculerPopularite())
