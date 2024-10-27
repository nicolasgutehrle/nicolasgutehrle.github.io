from reseausocial.reseau import Perso, Blogging, Images
from reseausocial.utils import plusPopulaire

if __name__ == "__main__":
    
    perso = Perso('facebook', 1000, 500)

    images = Images('instagram', 500, 1000)

    blog = Blogging('twitter', 1000, 1000)

    populaire = plusPopulaire([perso, images, blog])
    print('Plus populaire :', populaire)