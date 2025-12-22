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
import os
import cfg
from typing import Optional

class ImageID:
    def __init__(self):
        # map: path_canonic -> uuid_str
        self._dic_uuids = {}

    def _normalize(self, file: str) -> str:
        """Normalitza el path per buscar coincidències"""
        try:
            if not isinstance(file, str):
                return ""
            # Intentem obtenir el canonical relatiu si cfg pot
            try:
                can = cfg.get_canonical_pathfile(file)
                if can:
                    return can.replace("\\", "/")
            except Exception:
                pass
            # fallback: normpath i replace separadors
            p = os.path.normpath(file)
            return p.replace("\\", "/")
        except Exception:
            return file.replace("\\", "/") if isinstance(file, str) else ""

    def generate_uuid(self, file: str) -> Optional[str]:
        if not file or not isinstance(file, str):
            print("WARNING (ImageID): fitxer invàlid a generate_uuid().")
            return None
        path_key = self._normalize(file)
        if not path_key:
            print("WARNING (ImageID): path canònic buit.")
            return None

        # Si ja existeix per aquest path, retornem el mateix UUID (no crear-ne un de nou)
        if path_key in self._dic_uuids:
            return self._dic_uuids[path_key]

        # Generem l'UUID amb cfg.get_uuid (pot llençar excepció)
        try:
            uuid_obj = cfg.get_uuid(path_key)
            uuid_str = str(uuid_obj)
        except Exception:
            print("WARNING (ImageID): error generant UUID amb cfg.get_uuid().")
            return None

        # Si l'UUID ja està assignat a un altre path, denunciem col·lisió
        if uuid_str in self._dic_uuids.values():
            print(f"WARNING (ImageID): col·lisió d'UUID detectada ({uuid_str}). Fitxer ignorat.")
            return None

        self._dic_uuids[path_key] = uuid_str
        return uuid_str

    def get_uuid(self, file: str) -> Optional[str]:
        if not file or not isinstance(file, str):
            return None
        path_key = self._normalize(file)
        if path_key in self._dic_uuids:
            return self._dic_uuids[path_key]
        # Intentem matches parcials: buscar si qualsevol key acaba o conté el path proporcionat
        try:
            for k, v in self._dic_uuids.items():
                if k == file or k.endswith(file) or file.endswith(k):
                    return v
        except Exception:
            pass
        return None

    def remove_uuid(self, uuid: str) -> None:
        if not uuid:
            return
        try:
            to_del = None
            for k, v in list(self._dic_uuids.items()):
                if v == uuid:
                    to_del = k
                    break
            if to_del:
                del self._dic_uuids[to_del]
        except Exception:
            pass

    def __len__(self) -> int:
        try:
            return len(self._dic_uuids)
        except Exception:
            return 0

    def __str__(self) -> str:
        return f"<ImageID: {len(self)} UUIDs registrats>"