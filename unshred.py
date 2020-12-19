# BLART Louise L2 MASS - Projet
# Difficulté: identification des motifs.

from PIL import Image
import colors
import glob


def compare(image_gauche,image_droite):
    """
    :param image_gauche: nom d'un fichier image png
    :type image_gauche: chaine de caractéres
    :param image_droite: nombre de bandelettes
    :type image_droite: chaine de caractéres
    :return:
       Nombre 'score' de pixels noirs cote à cote entre les deux bandelettes.
    :Examples:
    >>> compare('compl-0.png','compl-1.png')
    9
    """
    score=0
    img_gauche=Image.open(image_gauche)
    img_droite=Image.open(image_droite)
    img_gauche=img_gauche.convert('RGB')
    img_droite=img_droite.convert('RGB')
    xgsize,ygsize=img_gauche.size
    xdsize,ydsize=img_droite.size
    assert ydsize == ygsize,'les bandelettes doivent avoir la meme hauteur'
    for y in range(ygsize):
        pixelg=img_gauche.getpixel((xgsize-1,y))
        pixeld=img_droite.getpixel((0,y))
        if colors.brightness(pixelg)==0 and colors.brightness(pixelg)==colors.brightness(pixeld):
            img_gauche.putpixel((xgsize-1,y),colors.red)
            img_droite.putpixel((0,y),colors.red)
            score+=1
    return score
    
    
def liste_score (prefix):
    '''
    :param prefix: préfixe des fichiers sortants
    :type prefix: chaine de caractéres
    :return:
    Une liste de liste des score de chacune des images entre elles.
    Exemple:
    >>> liste_score('compl-')
    [['/', 0, 0, 0], [9, '/', 4, 0], [35, 0, '/', 0], [0, 0, 0, '/']]
    '''
    l= sorted(glob.glob(prefix+"*png"))
    score=[]
    t=[]
    for d in l:
        for g in l:
            if g!=d:
                t.append(compare(g,d))
            else:
                t.append('/')
        score.append(t)
        t=[]
    return score
 


class unshred:
    def __init__ (self,prefix):
        self.__prefix=prefix
        self.__resultat=[]
        self.__liste=liste_score(self.__prefix)
        self.__img=0

    def grille(self):
        '''
    :return: La grille des scores des bandelettes d'une image
    Exemple: score de la grille des bandelettes non mélangées:
    >>>  u.grille()
     0    1    2    3    4    5    6
   +----+----+----+----+----+----+----
0  | /  | 0  | 0  | 0  | 0  | 0  | 0  |
   +----+----+----+----+----+----+----
1  | 26  | /  | 16  | 1  | 8  | 1  | 0  |
   +----+----+----+----+----+----+----
2  | 3  | 25  | /  | 1  | 17  | 1  | 0  |
   +----+----+----+----+----+----+----
3  | 15  | 19  | 32  | /  | 1  | 5  | 0  |
   +----+----+----+----+----+----+----
4  | 12  | 7  | 10  | 9  | /  | 1  | 0  |
   +----+----+----+----+----+----+----
5  | 11  | 0  | 2  | 7  | 20  | /  | 0  |
   +----+----+----+----+----+----+----
6  | 0  | 2  | 3  | 0  | 0  | 4  | /  |
   +----+----+----+----+----+----+----
    '''
        print ('    ','    '.join(str(x) for x in range(len(self.__liste))))
        k=0
        for i in self.__liste:
            print('  ','+----'*len(self.__liste))
            print(k,' |',end='')
            for j in i:
                print('',j,end='  |')
            print()
            k+=1
        
        print('  ','+----'*len(self.__liste))


    def premiere(self):
        '''
    :return: la premiere bandelette de l'image, c'est à dire celle située tout à gauche. Son score avec une bandelette à gauche est forcement de 0. 

    Exemple:
    >>> img=unshred('compl')
    >>> img.premiere()
    >>> img.get_resultat()
    [4]
    '''
        b=[]#si plusieurs cas sont possible pour la première bandelette, il faudra identifier quelle image finale est valable
        for i in self.__liste :
            a=[]
            for j in i :
                if j!=0 and j!='/':
                    a.append(j)
            if a==[]:
                b.append(self.__liste.index(i))
        if len(b)==1:
            self.__resultat.append(b[0])
        else:
            self.__resultat=[b]


    def resultat(self):
        p = self.__resultat[-1]
        M=max([l[p] for l in self.__liste if l[p]!='/'])
        for l in self.__liste:
            if(l[p])==M:
                self.__resultat.append(self.__liste.index(l))
        if len(self.__resultat)!=len(self.__liste)-1:
            return self.resultat()


    def derniere(self):
        ''' la dernière image est constituée d'un score de 0 pour toutes les images pouvant être à sa droite. Elle est a l'extréminé de l'image.
    '''
        b=[]#si plusieurs cas sont possible pour la derniere bandelette, il faudra identifier quelle image finale est valable
        for i in range(len(self.__liste)) :
            a=[]
            for j in self.__liste:
                if j[i]!=0 and j[i]!='/':
                    a.append(i)
            if a==[]:
                b.append(i)
        if len(b)==1:
            self.__resultat.append(b[0])
        else:
            self.__resultat=[b]
    

    def get_resultat(self):
        return self.__resultat


    def reconstitution (self):
        img_left=Image.open(self.__prefix+'-'+str(self.__resultat[0])+'.png')
        img_left.save('image_reconstituee.png')
        for i in range(1,len(self.__resultat)):
            img_right=Image.open(self.__prefix+'-'+str(self.__resultat[i])+'.png')
            xsize1,ysize1=img_right.size
            imjoin=Image.open('image_reconstituee.png')
            xsize,ysize=imjoin.size
            img=Image.new("RGB",(xsize+xsize1,ysize))
            img.paste(imjoin,(0,0))
            img.paste(img_right,(xsize,0))
            img.save('image_reconstituee.png')
        self.__img=imjoin.copy()


    def programme_final (self):
        ''' programme qui reconstitue une image a partir de bandelettes.
    L'image obtenue sera enregistrée dans le dossier.
    Exemple:
    >>> u=unshred('compl-')
    >>> u.programme_final()
    "l'image reconstituée est enregistrée dans votre dossier"
    '''
        self.premiere()
        self.resultat()
        self.derniere()
        liste=self.get_resultat()
        for i in liste :
            if type(i) ==int:
                self.reconstitution()
                return ("l'image reconstituée est enregistrée dans votre dossier")
            else:# Ce cas peut servir si deux scores entre deux images sont égaux 
                a=liste.index(i)
                for l in i :
                    liste2=liste
                    liste2[a]=l
                    self.__resultat=liste2
                    print (self.__img.show() )
                    self.reconstitution()
                    b=input("L'image enregistrée dans le dossier est-elle juste? (répondre Oui ou Non)")
                    if b=='Non':
                        pass
                    else:
                        return 
