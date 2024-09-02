# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:44:59 2023

@author: A
"""


from vo import Member
from dao_db import MemberDao


#service
class MemberService:
    loginId = ''
    def __init__(self):
        self.dao=MemberDao()
        
    #추가, name중복 불가
    def addMember(self):
        if MemberService.loginId !='':
            print('로그인 중')
            return
        print('===추가===')
        id = input('id:')
        a = self.dao.select(id)

        if a != None:
            print('이미 존재하는 id입니다')
        
        else:      
            pwd = input('pwd:')
            name = input('name:')
            email = input('email:')
            self.dao.insert(Member(id=id, pwd=pwd, name=name, email=email))

    def delMember(self):
        print('===탈퇴===')
        if MemberService.loginId == '':
            print('로그인 필요')
            return
        id = input('회원 id: ')
        a = self.dao.select(id)
    
        if a==None:
            print('없는 아이디')
        else:
            pwd=input('패스워드:')
            if pwd == a.pwd:
                self.dao.delete(id)
                print('탈퇴되었습니다')
            else:
                print('회원정보가 없습니다 ')
        
    def login(self):
        if MemberService.loginId !='':
            print('로그인 중')
            return
        id = input('아이디 : ')
        a = self.dao.select(id)
    
        if a==None:
            print('없는 아이디')
        else:
            pwd=input('패스워드:')
            if pwd == a.pwd:
                MemberService.loginId = id
                print('로그인 성공')
            else:
                print('다시 입력하십시오')
    
    
    def logout(self): #로그인상태에서만 가능
        if MemberService.loginId == '':
            print('로그인 필요')
            return 
        MemberService.loginId = ''
        print('로그아웃 되었습니다')













