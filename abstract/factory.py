""" This file contains Fabric abstract class """
import abc


class Factory:
    """ This class is used to mark and in the future add functionality to all
    classses which will implement fabric pattern """

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        ...
