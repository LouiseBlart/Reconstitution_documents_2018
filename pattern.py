# BLART Louise L2 MASS - Projet
#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Pattern module
"""

from PIL import Image


class Pattern(object):
    """
    Pattern constructor

    :param list_coords: (a list of pixel coordinates)
    :type list_coords: list of (int,int)
    :rtype: Pattern
    :return: the pattern built from the list coordinates
    :UC: list_coords is not empty

    """
    
    def __init__(self, list_coords):
        self.__list_coords = list_coords



    def get_coords(self):
        """
        Return the list of all coordinates of the pattern

        :rtype: list of (int,int)
        """
        return self.__list_coords
    
    def get_moments(self):
        """
        Return the list of the 9 moments of the pattern

        :rtype: list of floats

        exemples:
        >>>l=Pattern([(1,4),(2,5),(3,6)])
        >>> l.get_moments()
        [3.0, 0.0, 2.0, 0.0, 2.0, 0.0, 2.0, 0.0, 2.0]
        
        """
        surface=len(self.__list_coords)
        assert surface>0,'la liste de coordonnées du motifs doit contenir des coordonnées'
        xc=0 #valeur x du centre de gravité
        yc=0 #valeur y du centre de gravité
        for i in self.__list_coords:
            xc+=i[0]
            yc+=i[1]
        centre=(xc/surface,yc/surface)
        xc,yc=centre# valeur x et y du centre de gravité 
        somme=0
        moments=[]#liste des Moments(P,(d,e)) avec P de coordonnées self.__list_coords, d et e des variables indépendantes de 0 à 2 inclus
        for d in range(3):
            for e in range(3):
                for i in self.__list_coords:
                    x=i[0]
                    y=i[1]
                    somme +=((x-xc)**d)*((y-yc)**e)
                moments.append(somme)
                somme=0
        return moments
                    
            
    
    def distance(self,p2):
        """
        Return the distance between the patterns self and p2

        :rtype: a non negative float
        """
        l1=self.get_moments()
        l2= p2.get_moments()# deux listes à comparer
        d=0
        for i in l1:
            for j in l2:
                if abs(i-j)>d:
                    d=abs(i-j)#maximum de distance entre 2 moments
        return d
