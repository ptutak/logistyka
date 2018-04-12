#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:30:14 2018

@author: ptutak
"""
import tkinter as tk
from tkinter import ttk

class FuncButtons(tk.Frame):
    def __init__(self,*args,log,countlog,**kwargs):
        super().__init__(*args,**kwargs)
        self.log=log
        self.countLog=countlog
        self.loadFileName=tk.StringVar()
        self.loadFileEntry=tk.Entry(self,textvariable=self.loadFileName)
        self.loadFileEntry.grid(row=0,column=0)
        self.loadFileName.set('File Name')
        self.loadFileBtn=tk.Button(self,text="Load File")
        self.loadFileBtn.grid(row=1, column=0)
        self.loadFileBtn.bind('<Button-1>',self.loadFileAction)
        self.calculateBtn=tk.Button(self,text="Calculate")
        self.calculateBtn.grid(row=2,column=0)
        self.calculateBtn.bind('<Button-1>',self.calculateBtnAction)
        self.exitBtn=tk.Button(self,text="Exit")
        self.exitBtn.grid(row=4,column=0)
        self.exitBtn.bind('<Button-1>',self.exitBtnAction)
        self.clearBtn=tk.Button(self,text="Clear")
        self.clearBtn.grid(row=3,column=0)
        self.clearBtn.bind('<Button-1>',self.clearBtnAction)
    def clearBtnAction(self,event):
        self.log.clearTasks()
        self.countLog.clearTasks()
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
                        if data[2]-data[3]!=0:
                            data.append((data[5]-data[4])/(data[2]-data[3]))
                        else:
                            data.append(0)
                        self.log.insertTask(tk.END,tuple(data))
    def exitBtnAction(self,event):
        root.destroy()
    def dfsNode(self,node,p,path,start,paths):
        if node==start:
            paths.append(list(reversed(path)))
            return
        for x in p[node]:
            nexPath=list(path)
            nexPath.append((x,node))
            self.dfsNode(x,p,nexPath,start,paths)
    def dfsPaths(self,p,start,stop):
        paths=[]
        for x in p[stop]:
            nexPath=list()
            nexPath.append((x,stop))
            self.dfsNode(x,p,nexPath,start,paths)
        return paths
    def getCriticalPaths(self,tasksEdges,tasksGraph,start,stop):
        Q=list(tasksGraph.keys())
        Q=set(Q)
        p=dict(zip(Q,[[] for i in range(len(Q))]))
        while Q:
            u=Q.pop()
            for w in tasksGraph[u]:
                p[w].append(u)
        critPaths=self.dfsPaths(p,start,stop)
        toRemove=[]
        maxTime=0
        times=[]
        for path in critPaths:
            time=0
            for task in path:
                time+=tasksEdges[task]
            times.append(time)
            if time>maxTime:
                maxTime=time
        for path in critPaths:
            if times[critPaths.index(path)]<maxTime:
                toRemove.append(path)
        for path in toRemove:
            critPaths.remove(path)
        return critPaths
    def getTaskEdges(self,tasks,index):
        tasksEdges={}
        for task in tasks:
            tasksEdges[(task[1][0],task[1][2])]=task[index]
        return tasksEdges
    def getTaskGraph(self,tasks):
        tasksGraph={}
        for task in tasks:
            if task[1][0] not in tasksGraph:
                tasksGraph[task[1][0]]=[]
                tasksGraph[task[1][0]].append(task[1][2])
            else:
                tasksGraph[task[1][0]].append(task[1][2])
        tasksValues=list()
        for x in tasksGraph.values():
            tasksValues.extend(x)
        tasksValues=set(tasksValues)
        starts=[]
        stops=[]
        for x in tasksGraph.keys():
            if x not in tasksValues:
                starts.append(x)
        for x in tasksValues:
            if x not in set(tasksGraph.keys()):
                stops.append(x)
        for x in stops:
            tasksGraph[x]=[]
        return (tasksGraph,starts,stops)
    def calculateToCutPaths(self,toCutPaths,taskCosts):
        chosenIndexes=[0 for i in range(len(toCutPaths))]
        chosenTasks=[None for i in range(len(toCutPaths))]
        chosenIndexes[0]=-1
        run=True
        reduction=[]
        while run:
            chosenIndexes[0]+=1
            overflow=False
            for i in range(len(toCutPaths)):
                chosenTasks[i]=None
            for i in range(len(toCutPaths)):
                if not chosenTasks[i]:
                    if overflow:
                        chosenIndexes[i]+=1
                        overflow=False
                    if chosenIndexes[i]==len(toCutPaths[i]):
                        chosenIndexes[i]=0
                        overflow=True
                    chosenTasks[i]=toCutPaths[i][chosenIndexes[i]]
                    for j in range(i+1,len(toCutPaths)):
                        if chosenTasks[i] in toCutPaths[j]:
                            chosenTasks[j]=chosenTasks[i]
                    if overflow and i+1==len(toCutPaths):
                        run=False
                        break
            cost=0
            for task in chosenTasks:
                cost+=taskCosts[task]
            if (cost,tuple(chosenTasks)) in reduction:
                break
            reduction.append((cost,tuple(chosenTasks)))
        reduction=sorted(reduction)
        if len(reduction)>0:
            return reduction[0]
        return []
    def calculateBtnAction(self,event):
        tasks=self.log.getTasks()
        tasksGraph,starts,stops=self.getTaskGraph(tasks)
        if len(starts)!=len(stops)!=1:
            print("Error, many start and stops in graph")
        else:
            start=starts[0]
            stop=stops[0]
            taskTimes=self.getTaskEdges(tasks,2)
            critPaths=self.getCriticalPaths(dict(taskTimes),tasksGraph,start,stop)
            self.log.insertText('Crit paths:')
            for path in critPaths:
                time=0
                self.log.insertText(path)
                for task in path:
                    time+=taskTimes[task]
                
                self.log.insertText('time: {0}'.format(time))
            cost=0
            while True:
                start=starts[0]
                stop=stops[0]
                taskTimes=self.getTaskEdges(tasks,2)
                taskBoardTimes=self.getTaskEdges(tasks,3)
                critPaths=self.getCriticalPaths(dict(taskTimes),tasksGraph,start,stop)
                taskCosts=self.getTaskEdges(tasks,6)
                for i in range(len(critPaths)):
                    critPaths[i]=sorted(critPaths[i],key=lambda k:taskCosts[k])
                toCutPaths=list()
                for path in critPaths:
                    toCutPath=[]
                    for x in path:
                        if taskTimes[x]>taskBoardTimes[x]:
                            toCutPath.append(x)
                    if toCutPath:
                        toCutPaths.append(toCutPath)
                if len(toCutPaths)<len(critPaths):
                    break
                if not toCutPaths:
                    break
                toCutTasks=self.calculateToCutPaths(toCutPaths,taskCosts)
                if not toCutTasks:
                    break
                toCutTasksSet=dict()
                for task in toCutTasks[1]:
                    if task in toCutTasksSet:
                        toCutTasksSet[task]+=1
                    else:
                        toCutTasksSet[task]=1
                for k,v in toCutTasksSet.items():
                    cost+=taskCosts[k]
                for i in range(len(tasks)):
                    for task in toCutTasksSet.keys():
                        if task[0]==tasks[i][1][0] and task[1]==tasks[i][1][2]:
                            newTask=list(tasks[i])
                            newTask[2]=newTask[2]-1.0
                            newTask[4]=newTask[4]+taskCosts[task]
                            tasks[i]=tuple(newTask)
            self.countLog.clearTasks()
            self.countLog.putTasks(tasks)
            self.countLog.insertText('Total cost:')
            self.countLog.insertText(cost)
            
            self.countLog.insertText('New crit paths:')
            critPaths=self.getCriticalPaths(dict(taskTimes),tasksGraph,start,stop)
            for path in critPaths:
                time=0
                for task in path:
                    time+=taskTimes[task]
                self.countLog.insertText(path)
                
                self.countLog.insertText('time: {0}'.format(time))
            
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
            task[-1]=tuple(x.strip() for x in task[-1].strip().split('-'))
            if len(task[-1])!=2:
                raise ValueError
            task[-1]=(task[-1][0],'-',task[-1][1])
            task.append(self.taskTimeNorm.get())
            task.append(self.taskTimeBoard.get())
            task.append(self.taskCostNorm.get())
            task.append(self.taskCostBoard.get())
            if task[2]-task[3]!=0:
                task.append((task[5]-task[4])/(task[2]-task[3]))
            else:
                task.append(0)
        except:
            print('Wrong data format')
            return []
        else:
            return task
    def addFirstBtnAction(self,event):
        task=self.getTaskData()
        if task!=[]:
            self.log.insertTask(0,tuple(task))
    def insertBtnAction(self,event):
        task=self.getTaskData()
        if task!=[]:
            curSelect=self.log.curSelection()
            if curSelect!=():
                self.log.insertTask(curSelect[0],tuple(task))
    def addLastBtnAction(self,event):
        task=self.getTaskData()
        if task!=[]:
            self.log.insertTask(tk.END,tuple(task))

class Log(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1,rowspan=5, sticky=tk.N+tk.S)
        self.taskList=tk.StringVar()
        self.taskListBox=tk.Listbox(self,yscrollcommand=self.yScroll.set,listvariable=self.taskList)
        self.taskListBox.grid(row=0,column=0,rowspan=5,sticky=tk.N+tk.S+tk.W+tk.E)
        self.yScroll['command'] = self.taskListBox.yview
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.tasks=[]
    def insertText(self,text,index=tk.END):
        self.taskListBox.insert(index,text)
    def insertTask(self,index,task):
        if index=='end':
            self.tasks.append(task)
        else:
            self.tasks.insert(index,task)
        self.taskListBox.insert(index,task)
    def putTasks(self,tasks):
        self.tasks=tasks
        for task in tasks:
            self.taskListBox.insert(tk.END,tuple(task))
    def curSelection(self):
        return self.taskListBox.curselection()
    def getTasks(self):
        return self.tasks
    def clearTasks(self):
        self.tasks=[]
        self.taskList.set('')

if __name__=='__main__':
    root = tk.Tk()
    log=Log(root)
    log.grid(row=0,column=0,sticky=tk.N+tk.W+tk.S+tk.E)
    countLog=Log(root)
    countLog.grid(row=1,column=0,sticky=tk.N+tk.W+tk.S+tk.E)
    AddTask(root,log=log).grid(row=2,column=0)
    fButtons=FuncButtons(root,log=log,countlog=countLog)
    fButtons.grid(row=0,column=1,columnspan=2,sticky=tk.N+tk.W+tk.S+tk.E)
    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.grid_rowconfigure(1,weight=1)
    root.mainloop()