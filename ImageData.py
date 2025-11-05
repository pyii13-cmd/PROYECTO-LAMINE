# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""

"""
ESTRUCTURA DEL DICCIONARI --> Clau: UUID, Valor --> un segon diccionari amb tota la info de la imatge:
_registre = {
    "UUID-exemple-1": {
        "file": "path/canonic/imatge1.png",
        "prompt": "Un gat en un coet...",
        "seed": "12345",
        "cfg_scale": "7.0",
        # ... altres metadades
    },
    # ... altres imatges
}
"""

import cfg
import os.path
from PIL import Image
# Llista de metadades obligatòries que s'han de considerar.
METADADES_IA = [
    "Prompt", 
    "Seed", 
    "CFG_Scale", 
    "Steps", 
    "Sampler", 
    "Model", 
    "Generated", 
    "Created_Date"
]

# Valor de convenció per a camps no definits
VALOR_NONE = None
VALOR_ERROR = -1

class ImageData:
    """
    Gestiona el registre de dades i metadades de la col·lecció d'imatges,
    indexat per l'identificador únic (UUID).
    """
    
    # Registre intern: Diccionari compartit per totes les instàncies.
    # Clau: UUID (str)
    # Valor: Diccionari amb les dades de la imatge (file, prompt, seed, etc.)
    _dic_registre: dict[str, dict] = {}
    
    
    def __init__(self):
        pass
    
    
    def add_image(self, uuid: str, fitxer: str) -> None:
        """
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialitza les metadades a VALOR_NONE.
        
        Args:
            uuid (str): Identificador únic de la imatge.
            fitxer (str): Path canònic de l'arxiu.
        """
        if uuid in self._dic_registre:
            # Ja està afegida.
            print("UUID Ja afegit!")
            return 
            
        # Creació del diccionari de dades amb valors per defecte.
        entrada = {
            "file": fitxer,
            "width": VALOR_ERROR,
            "height": VALOR_ERROR
        }
        
        # Inicialització de totes les metadades d'IA a "None"
        for clau in METADADES_IA:
            # Utilitzem les mateixes claus que l'arxiu PNG
            entrada[clau] = VALOR_NONE
            
        self._dic_registre[uuid] = entrada # Afegim al diccionari les parelles clau - valor
                                           # tal que la clau es el UUID, i el valor un diccionari amb les metadades.

    
    def remove_image(self, uuid: str) -> None:
        """
        Elimina la imatge i totes les seves metadades de la col·lecció.
        
        Args:
            uuid (str): Identificador únic de la imatge a eliminar.
        """
        if uuid in self._dic_registre:
            del self._dic_registre[uuid]

    
    def load_metadata(self, uuid: str) -> None:
        """
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema al registre.
        
        Args:
            uuid (str): Identificador únic de la imatge a processar.
        """
        if uuid not in self._dic_registre:
            print(f"ERROR: UUID '{uuid}' no trobat al registre. No es poden carregar metadades.")
            return

        entrada = self._dic_registre[uuid]
        path_arxiu_relatiu = entrada["file"] # Aquest és p.ex. "ciutat/img1.png"
        
        # 1. CONSTRUIR EL PATH COMPLET (ABSOLUT)
        #    Necessitem el path base (ROOT_DIR) + el path relatiu
        path_arxiu_complet = os.path.join(cfg.get_root(), path_arxiu_relatiu)

        try:
            # Intentem obrir la imatge amb el PATH COMPLET
            img = Image.open(path_arxiu_complet)
            
            # Llegim les dimensions de la imatge
            entrada["width"] = img.width
            entrada["height"] = img.height

            # Llegim les metadades de la imatge
            metadades_png = img.info # PIL utilitza .info per arxius PNG
            
            # Actualitzem només els camps obligatoris
            for clau_meta in METADADES_IA:
                # Recuperem el valor de les metadades llegides. En cas que no hi hagi, deixem el None.
                valor = metadades_png.get(clau_meta, VALOR_NONE) 
                
                # S'ha d'emmagatzemar com a string
                entrada[clau_meta] = str(valor)

        # CONTROLS D'EXECEPCIONS AMB L'OBERTURA DELS FITXERS O LES LECTURES AMB PILLOW.
        except FileNotFoundError:
            print(f"ERROR: Arxiu '{path_arxiu}' no trobat al disc.")
        except Exception as e:
            print(f"ERROR llegint imatge/metadades de '{path_arxiu}' ({uuid}): {e}")

    #GETTERS
    
    def _obtenir_dada(self, uuid: str, clau: str) -> str | tuple | int | None:
        """Funció auxiliar per obtenir qualsevol dada del registre per UUID i clau."""
        if uuid not in self._dic_registre:
            if clau in ["width", "height"]:
                return VALOR_ERROR
            return VALOR_NONE # <-- Ara retorna l'objecte None
        
        # Retorna la dada emmagatzemada o None si la clau no existeix.
        return self._dic_registre[uuid].get(clau, VALOR_NONE)


    def get_prompt(self, uuid: str) -> str:
        """Retorna el prompt utilitzat per generar la imatge."""
        return self._obtenir_dada(uuid, "Prompt")

    def get_model(self, uuid: str) -> str:
        """Retorna el model d'IA utilitzat."""
        return self._obtenir_dada(uuid, "Model")

    def get_seed(self, uuid: str) -> str:
        """Retorna la llavor aleatòria utilitzada en la generació."""
        return self._obtenir_dada(uuid, "Seed")

    def get_cfg_scale(self, uuid: str) -> str:
        """Retorna el CFG Scale (guidance scale) utilitzat."""
        return self._obtenir_dada(uuid, "CFG_Scale")

    def get_steps(self, uuid: str) -> str:
        """Retorna el nombre de passos d'iteració del model."""
        return self._obtenir_dada(uuid, "Steps")

    def get_sampler(self, uuid: str) -> str:
        """Retorna l'algorisme de mostreig utilitzat."""
        return self._obtenir_dada(uuid, "Sampler")

    def get_generated(self, uuid: str) -> str:
        """Retorna "true" si la imatge està marcada com a generada."""
        return self._obtenir_dada(uuid, "Generated")

    def get_created_date(self, uuid: str) -> str:
        """Retorna la data de creació en format YYYY-MM-DD."""
        return self._obtenir_dada(uuid, "Created_Date")
    
    def get_dimensions(self, uuid: str) -> tuple[int, int]:
        """Retorna una tupla (width, height) amb les dimensions de la imatge."""
        amplada = self._obtenir_dada(uuid, "width")
        altura = self._obtenir_dada(uuid, "height")
        return (amplada, altura)