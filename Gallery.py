# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""
from ImageViewer import ImageViewer
import json
import cfg

class Gallery:
    """
    Gestor de la col.leccio d'imatges 
    """
    def __init__(self,  instancia_image_viewer: ImageViewer, name: str = "No_Name", description: str = "", created_date: str = ""):
        self.name = name
        self.description = description
        self.created_date = created_date
        self.images_uuids = []  # llista identificadors  

        self.image_viewer = instancia_image_viewer


#FUNC 5
    def load_file(self, file: str):    #file --> es realment el file path
        """
        Carrega la galeria des de un fitxer JSON
        """
        self.images_uuids = [] #reiniciem la llista  

        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.name = data.get("gallery_name", self.name)
            self.description = data.get("description", self.description)
            self.created_date = data.get("created_date", self.created_date)
            
            #convertim la ruts de cada imatge en un codi unic (uuid)
            for imatge in data.get("images", []):
                imatge_canon = cfg.get_canonical_pathfile(imatge)
                uuid = str(cfg.get_uuid(imatge_canon))  #generem codi unic
                self.images_uuids.append(uuid) #afegim a la llista

            print(f"GALEREIA CARRGADA AMB EXIT:\n  - Nom: {self.name}\n  - Nº Imatges: {len(self.images_uuids)}\n  - Arxiu: {file}")

        except FileNotFoundError:
            print(f"ERROR --> Fitxer no trobat")
        except json.JSONDecodeError:
            print(f"ERROR --> Format JSON invàlid")
        except Exception as e:
            print(f"ERRROR --> Error no identificat: {e}")
    
    
    def show(self):
        """
        visualitza les imatges de la galeria.
        Cal una instancia de ImageVIwer (inicialitzada al init)
        """
        if not self.images_uuids:
            print("La galeria està buida.")
            return 

        for i, uuid in enumerate(self.images_uuids):
            self.image_viewer.show_image(uuid, cfg.DISPLAY_MODE) #cridem a la visualitzacio
            if cfg.DISPLAY_MODE > 0 and i < len(self.images_uuids) - 1: #comprovem si cal fer pausa
                input("Prem [ENTER] per passar d'imatge")


#FUNC 7

    def add_image_at_end(self, uuid: str):
        """
        Afegeix un UUID d'imatge al final de la galeria
        """
        if uuid not in self.images_uuids: #control de duplicats
            self.images_uuids.append(uuid)

    def remove_first_image(self):
        """
        Elimina i retorna el primer UUID de la galeria
        """
        if self.images_uuids:
            removed_uuid = self.images_uuids.pop(0) 
            return removed_uuid
        return None #la llista esta biuda

    def remove_last_image(self):
        """
        Elimina i retorna l'últim UUID de la galeria
        """
        if self.images_uuids:
            removed_uuid = self.images_uuids.pop()
            return removed_uuid
        return None #la llista esta buida
