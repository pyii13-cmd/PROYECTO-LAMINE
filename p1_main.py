# -*- coding: utf-8 -*-
"""
p1_main.py : Script de proves per a Func 1, 2 i 3
"""

import cfg  # Necessari per obtenir el ROOT_DIR
import time

# Importem TOTES les classes que necessitem
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData

print("--- Iniciant Prova d'Integració (Func 1, 2, 3) ---")

# 1. Creem les instàncies de les classes
#    (Com que són registres de classe, les podem crear així)
gestor_arxius = ImageFiles()
gestor_id = ImageID()
gestor_dades = ImageData()

print("Objectes creats.")
print(f"Buscant arxius a: {cfg.get_root()}...")

# -----------------------------------------------------------------
# PAS 1: Simulem la càrrega inicial del programa
# -----------------------------------------------------------------
# Func 1: Escaneja el disc
gestor_arxius.reload_fs(cfg.get_root())

# Obtenim la llista d'arxius que s'han d'afegir
arxius_per_afegir = gestor_arxius.files_added()
print(f"Trobats {len(arxius_per_afegir)} arxius PNG al disc.")

# Variables per comptar
comptador_exit = 0
comptador_error_id = 0
llista_uuids = []

# Bucle principal: Processem cada arxiu trobat
for path_relatiu in arxius_per_afegir:
    
    # Func 2: Generem el seu UUID
    uuid_nou = gestor_id.generate_uuid(path_relatiu)
    
    if uuid_nou is None:
        # Error! Col·lisió d'UUID o un altre problema
        print(f"ERROR: No s'ha pogut generar UUID per a {path_relatiu}")
        comptador_error_id += 1
        continue

    # Func 3: Afegim la imatge al registre de dades
    gestor_dades.add_image(uuid_nou, path_relatiu)
    
    # Func 3: Carreguem les seves metadades des del disc
    gestor_dades.load_metadata(uuid_nou)
    
    comptador_exit += 1
    llista_uuids.append(uuid_nou)

print(f"\nProcés de càrrega completat.")
print(f"  Imatges processades amb èxit: {comptador_exit}")
print(f"  Errors de generació d'UUID: {comptador_error_id}")

# -----------------------------------------------------------------
# PAS 2: Comprovem els mètodes __len__ i __str__
# -----------------------------------------------------------------
print("\n" + "="*40)
print("[PROVA 2: Comprovació de __len__ i __str__]")

print(f"  ImageFiles:   {gestor_arxius}")
print(f"  ImageID:      {gestor_id}")
print(f"  ImageData:    {gestor_dades}")

# Comprovem que les mides coincideixin
if len(gestor_arxius) == len(gestor_id) == len(gestor_dades):
    print("\n  >> ÈXIT! Els 'len()' de les tres classes coincideixen.")
else:
    print(f"\n  >> ERROR! Els 'len()' no coincideixen:")
    print(f"     len(Files) = {len(gestor_arxius)}")
    print(f"     len(ID)    = {len(gestor_id)}")
    print(f"     len(Data)  = {len(gestor_dades)}")

# -----------------------------------------------------------------
# PAS 3: Comprovem els 'getters' de ImageData
# -----------------------------------------------------------------
print("\n" + "="*40)
print("[PROVA 3: Comprovació dels 'getters' d'ImageData]")

# Agafem el primer UUID de la llista per provar
if llista_uuids:
    uuid_test = llista_uuids[0]
    print(f"Provant 'getters' amb un UUID de mostra: {uuid_test}")
    
    # Obtenim totes les dades d'aquesta imatge
    prompt = gestor_dades.get_prompt(uuid_test)
    model = gestor_dades.get_model(uuid_test)
    seed = gestor_dades.get_seed(uuid_test)
    dims = gestor_dades.get_dimensions(uuid_test)
    
    print(f"  Dimensions (W, H): {dims}")
    print(f"  Model:             {model}")
    print(f"  Seed:              {seed}")
    
    # Comprovem si el prompt és un string o és None
    if isinstance(prompt, str):
        print(f"  Prompt (curt):     {prompt[:50]}...")
    elif prompt is None:
        print("  Prompt:            None (Correcte, no hi ha prompt)")
    else:
        print(f"  Prompt:            ERROR! Tipus de dada incorrecte: {type(prompt)}")

    # Comprovació clau del VPL
    if model == "None" or seed == "None":
        print("\n  >> ALERTA VPL! El getter ha retornat el text \"None\" en lloc de l'objecte None.")
        print("     Assegureu-vos que VALOR_NONE = None a ImageData.py")
    elif model is None or seed is None:
         print("\n  >> CORRECTE! El getter ha retornat l'objecte None per a camps buits.")
        
else:
    print("No s'han trobat UUIDs, no es poden provar els 'getters'.")


print("\n--- Fi de la Prova d'Integració ---")