# -*- coding: utf-8 -*-

from subprocess import getoutput as gout
from os.path import getctime
from time import ctime
from pathlib import Path
from json import load, dumps
jsonconf = dict(
    indent=4,
    sort_keys=True,
    ensure_ascii=False
)
containers_path = Path.home().joinpath("Pictures/containers")
current_path = Path(__file__).parent


def getjson(filepath):
    return load(Path(str(filepath)).open())


def jsonwriter(datajson, filepath):
    Path(str(
        filepath
    )).open("w").write(dumps(
        datajson, **jsonconf
    ))


def getfilesize(xpath):
    return Path(str(
        xpath
    )).stat().st_size * 1.0e-6


def getdate(filepath=None):
    dtime = list(
        s for s in (
            ctime(getctime(Path(str(filepath)))).split()
            if filepath else ctime().split()
        ) if s
    )
    t = dtime[3].split(":")
    return "{day}-{month}-{year}, {hours}:{minutes}:{seconds}".format(
        day=dtime[2], month=dtime[1], year=dtime[4],
        **{
            s: f"0{t[i]}" if len(t[i]) == 1 else t[i]
            for i, s in enumerate(["hours", "minutes", "seconds"])
        }
    )
