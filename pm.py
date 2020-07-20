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
class FileReader():
    filetype = "" 
    
    @staticmethod
    def match_file(path):
        if path.endswith(FileReader.filetype):
            return True
        else:
            return False

class PickleReader(FileReader):#类名称PickleReader
    filetype = ".txt"

    def __init__(self, path):
        self.path = path
        self.file = open(self.path,"rb")
        self.data = []
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self.data:
            self.data = pickle.load(self.file)
        self.index += 1
        if self.index <= len(self.data):
            return self.data[self.index-1]
        else:
            raise StopIteration()

    def read(self):#层次太复杂，一次性load然后在迭代，文件不要操作太多次浪费时间成本
        self.data = pickle.load(self.file)
        return self.data

    def write(self, address=""):
        if not address:
            address = self.path
        with open(address,"wb")as f:
            pickle.dump(self.data,f)
    
    @staticmethod
    def match_file(path):
        if path.endswith(PickleReader.filetype):
            return True
        else:
            return False

    def __del__(self):
        self.file.close()

class CsvReader(FileReader):
    filetype = ".csv"
    def __init__(self, path):
        self.path = path
        self.file = open(self.path,"r")
        self.f_csv = csv.reader(self.file)
        self.data = []

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.f_csv.__next__()
        except EOFError:
            raise StopIteration()     

    def read(self):
        for i in self.f_csv:
            self.data.append(i)   
        return self.data

    def write(self, address=""):
        if not address:
            address = self.path
        with open(address,"w",newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.data)

    @staticmethod
    def match_file(path):
        if path.endswith(CsvReader.filetype):
            return True
        else:
            return False

    def __del__(self):
        self.file.close()

class ZipReader(FileReader):
    filetype = "zip"

    def __init__(self, path, address=""):
        self.path = path
        self.file = zipfile.ZipFile(self.path,"r")
        self.address = address
        self.data = []  
        self.index = 0
    
    def __iter__(self):
        return self   

    def __next__(self):
        if not self.data:
            self.read()
        self.index += 1
        if self.index <= len(self.data):
            return self.data[self.index-1]
        else:
            raise StopIteration()

    def read(self):  
        if self.address.endswith("csv"):
            with self.file.open(self.address,"r")as f:
                f_csv = f.readlines()
                for i in f_csv:
                    self.data.append(str(i,"UTF-8"))   
        if self.address.endswith("txt"):
            with self.file.open(self.address,"r")as f:
                self.data = pickle.load(f)
        return self.data
          
    def output(self, out_path=''):
        if not out_path:
            out_path = os.path.dirname(self.path)
        self.file.extract(self.address,out_path)
    
    def input(self, source_path, in_path=''):
        self.zip = zipfile.ZipFile(self.path,"a")
        if not in_path:
            in_path = source_path[len(os.path.dirname(source_path)):] 
        self.zip.write(source_path,in_path)
        self.zip.close()
        self.file = zipfile.ZipFile(self.path,"r")

    @staticmethod
    def match_file(path):
        if path.endswith(ZipReader.filetype):
            return True
        else:
            return False

    def __del__(self):
        self.file.close()

def file_read(path):
    dir = path.split("/")
    for i in dir:
        if ZipReader.match_file(i):
            zip_path = '/'.join(dir[0:dir.index(i)+1])
            obj_path = '/'.join(dir[dir.index(i)+1:])
            data = ZipReader(zip_path,obj_path)
            return data.read()
    for x in FileReader.__subclasses__():
        if x.match_file(path):
            data = x(path)
    return data.read()

def file_readline(path):
    dir = path.split("/")
    for i in dir:
        if ZipReader.match_file(i):
            zip_path = '/'.join(dir[0:dir.index(i)+1])
            obj_path = '/'.join(dir[dir.index(i)+1:])
            data = ZipReader(zip_path,obj_path)
            return data.__next__()
    for x in FileReader.__subclasses__():
        if x.match_file(path):
            data = x(path)
    return data.__next__()
"""
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
        #self.zip_input(file_path)#只能处理zip一级子目录既file_path只能是文件名,若x\\x.csv
        #with open(os.path.dirname(self.path) + os.sep + file_path,"r")as f:#os.sep+file出错
            #f_csv = csv.reader(f)#csv.reader返回的是csv.reader格式，迭代此文件获得每一行元素写入date.list
            #for i in f_csv:
                #self.date_list.append(i)

        #self.zip = zipfile.ZipFile(self.path,"r")
        #f_csv = self.zip.open(file_path,"r").read().decode("UTF-8")
        #self.date_list = f_csv.split(" ")

        self.zip = zipfile.ZipFile(self.path,"r")
        f_csv = self.zip.open(file_path,"r").readlines()
        for i in f_csv:
            self.date_list.append(str(i,"UTF-8"))
"""
class Joseph():
    def __init__(self, star, step):#start别省略
        self.__date = []#内部变量一根下划线
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
student_pick = PickleReader("D:/Python/student-date/pickle.txt")
student_pick.read()
for i in student_pick:
    print(i.name)

student_csv = CsvReader("D:/Python/student-date/student.csv")
for i in student_csv:
    print(i)

student_zip_csv = ZipReader("D:/Python/student-date/student.zip","student/student.csv")
for i in student_zip_csv:
    print(i,end="")

student_zip_pick = ZipReader("D:/Python/student-date/student.zip","student/pickle.txt")
for i in student_zip_pick:
    print(i.name)
"""
data = file_read("D:/Python/student-date/pickle.txt")
assert data[0].name == "pb"
data = file_read("D:/Python/student-date/student.csv")
assert data[0] == ['num','name','sex','age']
data = file_readline("D:/Python/student-date/pickle.txt")
assert data.name == "pb"
data = file_readline("D:/Python/student-date/student.csv")
assert data == ['num','name','sex','age']
data = file_read("D:/Python/student-date/student.zip/student/student.csv")
assert data[0] == "num,name,sex,age\r\n"
data = file_readline("D:/Python/student-date/student.zip/student/student.csv")
assert data == "num,name,sex,age\r\n"
data = file_read("D:/Python/student-date/student.zip/student/pickle.txt")
assert data[0].name == 'pb'
data = file_readline("D:/Python/student-date/student.zip/student/pickle.txt")
assert data.name == 'pb'
"""
student_pick = File_pick("D:/Python/student-date/pickle.txt")
print(file_readline(student_pick))
print(file_readline(student_pick))
print(file_readline(student_pick))
student_csv = File_csv("D:/Python/student-date/student.csv")
print(file_readline(student_csv))
print(file_readline(student_csv))
print(file_readline(student_csv))
print(file_readline(student_csv))
print(file_readline(student_csv))
print(file_readline(student_csv))
student_zip_csv = File_zip("D:/Python/student-date/student.zip","student/student.csv")
print(file_readline(student_zip_csv),end="")
print(file_readline(student_zip_csv),end="")
print(file_readline(student_zip_csv),end="")
print(file_readline(student_zip_csv),end="")
print(file_readline(student_zip_csv),end="")
print(file_readline(student_zip_csv),end="")
print(file_readline(student_zip_csv),end="")
"""

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
