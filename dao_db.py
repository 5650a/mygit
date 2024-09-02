# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:41:39 2023

@author: A
"""
import cx_Oracle as oci
from vo import Member

#Dao
class MemberDao:
    def __init__(self):
        self.conn = None
    def connect(self):
        self.conn = oci.connect(user='system', password='oraclejava', dsn='localhost:1521/xe')
    def disconn(self):
        self.conn.close()
    
    # 추가 메서드
    def insert(self, a:Member):
        #1. db커넥션 수립
        self.connect()
        #2. 사용할 커서객체 생성, db작업 메서드가 이 클래스가 정의되어 있어 필수
        cursor = self.conn.cursor()
        #3. 실행할 sql문 정의
        sql = 'insert into member(id, pwd, name, email) values(:id,:pwd,:name,:email)'
        #4. %s 값 튜플로 정의
        d = {'id' : a.id, 'pwd' : a.pwd, 'name' : a.name, 'email' : a.email}
        #5. sql 실행(실행할 sql, 매칭한 튜플)
        cursor.execute(sql, d)
        #6. 쓰기동작
        self.conn.commit()
        #db커넥션 디스커넥트
        self.disconn()
    
    # 검색 메서드
    def select(self, id:str): #num(pk)기준 1개검색
        try:
            self.connect()
            cursor = self.conn.cursor()
            sql = 'select * from member where id=:s'
            d = {'s':id}
            cursor.execute(sql, d)
            row = cursor.fetchone() #fetchone() : 현재 커서 위치의 한 줄 추출
            if row:
                return Member(row[0], row[1], row[2], row[3])
        except Exception as e:
            print(e)
        finally:
            self.disconn()
    
    

    def delete(self, id:str): #num(pk)기준 1개검색
        try:
            self.connect()
            cursor = self.conn.cursor()
            sql = 'delete from member where id=:s'
            d = {'s':id}
            cursor.execute(sql, d)
            self.conn.commit()
            
        except Exception as e:
            print(e)
        finally:
            self.disconn()













