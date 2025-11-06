# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""
import cfg
import os.path
from PIL import Image

try:
    from ImageData import ImageData
except ImportError:
    print("ERROR: NO ÉS POT IMPORTAR LA CLASSE (ImageData)")
class ImageViewer:
    def __init__(self):
        pass
    def print_image(uuid:str):
        dades = ImageData()
        dims = dades.get_dimensions(uuid)
        prompt = dades.get_prompt(uuid)
        model = dades.get_model(uuid)
        seed = dades.get_seed(uuid)
        cfg_scale = dades.get_cfg_scale(uuid)
        steps = dades.get_steps(uuid)
        sampler = dades.get_sampler(uuid)
        generated = dades.get_generated(uuid)
        created_date = dades.get_created_date(uuid)

        path_relatiu = dades._obtenir_dada(uuid,"file")
        print("-"*30)
        print("\n")
        print(f"Metadades de la imatge: {uuid}")
        print(f"Dimensions: {dims}")
        print(f"Prompt {prompt}")
        print(f"Model: {model}")
        print(f"Seed: {seed}")
        print(f"CFG SCALE {cfg_scale}")
        print(f"Steps: {steps}")
        print(f"Sampler: {sampler}")
        print(f"Generated: {generated}")
        print(f"Created date: {created_date}")
        print(f"Arxiu: {path_relatiu}")

        if prompt:
            prompt_curt = (prompt[:100] + "...") if len(prompt) > 100 else prompt
            print(f"  Prompt:     {prompt_curt}")
        else:
            print(f"  Prompt:     {None}")
            
        print("-" * 30 + "\n")

    def show_file(self, file: str):
        if not file:
            print("ERROR (show_file): El path del fitxer és buit.")
            return False
        try:
            path_complet = os.path.join(cfg.get_root,file) 
            img = Image.open(path_complet)
            img.show()
            return True
        except FileNotFoundError:
            print(f"ERROR (show_file): Arxiu no trobat a '{path_complet}'")
            return False
        except Exception as e:
            print(f"ERROR (show_file): No es pot mostrar la imatge '{file}'. {e}")
            return False
    def show_image(self, uuid: str, mode: int = -1):
        if mode == -1:
            mode = cfg.DISPLAY_MODE
        
    # Obtenim el path relatiu
        dades = ImageData()
        path_relatiu = dades._obtenir_dada(uuid, "file")
        
        if not path_relatiu:
            print(f"ERROR (show_image): No s'ha trobat cap arxiu per a l'UUID '{uuid}'")
            return

        # Gestionem els modes
        imatge_mostrada = False
        
        if mode == 0:  # Només metadades
            self.print_image(uuid)
            
        elif mode == 1:  # Metadades + Imatge
            self.print_image(uuid)
            imatge_mostrada = self.show_file(path_relatiu)
            
        elif mode == 2:  # Només imatge
            imatge_mostrada = self.show_file(path_relatiu)
            
        else:
            print(f"ERROR (show_image): Mode '{mode}' desconegut.")
            return

        # Fem la pausa síncrona si s'ha mostrat una imatge
        if imatge_mostrada:
            print("Imatge mostrada en una finestra separada.")
            input("... prem Enter per continuar ...")
    
    # --- MÈTODES OBLIGATORIS PER AL VPL ---
    
    def __len__(self) -> int:
        """ Retorna 0, ja que el viewer no emmagatzema elements. """
        return 0

    def __str__(self) -> str:
        """ Retorna una representació en text de l'objecte. """
        return "<ImageViewer: Eina de visualització d'imatges i metadades>"