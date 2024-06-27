# Writing by Atlas
# common.py

from package.common.logger import Logger
import random
from datetime import datetime

class Common:
    @staticmethod
    def calcul_next_port(key: int, allowed_ports:list, is_time_based:bool = True) -> int:
        if is_time_based:
            len_list = len(allowed_ports)
            date = datetime.utcnow()
            my_sec = date.second
            # micro = int(micro // 1000)
            my_sec -= my_sec % 5
                
            alea = date.year + date.month + date.weekday() + date.day + date.hour + date.minute + my_sec + 1
            alea = alea * len_list
            random.seed(alea)
            seed = int(random.random()*65539)
            random.seed()
            new_port: int = int(allowed_ports[seed%len_list])
            Logger().debug(f"alea : {alea}, new_port : {new_port}")

            return new_port
        else:
            inc = key + 1
            len_list = len(allowed_ports)
            new_port: int = int(allowed_ports[inc%len_list])
            Logger().debug(f"Calcul_next_port = {new_port}")
            return new_port


    @staticmethod
    def getperm(l, seed:int):
        seed = sum(sum(a) for a in l) * seed
        random.seed(seed)
        perm = list(range(len(l)))
        random.shuffle(perm)
        random.seed()
        return perm

    @staticmethod
    def shuffle(l, seed:int):
        perm = Common.getperm(l, seed=seed)
        l[:] = [l[j] for j in perm]

    @staticmethod
    def unshuffle(l, seed:int):
        perm = Common.getperm(l, seed=seed)
        res = [None] * len(l)
        for i, j in enumerate(perm):
            res[j] = l[i]
        l[:] = res