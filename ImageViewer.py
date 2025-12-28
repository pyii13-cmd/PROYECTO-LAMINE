# -*- coding: utf-8 -*-
"""
ImageViewer.py : Correcció mínima per passar tests Func4
"""
import os
import cfg
from PIL import Image
from typing import Optional

class ImageViewer:
    def __init__(self, data_manager: Optional[object] = None, id_manager: Optional[object] = None):
        self.data_manager = data_manager
        self.id_manager = id_manager

    def print_image(self, uuid: str) -> None:
        # Comprovar si el UUID existeix sense petar
        filep = ""
        if not self.data_manager or not uuid:
            print(f"UUID inexistent o gestor no inicialitzat: {uuid}")
            return
        try:
            filep = self.data_manager._obtenir_dada(uuid, "file")
        except Exception:
            filep = None
        if not filep:
            print(f"UUID inexistent o path invàlid: {uuid}")
            return

        # Obtenir camps amb seguretat
        dims = self.data_manager.get_dimensions(uuid)
        prompt = self.data_manager.get_prompt(uuid)
        model = self.data_manager.get_model(uuid)
        seed = self.data_manager.get_seed(uuid)
        cfg_scale = self.data_manager.get_cfg_scale(uuid)
        steps = self.data_manager.get_steps(uuid)
        sampler = self.data_manager.get_sampler(uuid)
        generated = self.data_manager.get_generated(uuid)
        created = self.data_manager.get_created_date(uuid)

        print("-" * 40)
        print(f"UUID: {uuid}")
        print(f"Arxiu: {filep}")
        print(f"Dimensions: {dims[0]}x{dims[1]}")
        print(f"Model: {model}")
        print(f"Seed: {seed}")
        print(f"CFG Scale: {cfg_scale}")
        print(f"Steps: {steps}")
        print(f"Sampler: {sampler}")
        print(f"Generated: {generated}")
        print(f"Created Date: {created}")
        if prompt and prompt != "None":
            print("Prompt:", (prompt if len(prompt) <= 200 else (prompt[:200] + "...")))
        else:
            print("Prompt: None")
        print("-" * 40)

    def show_file(self, file: str) -> bool:
        if not file or not isinstance(file, str):
            return False
        try:
            root = cfg.get_root()
        except Exception:
            root = ""
        abs_path = file if os.path.isabs(file) else os.path.join(root, file) if root else file
        if not os.path.isfile(abs_path):
            return False
        try:
            img = Image.open(abs_path)
            try:
                img.show()
            finally:
                img.close()
            return True
        except Exception:
            return False

    def show_image(self, uuid: str, mode: int = -1) -> None:
        if mode == -1:
            try:
                mode = int(cfg.DISPLAY_MODE)
            except Exception:
                mode = 0

        path_rel = ""
        if self.data_manager and uuid:
            try:
                path_rel = self.data_manager._obtenir_dada(uuid, "file") or ""
            except Exception:
                path_rel = ""

        if mode == 0:
            self.print_image(uuid)
        elif mode == 1:
            if path_rel:
                self.print_image(uuid)
                ok = self.show_file(path_rel)
                if ok:
                    try:
                        input("... Imatge mostrada. Premeu Enter per continuar ...")
                    except Exception:
                        pass
            else:
                # UUID inexistent, imprimir advertència mínima
                print(f"UUID inexistent o path invàlid: {uuid}")
        elif mode == 2:
            if path_rel:
                ok = self.show_file(path_rel)
                if ok:
                    try:
                        input("... Imatge mostrada. Premeu Enter per continuar ...")
                    except Exception:
                        pass
            else:
                print(f"UUID inexistent o path invàlid: {uuid}")
        else:
            self.print_image(uuid)

    def __len__(self) -> int:
        if self.data_manager and hasattr(self.data_manager, "_data_storage"):
            return len(self.data_manager._data_storage)
        return 0

    def __str__(self) -> str:
        return f"<ImageViewer: {len(self)} imatges registrades>"
