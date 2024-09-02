# -*- coding: utf-8 -*-


class Member:
    def __init__(self, id=None, pwd=None, name=None, email=None):
        self.id = id
        self.pwd = pwd
        self.name = name
        self.email = email
        
    def __set__(self):
        return 'id:'+self.id+', pwd:'+self.pwd+', name:'+self.name+', email:'+self.email
    