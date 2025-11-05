# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""

import cfg

class ImageID:
    """
    Gestiona la generació i el registre d'identificadors únics (UUID)
    per a imatges, assegurant que no hi hagi col·lisions.
    """
    
    # Registre intern: Diccionari compartit per totes les instàncies de la classe.
    # Clau: path canònic del fitxer (str)
    # Valor: UUID generat (str)
    _dic_uuids: dict[str, str] = {}
    
    def __init__(self):
        pass

    
    def generate_uuid(self, fitxer: str) -> str | None:
        """
        Genera i registra un UUID únic per a l'arxiu especificat.
        
        Args:
            fitxer (str): El path canònic de l'arxiu.
            
        Returns:
            str | None: El UUID generat com a string, o None si hi ha col·lisió.
        """
        # 1. Comprova si ja existeix el path a les claus del diccionari.
        if fitxer in self._dic_uuids:
            return self._dic_uuids[fitxer]
        
        # 2. Genera l'UUID utilitzant la funció del cfg.
        uuid_obj_nou = cfg.get_uuid(fitxer)
        uuid_str_nou = str(uuid_obj_nou)

        # 3. Comprovació de col·lisions: mirem si el nou UUID generat ja existeix
        #    com a VALOR assignat a una altra RUTA.
        if uuid_str_nou in self._dic_uuids.values():
            print(f"Col·lisió detectada! L'UUID '{uuid_str_nou}' ja està en ús.")
            print(f"L'arxiu '{fitxer}' no es pot afegir.")
            return None
        
        # 4. Si és únic, l'afegim utilitzant el path canònic com a clau.
        self._dic_uuids[fitxer] = uuid_str_nou
        return uuid_str_nou

    
    def get_uuid(self, fitxer: str) -> str | None:
        """
        Retorna el UUID associat a l'arxiu, si ja ha estat generat i és actiu.
        
        Args:
            fitxer (str): El path canònic de l'arxiu.
            
        Returns:
            str | None: El UUID com a string, o None si el fitxer no s'ha registrat.
        """
        # Retorna el valor associat al path o None si el path no és al diccionari.
        return self._dic_uuids.get(fitxer, None)

    
    def remove_uuid(self, uuid_str: str) -> None:
        """
        Elimina el registre d'un UUID del sistema. L'UUID queda lliure.
        
        Args:
            uuid_str (str): El UUID a eliminar com a string.
        """
        # Cerquem el path corresponent a l'UUID
        path_a_eliminar = None
        for path_canonic, uuid_registrat in self._dic_uuids.items():
            if uuid_registrat == uuid_str:
                path_a_eliminar = path_canonic
                break
        
        # Eliminem l'element del diccionari si existeix el path.
        if path_a_eliminar:
            del self._dic_uuids[path_a_eliminar]

    def __len__(self) -> int:
        """ Retorna el nombre total d'imatges registrades. """
        return len(self._dic_uuids)

    def __str__(self) -> str:
        """ Retorna una representació en text de l'objecte. """
        return f"<ImageData: gestionant {len(self)} imatges>"

    