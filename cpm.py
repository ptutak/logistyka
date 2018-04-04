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

class Log(tk.Frame):
    def __init__(self,*args):
        super().__init__(*args)
        self.loadFileBtn=tk.Button(self,text="Load File").grid(row=1, column=0,sticky=tk.N+tk.S)
        self.addTaskBtn=tk.Button(self,text="Add Task").grid(row=2,column=0)
        self.calculateBtn=tk.Button(self,text="Calculate").grid(row=3,column=0)
        self.exitBtn=tk.Button(self,text="Exit").grid(row=4,column=0)
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=2,rowspan=5, sticky=tk.N+tk.S)
        self.taskList=tk.Listbox(self,yscrollcommand=self.yScroll.set)
        self.taskList.grid(row=0,column=1,rowspan=5,sticky=tk.N+tk.S+tk.W+tk.E)
        self.yScroll['command'] = self.taskList.yview
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

if __name__=='__main__':
    root = tk.Tk()
    log=Log(root).grid(row=0,column=0,sticky=tk.N+tk.W+tk.S+tk.E)
    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.mainloop()