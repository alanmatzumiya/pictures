

"""""

if __name__ != "__main__":
    CLI = CLI()


class Container:

    def __init__(self, dpath):
        self.path = Path(dpath)
        self.name = self.path.name

    def gitdata(self, path="/", datatype=""):
        content = []

        def git(arg):
            return CLI.input(f"cd {self.path} && git {arg}", getout=True)

        br = git("branch")[0].replace("* ", "")
        dataurl = git("config --get remote.origin.url")[0].replace(".git", f"/blob/{br}/{path}")
        links = BeautifulSoup(get(dataurl).text, "html.parser").find("body").findAll("a")
        for link in links:
            href = link.get("href")
            if datatype:
                if href.endswith(f".{datatype}"):
                    content.append(dict(
                        filename=link.get("title"),
                        url=f"{dataurl}{href}?raw=true"
                    ))
            else:
                content.append(dict(
                    filename=link.get("title"),
                    url=f"{dataurl}{href}?raw=true"
                ))
        return content


class Pictures(Container):
    root_path = getpath("home").joinpath("Pictures/containers")
    db_path = base_path.joinpath(
        f"db/container/pictures-files.json"
    )
    folders = list(i.name for i in root_path.iterdir() if i.is_dir())

    def __init__(self, folder):
        super().__init__(
            self.root_path, folder
        )
        self.info.content = []
        self.getdata()

    def getdata(self):
        self.info.content = []
        for yr in self.path.joinpath("photos").iterdir():
            if yr.is_dir():
                date = ["", "", yr.name.split("-")[0]]
                for month in list(yr.iterdir()):
                    date[1] = month.name
                    for file in month.iterdir():
                        date[0] = file.name.split("-")[0]
                        self.info.content.append(dict(
                            name=file.name,
                            size=file.stat().st_size * 1.0e-6,
                            path=str(file.relative_to(self.root_path)),
                            date="/".join(date)
                        ))
        self.info.total_size += sum(x["size"] for x in self.info.content)
        self.info.update()
        return self.info.data

    def isupdated(self, **timer):
        t = timer if timer else {"hours": 1}
        lastupdate = self.lastupdate.copy()
        date = getdate(self.db_path)
        for i in ("year", "month", "day"):
            if date[i] != lastupdate[i]:
                return False
        for i in t:
            if t[i] < abs(date[i] - lastupdate[i]):
                return False
        else:
            return True

    @staticmethod
    def get_worker(**timer):
        class Worker:
            @staticmethod
            def task():
                for i in Pictures.folders:
                    folder = Pictures(i)
                    if not folder.isupdated(**timer):
                        data = []
                        for v in Pictures.alldata().values():
                            data.extend(v["content"])
                        Json.save(Pictures.db_path, data)
                        print('Pictures Data Updated')
                        break

            def init(self):
                while True:
                    try:
                        timeout(self.task, 5)
                    except KeyboardInterrupt:
                        pass
        return Worker()

    @staticmethod
    def alldata():
        return {
            i: Pictures(i).info.data
            for i in Pictures.folders
        }

    def push(self):
        if self.info.ready_to_push:
            CLI.input(
                f"cd {self.root_path} && bash push {self.name}"
            )




class Pictures(Container):
    root = Path.home().joinpath("Pictures/containers")
    ids = [i for i in root.iterdir() if i.is_dir()]

    def __init__(self, folder):
        super().__init__(self.root, folder)
        self.url_root = join(
            env["GIT-URL"], "alanmatzumiya",
            f"pictures_{folder}", "blob/main/photos"
        )

    def getdata(self):
        self.info.content.clear()
        root_folder = self.path.joinpath("photos")
        for yr in (i for i in root_folder.iterdir() if i.name != ".nothing"):
            ydata = dict()
            size = 0.0
            for month in yr.iterdir():
                ydata[month.name] = get_files(month)
                for yi in ydata[month.name]:
                    size += yi["size"]
                    yi["url"] = yi["path"].replace(
                        str(root_folder), self.url_root
                    ) + "?raw=true"
            if ydata:
                ydata["size"] = size
                self.info.content.append(ydata)
        self.info.update()
        return self.info.data

    class Pictures:
        path = Path(getjson(datafile)["local-container"]["pictures"])
        ids = list(i.name for i in path.joinpath("containers").iterdir() if i.is_dir())

        @staticmethod
        def update_folders():
            def push(folder_path):
                print(" && ".join([
                    f"cd {str(folder_path)}", "python3 -m main set allow-push true"
                ]))
                print(" && ".join([
                    f"cd {str(folder_path)}", "python3 -m main push"
                ]))

            for i in Pictures.ids:
                cont = Pictures.path.joinpath(f"containers/{i}")
                write_files(cont, f"pictures_{i}")
                push(cont)

"""""


