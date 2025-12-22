# -*- coding: utf-8 -*-
"""
ImageFiles.py
"""
import os
import cfg


class ImageFiles:
    def __init__(self):
        self._arxius_anteriors = set()
        self._arxius_actuals = set()

    def reload_fs(self, path: str = None) -> None:
        # Estado anterior
        self._arxius_anteriors = self._arxius_actuals.copy()
        self._arxius_actuals = set()

        # Path por defecto
        if not isinstance(path, str) or not path:
            path = cfg.get_root()

        try:
            path = os.path.normpath(path)
        except Exception:
            return

        if not os.path.isdir(path):
            return

        try:
            for base, _, files in os.walk(path):
                for fname in files:
                    if not fname.lower().endswith(".png"):
                        continue

                    full = os.path.abspath(os.path.join(base, fname))
                    self._arxius_actuals.add(full)
        except Exception:
            return

    def files_added(self):
        return sorted(self._arxius_actuals - self._arxius_anteriors)

    def files_removed(self):
        return sorted(self._arxius_anteriors - self._arxius_actuals)
