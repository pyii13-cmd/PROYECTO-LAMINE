# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""
from typing import List
import cfg

class SearchMetadata:
    def __init__(self, image_data_instance):
        self.data = image_data_instance

    def _uuids(self) -> List[str]:
        try:
            if hasattr(self.data, "_data_storage"):
                return list(self.data._data_storage.keys())
        except Exception:
            pass
        return []

    def _search(self, getter_name: str, sub) -> List[str]:
        res: List[str] = []
        if sub is None:
            return res
        sub_s = str(sub)
        for uuid in self._uuids():
            try:
                getter = getattr(self.data, getter_name, None)
                if not getter:
                    continue
                val = getter(uuid)
                if val is None:
                    continue
                if sub_s in str(val):
                    res.append(uuid)
            except Exception:
                continue
        return res

    def prompt(self, sub: str) -> List[str]:
        return self._search("get_prompt", sub)

    def model(self, sub: str) -> List[str]:
        return self._search("get_model", sub)

    def seed(self, sub: str) -> List[str]:
        return self._search("get_seed", sub)

    def cfg_scale(self, sub: str) -> List[str]:
        return self._search("get_cfg_scale", sub)

    def steps(self, sub: str) -> List[str]:
        return self._search("get_steps", sub)

    def sampler(self, sub: str) -> List[str]:
        return self._search("get_sampler", sub)

    def date(self, sub: str) -> List[str]:
        return self._search("get_created_date", sub)

    # Operadors que preserven ordre: intersecció ordenada per llist1, unió ordenada per aparició
    def and_operator(self, list1: List[str], list2: List[str]) -> List[str]:
        try:
            s2 = set(list2)
            return [u for u in list1 if u in s2]
        except Exception:
            return []

    def or_operator(self, list1: List[str], list2: List[str]) -> List[str]:
        try:
            seen = set()
            res = []
            for u in list1 + list2:
                if u not in seen:
                    seen.add(u)
                    res.append(u)
            return res
        except Exception:
            return []

    def __len__(self) -> int:
        try:
            return len(self.data._data_storage)
        except Exception:
            return 0

    def __str__(self) -> str:
        return f"<SearchMetadata: cercant sobre {len(self)} imatges>"