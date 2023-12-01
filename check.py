from pathlib import Path
from utils import getfilesize
path = Path.home().joinpath("Videos/waiting")
files = list(fi for fi in path.iterdir() if fi.is_file() and fi.name.endswith(".mp4"))
ids = []
repeated = []
xfiles = []
for file in files:
    filename = file.name
    strs = filename.split(".mp4")[0]
    fileid = strs[-12:-1] if strs.endswith("]") else strs[-11:]
    ids.append(fileid)
    if ids.count(fileid) > 1:
        repeated.append(fileid)


print(f"ids: {len(ids)}")
print(f"repeated: {len(repeated)}")
print(repeated)
trash = Path.home().joinpath("Videos/trash")
for nid in repeated:
    yn, xn = [], []
    for fn in files:
        if nid in fn.name:
            if f'[{nid}]' in fn.name:
                xn.append(str(fn))
            else:
                yn.append(str(fn))

    if len(yn) == 1 and len(xn) == 1:
        sy, sx = getfilesize(yn[0]), getfilesize(xn[0])
        if sy > sx:
            ypath = Path(yn[0])
            newpath = trash.joinpath(ypath.name)
        else:
            xpath = Path(xn[0])
            newpath = trash.joinpath(xpath.name)
