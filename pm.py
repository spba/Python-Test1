#!/usr/bin/env Python
# coding=utf-8
import os
import csv
import copy
import pickle
import zipfile
MALE = 1
FEMALE = 0
class Student():
    def __init__(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_num(self, num):
        self.num = num

class File_date():
    def __init__(self, path):
        self.path = path
        self.date_list = []

    def pick_input(self):
        with open(self.path,"rb")as f:
            self.date_list = pickle.load(f)

    def pick_output(self):
        with open(self.path,"wb")as f:
            pickle.dump(self.date_list,f)

    def pick_save_as(self, address):
        with open(str(address),"wb")as f:
            pickle.dump(self.date_list,f)

    def csv_input(self):
        with open(self.path,"r")as f:
            f_csv = csv.reader(f)#csv.reader返回的是csv.reader格式，迭代此文件获得每一行元素写入date.list
            for i in f_csv:
                self.date_list.append(i)
    
    def csv_output(self):
        with open(self.path,"w",newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.date_list)

    def csv_save_as(self, address):
        with open(address,"w",newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.date_list)

    def zip_input(self, file_path, address=''):
        self.zip = zipfile.ZipFile(self.path,"r")
        if not address:
            address = os.path.dirname(self.path)
        self.zip.extract(file_path,address)
        self.zip.close()

    def zip_output(self, file_path, zip_path=''):
        self.zip = zipfile.ZipFile(self.path,"a")
        if not zip_path:
            zip_path = file_path[len(os.path.dirname(file_path)):] 
        self.zip.write(file_path,zip_path)
        self.zip.close()

    def readzip_pickfile(self, file_path):
        self.zip = zipfile.ZipFile(self.path,"r")   
        file_in_zip = self.zip.open(file_path,"r")
        self.date_list = pickle.load(file_in_zip)
        file_in_zip.close()
        self.zip.close()
    
    def readzip_csvfile(self, file_path):#zip文件应该压缩的二进制文件，而csv只能处理文本文件 
        self.zip_input(file_path)#只能处理zip一级子目录既file_path只能是文件名,若x\\x.csv
        with open(os.path.dirname(self.path) + os.sep + file_path,"r")as f:#os.sep+file出错
            f_csv = csv.reader(f)#csv.reader返回的是csv.reader格式，迭代此文件获得每一行元素写入date.list
            for i in f_csv:
                self.date_list.append(i)

class Joseph():
    def __init__(self, star, step):
        self.__date = []
        self.__out_list = []
        self.star = star
        self.step = step
        self.__index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index < self.length():
            i = self.__index
            self.__index += 1
            return self.__date[self.__out_list[i]]
        else:
            raise StopIteration()

    def joseph_loop(self):
        self.__out_list = []#循环之前先清空列表，防止上次循环给列表赋值。
        length = self.length()
        map_list = [x for x in range(length)]
        star = self.star
        step = self.step
        for _i in range(length-1):
            index = (star + step-1)%length
            star = index
            length -= 1
            self.__out_list.append(map_list[index])
            map_list.pop(index)
        self.__out_list.append(map_list[0])

    def append(self, date):
        self.__date.append(date)
        self.joseph_loop()

    def pop(self):
        self.joseph_loop()
        return self.__date.pop()

    def remove(self, pos):
        self.joseph_loop()
        return self.__date.pop(pos)

    def length(self):
        return len(self.__date)

    def get_date(self):
        return copy.deepcopy(self.__date)#若返回self.__date,那么a=get_dateget_date()，通过改变a就可改变self.__date

"""
file_student = File_date("D:\\Python\\student-date\\student.zip")
file_student.readzip_csvfile("student/student.csv")
student_joseph = Joseph(2,3)
for i in file_student.date_list:
    print(i)
    student_joseph.append(i)
print("-----------------------------------")
for i in student_joseph:
    print(i)
"""

file_student = File_date("D:\\Python\\student-date\\student.zip")
file_student.readzip_pickfile("student/student-pick.txt")
student_joseph = Joseph(1,2)
for i in file_student.date_list:
    print(i.name)
    student_joseph.append(i)
print("-----------------------------------")
for i in student_joseph:
    print(i.name)

"""
student_pb = Student("pb")
student_z1 = Student("z1")
student_z2 = Student("z2")
student_z3 = Student("z3")
student_z4 = Student("z4")
student_z5 = Student("z5")
student_z6 = Student("z6")
file_student = File_date("pickle.txt")
file_student.date_list = [student_pb,student_z1,student_z2,student_z3,student_z4,student_z5,student_z6]
file_student.pick_output()
file_student.pick_input()
for i in file_student.date_list:
    print(i.name)
student_joseph = Joseph(2,3)
for i in range(len(file_student.date_list)):
    student_joseph.append(file_student.date_list[i])
print("---------------------------------")
for i in student_joseph:
    print(i.name)
"""

"""
file_student_csv = File_date("student.csv")
file_student_csv.date_list = [["num","name","sex" ,"age"], 
                              [1    ,"pb"  ,MALE  ,23   ],                       
                              [2    ,"le"  ,FEMALE,20   ],
                              [3    ,"zs"  ,MALE  ,22   ],
                              [4    ,"ls"  ,FEMALE,24   ],
                              [5    ,"ww"  ,FEMALE,26   ],
                              [6    ,"zl"  ,MALE  ,22   ],]
file_student_csv.csv_output()
file_student_csv.date_list = []
file_student_csv.csv_input()
for i in file_student_csv.date_list:
    print(i)
student_joseph = Joseph(7,2)
for i in file_student_csv.date_list:
    student_joseph.append(i)
print("-------------------------------")
for i in student_joseph:
    print(i)
"""
