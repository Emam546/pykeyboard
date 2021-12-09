import time
import difflib
from threading import Thread
import sys
import os
FILE_PATH=os.path.dirname(__file__)
sys.path.append(FILE_PATH)
from keys import ALL_KEYS
import atexit
from win32api import GetKeyState

class keyboards():
    def __init__(self):
        self.keys = {}
        self.pressed={}
        self.checking = True
        self.__checking_thread=Thread(target=self.__checkkey_have_been_pressed)
        atexit.register(self.stop_checking_all )
    def check_key_pressed(self,key,):
        self.checking = True
        try:
            self.__checking_thread.start()
        except:pass    

        if key not in self.keys:
            self.keys.update({key: False})
            return False
        else:
            if self.keys[key] == True:
                self.keys[key] = False
                return True
            else:
                if self.__checknow(key):
                    self.keys[key] = False
                    return True
                else: return False

    def __checknow(self,key):
        try:
            the_state = True
            if self.keys[key]:
                return True
            if type(key) == tuple:
                for k in key:
                    if GetKeyState(k) >= 0:
                        the_state = False
            elif GetKeyState(key) >= 0:
                the_state = False
            return the_state
        except: return False 

    def __checkkey_have_been_pressed(self):
        def __getstat(key):
            self.keys[key]=self.__checknow(key)
        while self.checking:
            for key in self.keys.copy():
                Thread(target=__getstat,args=(key,)).start()
                
    
    def stop_checking_all(self):
        self.checking = False
        self.keys = {}

    def deletmemory(self):
        self.keys = {}
        self.pressed={}
    def the_input_recently_clicked(self):
        list_keys = []
        for key in ALL_KEYS:
            if self.check_key_pressed(key) == True:
                list_keys.append(key)
        return list_keys

    
    def whickKeyspressed(self,stime: float):

        counting = [True]
        def __cancelthread(stime: float):
            time.sleep(stime)
            counting[0] =False


        Thread(target=self.__cancelthread, args=(stime,)).start()
        the_list = []
        while counting[0]:
            for key in self.the_input_recently_clicked():
                the_list.append(key)
        return the_list
    def pressedkey(self,key):
        "get key if it press for one time or not"
        if key not in self.pressed:
            self.pressed[key]=self.check_key_pressed(key)
        if self.check_key_pressed(key) and self.pressed[key]:
            self.pressed[key]=False;return True
        if self.check_key_pressed(key)==False:
            self.pressed[key]=True
            return False


    
def findmostsimilarkey(word,printing=False):
    listofallkeys = []
    for x in ALL_KEYS:
        listofallkeys.append(ALL_KEYS[x])
    words = difflib.get_close_matches(word, listofallkeys)
    if len(word) == 0:
        return None
    elif len(words) == 1:
        if words[0] == word:
            return getvaluename(words[0])
        else:
            if printing:
                print("did you mean "+words[0]+" ?")
            return getvaluename(words[0])
    else:
        if printing:
                print("did you mean "+words[0]+" ?")
        return getvaluename(words[0])


def getvaluename(word):
    for x in ALL_KEYS:
        if ALL_KEYS[x] == word:return x
   

    
    