# -*- coding: utf-8 -*-

from utils import gout, home_path, cpath, containers_path, getfilesize, getjson, jsonwriter
from os import system, environ
from dotenv import load_dotenv
load_dotenv(cpath.joinpath(".env"))
environ["TERM"] = "xterm"


class Container:
    def __init__(self, ident):
        self.id = ident
        self.name = f"pictures_{ident}"
        self.path = containers_path.joinpath(ident)
        self.url = "https://github.com/alanmatzumiya/pictures_a"
        self.content, self.totalsize = {}, 0.0
        self.available_space = bool

    def getinfo(self):
        data, totalsize = {}, 0.0
        folder = self.path.joinpath("photos")
        yrs = list(filter(lambda fn: fn.is_dir(), folder.iterdir()))
        for yr in yrs:
            months = list(filter(lambda fn: fn.is_dir(), yr.iterdir()))
            if months:
                data[yr.name] = {}
                for mth in months:
                    data[yr.name][mth.name] = []
                    files = list(filter(lambda fn: fn.is_file(), mth.iterdir()))
                    for x in files:
                        filepath = f"photos/{yr.name}/{mth.name}/{x.name}"
                        size = getfilesize(x)
                        totalsize += size
                        data[yr.name][mth.name].append(dict(
                            name=x.name,
                            size=size,
                            path=filepath,
                            url=f"{self.url}/blob/main/{filepath}?raw=true"
                        ))
        self.content = data
        self.totalsize = totalsize
        self.available_space = totalsize < 9.5e2
        return dict(
            available_space=self.available_space,
            content=data,
            total_size=totalsize)


class Shell:
    path = current_path

    def runscript(self, path, arg, *args):
        path = self.path.joinpath(str(path))
        self.input(f"bash {str(path)} {arg} {' '.join(args)}")

    @classmethod
    def input(cls, command, **opts):
        if opts.get("getout"):
            return list(filter(
                lambda r: bool(r), gout(command).strip().splitlines()
            ))
        else:
            system(command)

    @staticmethod
    def clear():
        system("clear")

    @staticmethod
    def do_sleep(t, unit="s"):
        system(
            f"sleep {str(t)}{unit if unit in ('s', 'm', 'h', 'd') else 's'}"
        )




