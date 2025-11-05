# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""
import cfg
import os
import os.path

class ImageFiles:
    def __init__(self):
        self._arxius_anteriors = set()
        self._arxius_actuals = set()
    def reload_fs(self,path: str):
        self._arxius_anteriors = self._arxius_actuals.copy()
        nous_arxius = set()
        for dir, sdir, arxius in os.walk(path):
            for nom_arxiu in arxius:
                if nom_arxiu.lower().endswith('.png'):
                    path_complet = os.path.join(dir,nom_arxiu)
                    path_relatiu = cfg.get_canonical_pathfile(path_complet) # construye el path desde donde tu estas hasta el archivo que tu quieres 
                    nous_arxius.add(path_relatiu)
        self._arxius_actuals = nous_arxius

    def files_added(self):
        afegides = self._arxius_actuals - self._arxius_anteriors
        return list(afegides)
    
    def files_removed(self):
        eliminades = self._arxius_anteriors - self._arxius_actuals
        return list(eliminades)
    
    def __len__(self) -> int:
        """
        Retorna el nombre d'arxius PNG gestionats actualment.
        """
        # Simplement retornem la mida del nostre conjunt d'arxius actuals
        return len(self._arxius_actuals)

    def __str__(self) -> str:
        """
        Retorna una representació en text de l'objecte.
        """
        # Podem reutilitzar el nostre propi __len__!
        quantitat = len(self)
        return f"<ImageFiles: gestionant {quantitat} arxius PNG>"