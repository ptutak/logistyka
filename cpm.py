#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:30:14 2018

@author: ptutak
"""
import tkinter as tk
from tkinter import ttk



def addTask(event=None):
    pass


class FuncButtons(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.loadFileName=tk.StringVar()
        self.loadFileEntry=tk.Entry(self,textvariable=self.loadFileName)
        self.loadFileEntry.grid(row=0,column=0)
        self.loadFileName.set('File Name')
        self.loadFileBtn=tk.Button(self,text="Load File")
        self.loadFileBtn.grid(row=1, column=0)
        self.calculateBtn=tk.Button(self,text="Calculate")
        self.calculateBtn.grid(row=2,column=0)
        self.exitBtn=tk.Button(self,text="Exit")
        self.exitBtn.grid(row=3,column=0)

class AddTask(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.taskName=tk.StringVar()
        self.taskCont=tk.StringVar()
        self.taskTimeNorm=tk.DoubleVar()
        self.taskTimeBoard=tk.DoubleVar()
        self.taskCostNorm=tk.DoubleVar()
        self.taskCostBoard=tk.DoubleVar()
        self.taskDesc=tk.StringVar()
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
        self.taskDescEntry=tk.Entry(self,textvariable=self.taskDesc)
        self.taskDescEntry.grid(row=0,column=6)
        self.addFirstBtn=tk.Button(self,text='Add Task First')
        self.addFirstBtn.grid(row=1,column=0,columnspan=3)
        self.addLastBtn=tk.Button(self,text='Add Task Last')
        self.addLastBtn.grid(row=1,column=3,columnspan=4)
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
        self.taskDesc.set('Task Description')


class Log(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1,rowspan=5, sticky=tk.N+tk.S)
        self.taskList=tk.Listbox(self,yscrollcommand=self.yScroll.set)
        self.taskList.grid(row=0,column=0,rowspan=5,sticky=tk.N+tk.S+tk.W+tk.E)
        self.yScroll['command'] = self.taskList.yview
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

if __name__=='__main__':
    root = tk.Tk()
    Log(root).grid(row=0,column=0,sticky=tk.N+tk.W+tk.S+tk.E)
    AddTask(root).grid(row=1,column=0)
    FuncButtons(root).grid(row=0,column=1,columnspan=2,sticky=tk.N+tk.W+tk.S+tk.E)
    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.mainloop()