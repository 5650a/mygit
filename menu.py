# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:46:35 2023

@author: A
"""

from service import MemberService
import movie_proj

class Menu:
    def __init__(self):
        self.service=MemberService()
        
    def run(self):
        while True:
            m = input('1.회원가입 2.로그인  3.로그아웃 4. 영화검색 5.회원탈퇴 6.종료 \n')
            if m=='1':
                self.service.addMember()
            elif m=='2':
                self.service.login()
            elif m=='3':
                self.service.logout()
            elif m=='4':
                if MemberService.loginId == '':
                    print('로그인 필요')
                    continue
                movie_proj.movie_menu()
            elif m=='5':
                self.service.delMember()
            elif m=='6':
                break
    
if __name__ == '__main__':
    m = Menu()
    m.run()


