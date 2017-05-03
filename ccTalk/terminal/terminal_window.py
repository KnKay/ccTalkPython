import abc
import os

class terminal_window(object):

    environment = environment()
    information_windows = []

    size = {"width":0,"heigth":0}
    position = {"left":0,"top":0}

    @abc.abstractmethod
    def resize(self,width:int, heigth:int):
        self.size["witdth"]=width
        self.size["heigth"]=heigth

    @abc.abstractmethod
    def print(self):
        return

    @abc.abstractmethod
    def set_position(self,left:int,top:int):
        self.position["left"] = left
        self.position["top"] = top
        return



#We need some information about our environment.
class environment():
    used_heigth = 0
    available_max=0

    def __init__(self):
        self.available_max = 50

    @property
    def get_space(self):
        return self.available_max - self.used_heigth
        #Get the complete size minus what we used