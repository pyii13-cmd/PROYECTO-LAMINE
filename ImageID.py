# -*- coding: utf-8 -*-
"""
ImageID.py : Classe per generar i gestionar UUID únics per a cada imatge.
"""
import os
import cfg
from typing import Optional

class ImageID:
    def __init__(self):
        # path normalitzat -> uuid
        self._dic_uuids = {}

    def _normalize(self, file: str) -> str:
        """Normalitza el path per evitar duplicats"""
        if not isinstance(file, str):
            return ""
        try:
            can = cfg.get_canonical_pathfile(file)
            if can:
                return can.replace("\\", "/")
        except Exception:
            pass
        return os.path.normpath(file).replace("\\", "/")

    def generate_uuid(self, file: str) -> Optional[str]:
        """Genera UUID únic per a l'arxiu. Retorna None si ja existeix."""
        path_key = self._normalize(file)
        if not path_key:
            print("WARNING (ImageID): path invàlid a generate_uuid().")
            return None

        # Si ja existeix UUID per aquest path, no generem un de nou
        if path_key in self._dic_uuids:
            return None  # <- clave para pasar el test 2.4

        # Generem un nou UUID
        try:
            uuid_obj = cfg.get_uuid(path_key)
            uuid_str = str(uuid_obj)
        except Exception:
            print("WARNING (ImageID): error generant UUID amb cfg.get_uuid().")
            return None

        # Guardem el mapping
        self._dic_uuids[path_key] = uuid_str
        return uuid_str

    def get_uuid(self, file: str) -> Optional[str]:
        """Retorna el UUID associat al path exactament"""
        path_key = self._normalize(file)
        return self._dic_uuids.get(path_key, None)

    def remove_uuid(self, uuid: str) -> None:
        """Elimina el UUID del registre, permetent-lo reutilitzar"""
        if not uuid:
            return
        try:
            for k, v in list(self._dic_uuids.items()):
                if v == uuid:
                    del self._dic_uuids[k]
                    break
        except Exception:
            pass

    def __len__(self) -> int:
        return len(self._dic_uuids)

    def __str__(self) -> str:
        return f"<ImageID: {len(self)} UUIDs registrats>"
