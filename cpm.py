#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:30:14 2018

@author: ptutak
"""
import tkinter as tk
from tkinter import ttk

class FuncButtons(tk.Frame):
    def __init__(self,*args,log,**kwargs):
        super().__init__(*args,**kwargs)
        self.log=log
        self.loadFileName=tk.StringVar()
        self.loadFileEntry=tk.Entry(self,textvariable=self.loadFileName)
        self.loadFileEntry.grid(row=0,column=0)
        self.loadFileName.set('File Name')
        self.loadFileBtn=tk.Button(self,text="Load File")
        self.loadFileBtn.grid(row=1, column=0)
        self.loadFileBtn.bind('<Button-1>',self.loadFileAction)
        self.calculateBtn=tk.Button(self,text="Calculate")
        self.calculateBtn.grid(row=2,column=0)
        self.exitBtn=tk.Button(self,text="Exit")
        self.exitBtn.grid(row=3,column=0)
    def loadFileAction(self,event):
        file=self.loadFileName.get()
        if file!='':
            with open(file,'r') as f:
                for line in f:
                    data=line.strip().split(',')
                    try:
                        data[1]=tuple(x.strip() for x in data[1].strip().split('-'))
                        if len(data[1])!=2:
                            raise ValueError
                        data[1]=(data[1][0],'-',data[1][1])
                        for i in range(2,len(data)):
                            data[i]=float(data[i])
                        if len(data)==6:
                            for x in data[2:]:
                                if type(x)!=float:
                                    raise ValueError
                        else:
                            raise ValueError
                    except:
                        print('Wrong data')
                    else:
                        self.log.insert(0,tuple(data))

class AddTask(tk.Frame):
    def __init__(self,*args,log,**kwargs):
        super().__init__(*args,**kwargs)
        self.log=log
        self.taskName=tk.StringVar()
        self.taskCont=tk.StringVar()
        self.taskTimeNorm=tk.DoubleVar()
        self.taskTimeBoard=tk.DoubleVar()
        self.taskCostNorm=tk.DoubleVar()
        self.taskCostBoard=tk.DoubleVar()
        self.taskNameEntry=tk.Entry(self,textvariable=self.taskName)
        self.taskNameEntry.grid(row=0,column=0)
        self.taskContEntry=tk.Entry(self,textvariable=self.taskCont)
        self.taskContEntry.grid(row=0,column=1)
        self.taskTimeNormEntry=tk.Entry(self,textvariable=self.taskTimeNorm)
        self.taskTimeNormEntry.grid(row=0,column=2)
        self.taskTimeBoardEntry=tk.Entry(self,textvariable=self.taskTimeBoard)
        self.taskTimeBoardEntry.grid(row=0,column=3)
        self.taskCostNormEntry=tk.Entry(self,textvariable=self.taskCostNorm)
        self.taskCostNormEntry.grid(row=0,column=4)
        self.taskCostBoardEntry=tk.Entry(self,textvariable=self.taskCostBoard)
        self.taskCostBoardEntry.grid(row=0,column=5)
        self.addFirstBtn=tk.Button(self,text='Add Task First')
        self.addFirstBtn.grid(row=1,column=0,columnspan=2)
        self.addFirstBtn.bind('<Button-1>',self.addFirstBtnAction)
        self.insertBtn=tk.Button(self,text='Insert Task')
        self.insertBtn.grid(row=1,column=2,columnspan=2)
        self.insertBtn.bind('<Button-1>',self.insertBtnAction)
        self.addLastBtn=tk.Button(self,text='Add Task Last')
        self.addLastBtn.grid(row=1,column=4,columnspan=2)
        self.addLastBtn.bind('<Button-1>',self.addLastBtnAction)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        self.columnconfigure(4,weight=1)
        self.columnconfigure(5,weight=1)
        self.columnconfigure(6,weight=1)
        self.taskName.set('Task Name')
        self.taskCont.set('Task Continuum')
        self.taskTimeNorm.set('Task Time Norm')
        self.taskTimeBoard.set('Task Time Board')
        self.taskCostNorm.set('Task Cost Norm')
        self.taskCostBoard.set('Task Cost Board')
    def getTaskData(self):
        task=[]
        try:
            task.append(self.taskName.get())
            task.append(self.taskCont.get())
            task.append(self.taskTimeNorm.get())
            task.append(self.taskTimeBoard.get())
            task.append(self.taskCostNorm.get())
            task.append(self.taskCostBoard.get())
        except tk._tkinter.TclError:
            print('Wrong data format')
            return []
        else:
            return task
    def addFirstBtnAction(self,event):
        task=self.getTaskData()
        if task!=[]:
            self.log.insert(0,tuple(task))
    def insertBtnAction(self,event):
        task=self.getTaskData()
        if task!=[]:
            curSelect=self.log.curselection()
            if curSelect!=():
                self.log.insert(curSelect[0],tuple(task))
    def addLastBtnAction(self,event):
        task=self.getTaskData()
        if task!=[]:
            self.log.insert(tk.END,tuple(task))

class Log(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1,rowspan=5, sticky=tk.N+tk.S)
        self.taskList=tk.StringVar()
        self.taskListBox=tk.Listbox(self,yscrollcommand=self.yScroll.set)
        self.taskListBox.grid(row=0,column=0,rowspan=5,sticky=tk.N+tk.S+tk.W+tk.E)
        self.yScroll['command'] = self.taskListBox.yview
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
    def insert(self,index,task):
        self.taskListBox.insert(index,tuple(task))
    def curselection(self):
        return self.taskListBox.curselection()

if __name__=='__main__':
    root = tk.Tk()
    log=Log(root)
    log.grid(row=0,column=0,sticky=tk.N+tk.W+tk.S+tk.E)
    AddTask(root,log=log).grid(row=1,column=0)
    fButtons=FuncButtons(root,log=log)
    fButtons.grid(row=0,column=1,columnspan=2,sticky=tk.N+tk.W+tk.S+tk.E)
    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.mainloop()