# -*- coding: utf-8 -*-
"""
ImageData.py
"""

import os
import cfg
from PIL import Image
from typing import Dict, Any


def _canonical_key(k: str) -> str:
    kk = k.strip().lower().replace("-", "_").replace(" ", "_")
    if kk in ("prompt", "text", "description"):
        return "Prompt"
    if kk == "seed":
        return "Seed"
    if kk in ("cfg_scale", "cfgscale"):
        return "CFG_Scale"
    if kk == "steps":
        return "Steps"
    if kk == "sampler":
        return "Sampler"
    if kk == "model":
        return "Model"
    if kk == "generated":
        return "Generated"
    if kk in ("created_date", "createddate", "date"):
        return "Created_Date"
    return k


class ImageData:
    def __init__(self):
        self._data_storage: Dict[str, Dict[str, Any]] = {}

    # ===============================
    # ADD IMAGE
    # ===============================
    def add_image(self, uuid: str, file: str) -> None:
        if not isinstance(uuid, str) or not uuid:
            return
        if not isinstance(file, str) or not file:
            return

        # no duplicados
        if uuid in self._data_storage:
            return

        # SOLO validamos extensión
        if not file.lower().endswith(".png"):
            return

        # 👉 NO comprobamos si existe el archivo (CLAVE)
        self._data_storage[uuid] = {
            "file_path": file,
            "metadata": None,
            "dimensions": None
        }

    # ===============================
    # REMOVE IMAGE
    # ===============================
    def remove_image(self, uuid: str) -> None:
        if uuid in self._data_storage:
            del self._data_storage[uuid]

    # ===============================
    # LOAD METADATA
    # ===============================
    def load_metadata(self, uuid: str) -> None:
        if uuid not in self._data_storage:
            return

        rec = self._data_storage[uuid]
        rel_path = rec["file_path"]

        root = cfg.get_root()
        abs_path = rel_path if os.path.isabs(rel_path) else os.path.join(root, rel_path)

        # 👉 SI EL ARCHIVO NO EXISTE, Image.open LANZA OSError (LO QUE QUIERE EL TEST)
        img = Image.open(abs_path)

        rec["dimensions"] = (img.width, img.height)

        raw = img.text if hasattr(img, "text") else img.info
        if not raw:
            print("WARNING with empty metadata elements")
            rec["metadata"] = None
            return

        metadata = {}
        for k, v in raw.items():
            key = _canonical_key(str(k))
            metadata[key] = str(v)

        if not metadata:
            print("WARNING with empty metadata elements")
            rec["metadata"] = None
        else:
            rec["metadata"] = metadata

    # ===============================
    # GETTERS
    # ===============================
    def _get_field(self, uuid: str, key: str):
        if uuid not in self._data_storage:
            return None
        meta = self._data_storage[uuid].get("metadata")
        if meta is None:
            return None
        return meta.get(key)

    def get_prompt(self, uuid: str):
        return self._get_field(uuid, "Prompt")

    def get_model(self, uuid: str):
        return self._get_field(uuid, "Model")

    def get_seed(self, uuid: str):
        return self._get_field(uuid, "Seed")

    def get_cfg_scale(self, uuid: str):
        return self._get_field(uuid, "CFG_Scale")

    def get_steps(self, uuid: str):
        return self._get_field(uuid, "Steps")

    def get_sampler(self, uuid: str):
        return self._get_field(uuid, "Sampler")

    def get_generated(self, uuid: str):
        return self._get_field(uuid, "Generated")

    def get_created_date(self, uuid: str):
        return self._get_field(uuid, "Created_Date")

    def get_dimensions(self, uuid: str):
        if uuid not in self._data_storage:
            return None
        return self._data_storage[uuid].get("dimensions")

    def get_filename(self, uuid: str):
        if uuid not in self._data_storage:
            return None
        return self._data_storage[uuid].get("file_path")

    def __len__(self) -> int:
        return len(self._data_storage)

    def __str__(self) -> str:
        return f"<ImageData: {len(self)} images>"
