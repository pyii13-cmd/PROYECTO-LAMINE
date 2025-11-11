# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""

class SearchMetadata:
    """
    Classe per cercar imatges segons metadades
    """
    def __init__(self, metadata_dict: dict):
        self.image_data = metadata_dict

    def busqueda(self, camp: str, sub: str) -> list:
        """
        Funció interna per a realitzar una cerca de subcadena.
        
        Args:
            camp (str): Camp de metadades a cercar
            sub (str): subcadena de text
            
        Returns:
            list: Una llista de cadenes UUID que contenen la subcadena
        """
        res = []
        for uuid, metadata in self.image_data.items():
            field_value = metadata.get(camp, "") #filtrem pel camp
            if str(field_value).find(sub) != -1:
                res.append(uuid)
        return res
    
    def prompt(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Prompt."""
        return self.busqueda('Prompt', sub)

    def model(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Model."""
        return self.busqueda('Model', sub)
    
    def seed(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Seed."""
        return self.busqueda('Seed', sub)

    def cfg_scale(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp CFG_Scale."""
        return self.busqueda('CFG_Scale', sub)

    def steps(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Steps."""
        return self.busqueda('Steps', sub)

    def sampler(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Sampler."""
        return self.busqueda('Sampler', sub)

    def date(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Created_Date."""
        return self.busqueda('Created_Date', sub)
    
    def and_operator(self, list1: list, list2: list) -> list:
        """Retorna una llista amb els UUID que apareixen en AMBDUES llistes."""
        set1 = set(list1)
        set2 = set(list2)
        interseccio = set1.intersection(set2)
        return list(interseccio)
    
    def or_operator(self, list1: list, list2: list) -> list:
        """Retorna una llista amb els UUID que apareixen en QUALSEVOL de les dues llistes, sense duplicats."""
        set1 = set(list1)
        set2 = set(list2)
        unio = set1.union(set2)
        return list(unio)
