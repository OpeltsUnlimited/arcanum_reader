
from git import Repo
from os import path

class MyRepo():
    def __init__(self, workdir, remote) -> None:
        self.__workdir=workdir
        self.__remote=remote
        self.__currentMaster = None
        if path.isdir(workdir):
            self.__repo=Repo(workdir)
            self.__currentMaster = self.__repo.head.commit.hexsha
        else:
            self.__repo=None

    def pull(self):
        if not self.__repo:
            self.__repo=Repo.clone_from(self.__remote, self.__workdir)
        else:
            test = self.__repo.remote().pull()
        self.__currentMaster = self.__repo.head.commit.hexsha

    def getCurrentCommit(self):
        return self.__currentMaster