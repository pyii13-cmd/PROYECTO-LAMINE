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

import os
import cfg
from PIL import Image
from typing import Dict, Tuple, Any

# Funció d'ajuda per normalitzar claus de metadades a les esperades
def _canonical_key(k: str) -> str:
    if not isinstance(k, str):
        return k
    kk = k.strip().lower().replace("-", "_").replace(" ", "_")
    # Mapatge explícit de variants
    if kk in ("prompt", "text", "description"):
        return "Prompt"
    if kk in ("seed",):
        return "Seed"
    if kk in ("cfg_scale", "cfg scale", "cfgscale", "cfg-scale"):
        return "CFG_Scale"
    if kk in ("steps", "num_steps"):
        return "Steps"
    if kk in ("sampler",):
        return "Sampler"
    if kk in ("model",):
        return "Model"
    if kk in ("generated",):
        return "Generated"
    if kk in ("created_date", "created-date", "created date", "createddate", "date"):
        return "Created_Date"
    # fallback: capitalitza la clau original
    return k

class ImageData:
    def __init__(self):
        # uuid -> { file_path: str, metadata: dict, dimensions: (w,h) }
        self._data_storage: Dict[str, Dict[str, Any]] = {}

    def add_image(self, uuid: str, file: str) -> None:
        if not uuid or not isinstance(uuid, str):
            print("WARNING (ImageData): UUID invàlid a add_image().")
            return
        if not file or not isinstance(file, str):
            print("WARNING (ImageData): file invàlid a add_image().")
            return
        # Inicialitzar tots els camps obligats amb "None" per coherència
        self._data_storage[uuid] = {
            "file_path": file.replace("\\", "/"),
            "metadata": {
                "Prompt": "None",
                "Seed": "None",
                "CFG_Scale": "None",
                "Steps": "None",
                "Sampler": "None",
                "Model": "None",
                "Generated": "None",
                "Created_Date": "None"
            },
            "dimensions": (0, 0)
        }

    def remove_image(self, uuid: str) -> None:
        if not uuid:
            return
        self._data_storage.pop(uuid, None)

    def load_metadata(self, uuid: str) -> None:
        """
        Llegeix metadades embegudes en el PNG i normalitza les claus.
        Si no hi ha metadades reals, imprimeix l'avís exacte:
            WARNING with empty metadata elements
        i deixa els camps amb "None".
        """
        if not uuid or uuid not in self._data_storage:
            # advertència suau, però no llença excepció
            # (el test vol que no peti)
            return

        rec = self._data_storage[uuid]
        rel = rec.get("file_path", "")
        # Construïm path absolut
        try:
            root = cfg.get_root()
            abs_path = os.path.join(root, rel) if not os.path.isabs(rel) else rel
        except Exception:
            abs_path = rel

        # Si l'arxiu no existeix, no hi ha metadades reals
        if not os.path.isfile(abs_path):
            # deixem els valors per defecte (ja inicialitzats), però alertem
            print("WARNING with empty metadata elements")
            rec["dimensions"] = (0, 0)
            # Assegurem que hi hagi el dict metadata amb les claus esperades
            if "metadata" not in rec or not isinstance(rec["metadata"], dict):
                rec["metadata"] = {
                    "Prompt": "None",
                    "Seed": "None",
                    "CFG_Scale": "None",
                    "Steps": "None",
                    "Sampler": "None",
                    "Model": "None",
                    "Generated": "None",
                    "Created_Date": "None"
                }
            return

        # Llegim la imatge amb PIL i extraiem text chunks (img.info o img.text)
        try:
            with Image.open(abs_path) as img:
                raw = getattr(img, "text", None)
                if raw is None:
                    # alguns PIL utilitzen img.info per a text
                    raw = img.info if isinstance(img.info, dict) else None

                # dimensions
                w = getattr(img, "width", None)
                h = getattr(img, "height", None)
                try:
                    rec["dimensions"] = (int(w) if w else 0, int(h) if h else 0)
                except Exception:
                    rec["dimensions"] = (0, 0)

                norm: Dict[str, str] = {}
                if raw and isinstance(raw, dict):
                    for k, v in raw.items():
                        try:
                            key = _canonical_key(str(k))
                            if isinstance(v, bytes):
                                try:
                                    sval = v.decode("utf-8", errors="ignore")
                                except Exception:
                                    sval = str(v)
                            else:
                                sval = str(v)
                            norm[key] = sval
                        except Exception:
                            continue
                elif raw:
                    # hi ha alguna cosa però no és dict -> la convertim a prompt
                    try:
                        sval = str(raw)
                        norm["Prompt"] = sval
                    except Exception:
                        pass

                # Si no hem obtingut cap metadada real, avisem i deixem valors per defecte
                if not norm:
                    print("WARNING with empty metadata elements")
                    # mantenim la metadata prèvia (defecte "None")
                    if "metadata" not in rec or not isinstance(rec["metadata"], dict):
                        rec["metadata"] = {
                            "Prompt": "None",
                            "Seed": "None",
                            "CFG_Scale": "None",
                            "Steps": "None",
                            "Sampler": "None",
                            "Model": "None",
                            "Generated": "None",
                            "Created_Date": "None"
                        }
                    return

                # inserim valors llegits, assegurant que totes les claus obligatòries existeixin
                # inicialitzem amb "None" i sobreescrivim amb valors reals
                meta_safe = {
                    "Prompt": "None",
                    "Seed": "None",
                    "CFG_Scale": "None",
                    "Steps": "None",
                    "Sampler": "None",
                    "Model": "None",
                    "Generated": "None",
                    "Created_Date": "None"
                }
                for k, v in norm.items():
                    if not isinstance(k, str):
                        continue
                    meta_safe[k] = str(v) if v is not None else "None"
                rec["metadata"] = meta_safe
        except Exception:
            # Qualsevol error llegint la imatge -> deixem valors segurs
            print("WARNING with empty metadata elements")
            rec["metadata"] = {
                "Prompt": "None",
                "Seed": "None",
                "CFG_Scale": "None",
                "Steps": "None",
                "Sampler": "None",
                "Model": "None",
                "Generated": "None",
                "Created_Date": "None"
            }
            rec["dimensions"] = (0, 0)

    # --- Getters (sempre string) ---
    def _get_field(self, uuid: str, key: str) -> str:
        if not uuid or uuid not in self._data_storage:
            return "None"
        try:
            val = self._data_storage[uuid].get("metadata", {}).get(key, "None")
            return "None" if val is None else str(val)
        except Exception:
            return "None"

    def get_prompt(self, uuid: str) -> str:
        return self._get_field(uuid, "Prompt")

    def get_model(self, uuid: str) -> str:
        return self._get_field(uuid, "Model")

    def get_seed(self, uuid: str) -> str:
        return self._get_field(uuid, "Seed")

    def get_cfg_scale(self, uuid: str) -> str:
        return self._get_field(uuid, "CFG_Scale")

    def get_steps(self, uuid: str) -> str:
        return self._get_field(uuid, "Steps")

    def get_sampler(self, uuid: str) -> str:
        return self._get_field(uuid, "Sampler")

    def get_generated(self, uuid: str) -> str:
        return self._get_field(uuid, "Generated")

    def get_created_date(self, uuid: str) -> str:
        return self._get_field(uuid, "Created_Date")

    def get_dimensions(self, uuid: str) -> Tuple[int, int]:
        if not uuid or uuid not in self._data_storage:
            return (0, 0)
        try:
            dims = self._data_storage[uuid].get("dimensions", (0, 0))
            if not isinstance(dims, tuple) or len(dims) != 2:
                return (0, 0)
            return (int(dims[0] or 0), int(dims[1] or 0))
        except Exception:
            return (0, 0)

    def _obtenir_dada(self, uuid: str, clau: str):
        if not uuid or uuid not in self._data_storage:
            return ""
        if clau == "file":
            return self._data_storage[uuid].get("file_path", "")
        return self._data_storage[uuid].get(clau)

    def __len__(self) -> int:
        try:
            return len(self._data_storage)
        except Exception:
            return 0

    def __str__(self) -> str:
        return f"<ImageData: {len(self)} imatges registrades>"