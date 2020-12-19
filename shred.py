# BLART Louise L2 MASS - Projet

from PIL import Image
from random import *

def decoupage (im,nb,prefix):
    """
    :param im: nom d'un fichier image png
    :type im: chaine de caractéres
    :param nb: nombre de bandelettes
    :type b: int
    :param prefix: préfixe des fichiers sortants
    :type prefix: chaine de caractéres
    :return:
       Nombre nb de fichiers images (au format png) au nom commençant par le prefix indiqué.
       Ces fichiers sont créés à partir de l'image im. Ce sont des bandelettes de cette image.
    
    :Examples:
    >>> decoupage('complainte.png',3,'compl')
    création de 3 fichiers:
    -> compl-0.png
    -> compl-1.png
    -> compl-2.png
    """
    l=[i for i in range(nb)]
    shuffle(l)# nom des fichiers pour mélanger les bandelettes
    img=Image.open(im)
    xsize,ysize=img.size
    long_band=int(xsize/nb) # longueur des bandelettes
    a=0
    for n in range(nb):
        if n != nb-1:
            img1=img.crop((a,0,long_band*(n+1),ysize))
            img1.save(prefix+'-'+str(l[n])+'.png')#enregistrement de la bandelette
            a+=long_band
        else:#la dernière bande peut-être un peu plus large que les autres si xsize%0!=0
            img1=img.crop((a,0,xsize,ysize))
            img1.save(prefix+'-'+str(l[n])+'.png')#enregistrement de la dernière bandelette
