#IN THE NAME OF ALLAAH
import numpy.random as randGen
from math import gcd
from numpy import argmin, argmax, exp
from copy import deepcopy
from datetime import datetime

class CPU:
    def __init__(self):
        self.state = 'idle'
        self.currTask = None
        self.endOfTask = 10000
        self.currTime = 0
        self.landa = 10**(-5)

    def make_Fault(self): # TODO: Is it right?
        return(randGen.exponential(1 / self.landa) )

    def do_task(self, task, currTime):
        self.state = 'busy'
        faultTime = self.make_Fault()
        self.currTask = task
        self.currTime = currTime
        if faultTime <= self.currTask.worstCaseHigh:
            self.currTask.fingerPrint = False
        else:
            self.currTask.fingerPrint = True
        self.endOfTask = self.currTask.worstCaseHigh + self.currTime
        return

    def find_end_of_currentTask(self):
        return self.endOfTask

    def terminate_task(self):
        print("cpu termination")
        self.currTime = self.endOfTask # TODO: Is it right?
        if self.state == False:
            print("Shit")
        self.state = 'idle'
        self.endOfTask = 10000000
        return self.currTask

    
        
class Task:
    def __init__(self, period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHigh, taskName, i, j, k, releaseTime=None, virtualDeadline=None): # TODO: remove None 
        self.i = i
        self.k = k
        self.j = j
        self.fingerPrint = False
        self.taskName = taskName
        self.period = period
        self.rDeadline = rDeadline
        self.criticality = criticality
        self.worstCaseLow = worstCaseLow
        self.worstCaseHigh = worstCaseHigh
        self.numOfTolerance = numOfTolerance
        self.numOfExecution = numOfExecution
        if self.criticality == 'High':
            # self.numOfTolerance = numOfTolerance
            self.delta = self.worstCaseHigh
        else:
            # self.numOfTolerance = 0
            self.delta = 0
        # self.numOfExecution = 2 * self.numOfTolerance + 1
        if releaseTime == None:
            self.releaseTime = 0
        else:
            self.releaseTime = releaseTime
        if virtualDeadline == None :
            self.virtualDeadline = int(self.releaseTime) + self.rDeadline - self.delta
        else:
            self.virtualDeadline = virtualDeadline

    def preprocessPT(self, releaseTime=None):
        ptTaskList = []
        if self.criticality == 'High':
            for j in range(1, self.numOfExecution + 1):
                k = self.k
                worstCaseLow = self.worstCaseLow
                worstCaseHigh = int( self.worstCaseHigh / self.numOfExecution )
                possibleRVD = ( (self.rDeadline * j) / self.numOfExecution ) - worstCaseHigh
                vD = self.releaseTime + max(0, possibleRVD)
                name = self.taskName + "," + str(j)
                period = self.period
                rDeadline = self.rDeadline
                criticality = self.criticality
                numOfTolerance = self.numOfTolerance
                numOfExecution = self.numOfExecution
                i = self.i
                newTask = Task(period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHigh, name, i, j, k, self.releaseTime, vD) # TODO: Add ReleaseTime
                ptTaskList.append(newTask)
        else:
            k = self.k
            vD = self.virtualDeadline
            name = self.taskName + ",1"
            j = self.j
            i = self.i
            period = self.period
            rDeadline = self.rDeadline
            worstCaseLow = self.worstCaseLow
            worstCaseHigh = self.worstCaseHigh
            criticality = self.criticality
            numOfTolerance = self.numOfTolerance
            numOfExecution = self.numOfExecution
            newTask = Task(period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHigh, name,i, j, k, None, vD) # TODO: Add ReleaseTime
            ptTaskList.append(newTask)
        return ptTaskList

    def log(self, f):
            f.write("taskName = " + str(self.taskName) + "\n")
            f.write("k = " + str(self.k) + "\n")
            f.write("worsCaseLow = " + str(self.worstCaseLow) + "\n")
            f.write("worsCaseHigh = " + str(self.worstCaseHigh) + "\n")
            f.write("T = " + str(self.period) + "\n")
            f.write("D = " + str(self.rDeadline) + "\n")
            f.write("criticality = " + str(self.criticality) + "\n")
            f.write("numOfTolerance = " + str(self.numOfTolerance) + "\n")
            f.write("numOfExecution = " + str(self.numOfExecution) + "\n")
            f.write("releaseTime = " + str(self.releaseTime) + "\n")
            f.write("delta = " + str(self.delta) + "\n")
            f.write("VD = " + str(self.virtualDeadline) + "\n")
            return

class Simulation: # TODO: Rename the class! 
    def __init__(self, numOfTolerance, pH, rH, cLoMax, tMax, uStar, errorVal, sizeImportance, taskNumShouldBe, numOfSimulationPeriods):
        self.logBefore = "LogSet.txt"
        self.logAfter = "LogSetPrime.txt"
        self.numOfSimulationPeriods = numOfSimulationPeriods
        self.taskList = []
        self.uStar = uStar
        self.errorVal = errorVal
        self.uStarMin = self.uStar - self.errorVal
        self.uStarMax = self.uStar + self.errorVal
        self.pH = pH
        self.rH = rH
        self.cLoMax = cLoMax
        self.tMax = tMax
        self.taskNum = 0
        self.taskNumShouldBe = taskNumShouldBe
        self.sizeImportance = sizeImportance
        self.taskListMade = False
        self.uAverage = self.uStarMin - errorVal # set uAverage minimum, first of all.
        self.uLow = 0
        self.uHigh = 0
        self.H = 0
        self.numOfFaults = 0
        self.numOfTolerance = numOfTolerance
        # End of Initializing
        self.abstract_make_task_set() # making Tasks
        self.taskNum = len(self.taskList)
        self.find_H()
        self.ENDTIME =  10000#self.H # TODO: * self.numOfSimulationPeriods

        startSlice = datetime.now()
        # self.simulate_Slice_EDF_VD()
        endSlice = datetime.now()
        sliceDuration = endSlice - startSlice

        startEDF = datetime.now()
        self.simulate_EDF()
        endEDF = datetime.now()
        EDFduration = endEDF - startEDF

        startVD= datetime.now()
        self.simulate_EDF_VD()
        endVD = datetime.now()
        VDduration = endVD - startVD

        print(sliceDuration, EDFduration, VDduration)

        
    def simulate_EDF(self):
        self.taskListEDF = []
        self.EDFtaskList = deepcopy(self.taskList)
        self.EDFQready = deepcopy(self.EDFtaskList)
        self.EDFnextReleaseTimes = []
        for i in range(self.taskNum):
            self.EDFnextReleaseTimes.append(self.taskList[i].period)
        self.EDFcurrentTime = 0
        self.EDFcpu = CPU()
        self.EDFindexOfNextRelease = 0
        self.EDFtimeNextEvent = 0
        self.EDFtypeOfNextEvent = ""
        self.EDFcorrectlyDone = [[] for i in range(self.taskNum)]
        self.EDFendBool = False
        self.EDFset_correctlydone()
        self.EDFdeadlines = []
        while(True):
            if self.EDFendBool == True:
                break
            self.EDFdeadlines[:] = []
            self.EDFclearQready()
            for i in range(len(self.EDFQready)):
                self.EDFdeadlines.append(self.EDFQready[i].rDeadline + self.EDFQready[i].releaseTime)
            if self.EDFcpu.state == 'idle' and len(self.EDFQready) != 0:
                indexMinDeadLine = argmin(self.EDFdeadlines)
                taskToOperate = self.EDFQready[indexMinDeadLine]
                index = self.EDFfind_index(taskToOperate.i, taskToOperate.k)
                self.EDFcpu.do_task(self.EDFQready[index], self.EDFcurrentTime)
                self.EDFdequeue_from_Qready(index)
                self.EDFgo_until_correct_time()

            self.EDFfind_next_event()
            self.EDFoperate_next_event()
        self.EDFendfunction()

    def EDF_END_SIMULATION(self):
        print("end")
        M = 0
        TotalNum = 0
        for i in range(len(self.EDFcorrectlyDone)):
            TotalNum += len(self.EDFcorrectlyDone[i])
        for i in range(len(self.EDFcorrectlyDone)):
            for k in range(len(self.EDFcorrectlyDone[i])):
                if self.EDFcorrectlyDone[i][k] == True:
                    M += 1
        self.EDF_Feasibility = M / TotalNum
        F = 1
        for y in range(len(self.EDFtaskList)):
            if self.EDFtaskList[y].criticality == 'High':
                iIndex = self.EDFtaskList[y].i - 1
                kIndex = self.EDFtaskList[y].k - 1
                if self.EDFcorrectlyDone[iIndex][kIndex] == True:
                    # TODO: for y in range(self.taskList[i].numOfExecution): /self.taskList[i].numOfExecution IS IT RIGHT?
                    F *= 1 - (1 - exp((self.EDFtaskList[y].worstCaseHigh) * (10**(-5)) * -1))
        self.Reliability = F
        self.EDFendBool = True
        return

    def EDFfind_index(self, i, k):
        print("find index")
        for x in range(len(self.EDFQready)):
            if ( (self.EDFQready[x].i == i) and (self.EDFQready[x].k == k) ):
                return x
        if True:
            print("294")
            return -1

    def EDFfind_next_event(self):
        print("find next event")
        self.EDFindexOfNextRelease = argmin(self.EDFnextReleaseTimes)
        timeNextRelease = self.EDFnextReleaseTimes[self.EDFindexOfNextRelease]
        timeNextEnd = self.EDFcpu.find_end_of_currentTask()
        self.EDFtimeNextEvent = min(timeNextRelease, timeNextEnd, self.ENDTIME)
        if self.EDFtimeNextEvent == self.ENDTIME:
            self.EDFtypeOfNextEvent = "END SIMULATION"

        elif self.EDFtimeNextEvent == timeNextEnd:
            self.EDFtypeOfNextEvent = "END TASK"

        elif self.EDFtimeNextEvent == timeNextRelease:
            self.EDFtypeOfNextEvent = "RELEASE TASK"
        return

    def EDFfind_k_of_task_with_i(self, i):
        print("find k")
        kMax = 0
        for x in range(len(self.EDFtaskList)):
            if self.EDFtaskList[x].i == i:
                if kMax < self.EDFtaskList[x].k:
                    kMax = self.EDFtaskList[x].k
        if kMax == 0:
            print("Definitly kill yourself.")
        return kMax

    def EDFoperate_next_release(self):
        print("operate next release")
        taskToRelease = self.taskList[self.EDFindexOfNextRelease]
        k = self.EDFfind_k_of_task_with_i(taskToRelease.i)
        k += 1
        newTask = Task(taskToRelease.period, taskToRelease.rDeadline, taskToRelease.numOfTolerance, taskToRelease.numOfExecution, taskToRelease.criticality, taskToRelease.worstCaseLow, taskToRelease.worstCaseHigh, taskToRelease.taskName,taskToRelease.i, taskToRelease.j, k, self.EDFtimeNextEvent)
        # newModifiedTasks = newTask.preprocessPT()
        self.EDFQready.append(newTask)
        self.EDFtaskList.append(newTask)
        self.EDFset_correctlydone()
        self.EDFnextReleaseTimes[self.EDFindexOfNextRelease] = self.EDFtimeNextEvent + self.EDFtaskList[self.EDFindexOfNextRelease].period 
        self.EDFcurrentTime = self.EDFtimeNextEvent
        return
    def EDFoperate_next_termination(self):
        print("next termination")
        terminatedTask = self.EDFcpu.terminate_task()
        self.EDFcurrentTime = self.EDFcpu.currTime
        i = terminatedTask.i - 1
        k = terminatedTask.k - 1 
        # if terminatedTask.fingerPrint == False:
        #     print("What?")
        self.EDFcorrectlyDone[i][k] = terminatedTask.fingerPrint
        return

    def EDFoperate_next_event(self):
        print("operate next event")
        if self.EDFtypeOfNextEvent == "END SIMULATION":
            self.EDF_END_SIMULATION()
        elif self.EDFtypeOfNextEvent == "END TASK":
            self.EDFoperate_next_termination()
        elif self.EDFtypeOfNextEvent == "RELEASE TASK":
            self.EDFoperate_next_release()
        return

    def EDFendfunction(self):
        print(self.EDF_Feasibility)
        print(self.Reliability)
        # self.EDFendLog
        return

    def EDFdequeue_from_Qready(self, index):
        #self.Qready.remove(self.Qready[index])
        print("dequeue")
        print(self.EDFQready[index].i, self.EDFQready[index].k)
        del self.EDFQready[index]
        return

    def EDFclearQready(self):
        listToDrop = []
        numFor = len(self.EDFQready)
        for i in range(len(self.EDFQready)):
            if (self.EDFQready[i].rDeadline + self.EDFQready[i].releaseTime) < self.EDFcurrentTime:
                listToDrop.append((self.EDFQready[i].i, self.EDFQready[i].k))
        for n in range(len(listToDrop)):
            for y in range(numFor):
                for it in self.EDFQready:
                    try:
                        if it.i == listToDrop[n][0] and it.k == listToDrop[n][1]:
                            self.EDFQready.remove(it)
                    except:
                        print("what?")
        return

    def EDFset_correctlydone(self):
        print("set correctly")
        for it in self.EDFtaskList:
            x = 0
            y = 0
            iIndex =  it.i - 1
            while( len(self.EDFcorrectlyDone) < it.i):
                self.EDFcorrectlyDone.append([])
                x += 1
                if x == 2:
                    print("What x?")
            while( len(self.EDFcorrectlyDone[iIndex]) < it.k):
                self.EDFcorrectlyDone[iIndex].append(False)
                y += 1
                # if y == 1:
                #     print("???")
                if y == 2:
                    print("What y?")
        return

    def EDFgo_until_correct_time(self):
        print("go until")
        self.EDFfind_next_event()
        if self.EDFtypeOfNextEvent == "END SIMULATION":
            self.EDFoperate_next_event()
            return
        if self.EDFcurrentTime == self.ENDTIME:
            print("EASY TIGER!")
        print(self.EDFcurrentTime)
        while self.EDFtypeOfNextEvent != "END TASK":
            self.EDFoperate_next_event()
            self.EDFfind_next_event()
        self.EDFoperate_next_event()
        return

    def simulate_EDF_VD(self):
        pass

    def simulate_Slice_EDF_VD(self):
        self.modifiedTaskList = []
        self.initial_pt_preprocess()
        self.nextReleseTimes = []
        for i in range(self.taskNum):
            self.nextReleseTimes.append(self.taskList[i].period)
        self.currentTime = 0
        self.cpu = CPU()
        self.indexOfNextRelease = 0
        self.timeNextEvent = 0
        self.typeOfNextEvent = ""
        self.Qready = []
        self.Qready = deepcopy(self.modifiedTaskList)
        self.fingerPrints = [[] for i in range(self.taskNum)] # Also remember self.i & self.j & self.k start from 1 not 0.
        self.correctlyDone = [[] for i in range(self.taskNum)]
        self.set_fingerprints()
        self.set_correctlydone()
        self.firstTime = True 
        self.ENDBOOL = False
        self.VDs = []
        while (True):
            if self.firstTime == False:
                self.find_next_event()
                self.operate_next_event()
                if self.ENDBOOL == True:
                        break
            else: 
                self.firstTime = False
            self.VDs[:] = []
            self.clearQready()
            for i in range(len(self.Qready)):
                self.VDs.append(self.Qready[i].virtualDeadline)
  
            if self.cpu.state == 'idle' and len(self.Qready) != 0:
                indexMinVD = argmin(self.VDs)
                taskToOperate = self.Qready[indexMinVD]
                if taskToOperate.criticality == 'High':
                    if taskToOperate.j == 1:
                        for j in range(1, taskToOperate.numOfExecution): # Not numOfExecution + 1  
                            # print()
                            index = self.find_index_task(taskToOperate.i, j, taskToOperate.k)
                            if index != None:
                                print(self.Qready[index].i, self.Qready[index].j, self.Qready[index].k, self.currentTime)
                                self.cpu.do_task(self.Qready[index], self.currentTime)
                                self.dequeue_from_Qready(index)
                            else:
                                print("198............................")
                            self.go_until_correct_time()
                    result = self.find_correctness_operation(taskToOperate.i, taskToOperate.k, taskToOperate.numOfExecution)
                    if result == True:  
                        index = self.find_index_task(taskToOperate.i, taskToOperate.numOfExecution, taskToOperate.k)
                        del self.Qready[index]
                        self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = True
                    else:
                        self.drop_low_from_Qready()
                        index = self.find_index_task(taskToOperate.i, taskToOperate.numOfExecution, taskToOperate.k)
                        print(self.Qready[index].i, self.Qready[index].j, self.Qready[index].k, self.currentTime)                        
                        self.cpu.do_task(self.Qready[index], self.currentTime)
                        self.dequeue_from_Qready(index)
                        self.go_until_correct_time()
                        if self.fingerPrints[taskToOperate.i - 1][taskToOperate.k - 1][taskToOperate.numOfExecution - 1] == True:
                            self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = True
                        else:
                            self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = False
                    if self.ENDBOOL == True:
                        break
                else:
                    index = self.find_index_task(taskToOperate.i, taskToOperate.j, taskToOperate.k)
                    print(self.Qready[index].i, self.Qready[index].j, self.Qready[index].k, self.currentTime)
                    self.cpu.do_task(self.Qready[index], self.currentTime)
                    self.dequeue_from_Qready(index)
                    self.go_until_correct_time()
                    if self.fingerPrints[taskToOperate.i - 1][taskToOperate.k - 1][taskToOperate.numOfExecution - 1] == True:
                            self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = True
                    else:
                        self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = False
                    if self.ENDBOOL == True:
                        break
        self.endfunction()

    def clearQready(self):
        listToDrop = []
        numFor = len(self.Qready)
        for i in range(len(self.Qready)):
            if self.Qready[i].virtualDeadline < 0:
                listToDrop.append((self.Qready[i].i, self.Qready[i].k))
        for n in range(len(listToDrop)):
            for y in range(numFor):
                for m in range(len(self.Qready)):
                    if self.Qready[m].i == listToDrop[n][0] and self.Qready[m].k == listToDrop[n][1]:
                        if self.Qready[m].j != self.Qready[m].numOfExecution:
                            self.Qready.remove(self.Qready[m])
        return

    def endfunction(self):
        print(self.Feasibility)
        print(self.Reliability)
        self.endLog()
        return

    def dequeue_from_Qready(self, index):
        #self.Qready.remove(self.Qready[index])
        print("dequeue")
        print(self.Qready[index].i, self.Qready[index].j, self.Qready[index].k)
        del self.Qready[index]
        return

    def drop_low_from_Qready(self):
        print("dropping")
        while(self.have_low()):
            for i in range(len(self.Qready)):
                if self.Qready[i].criticality == "LOW":
                    self.Qready.remove(self.Qready[i])
        return

    def have_low(self):
        print("have low")
        retBool = False
        for i in range(len(self.Qready)):
            if self.Qready[i].criticality == "LOW":
                retBool = True
        return retBool

    def set_correctlydone(self):
        print("set correctly")
        for it in self.modifiedTaskList:
            x = 0
            y = 0
            iIndex =  it.i - 1
            while( len(self.correctlyDone) < it.i):
                self.correctlyDone.append([])
                x += 1
                if x == 2:
                    print("What x?")
            while( len(self.correctlyDone[iIndex]) < it.k):
                self.correctlyDone[iIndex].append(False)
                y += 1
                # if y == 1:
                #     print("???")
                if y == 2:
                    print("What y?")
        return

    def set_fingerprints(self):
        print("set finger")
        for it in self.modifiedTaskList:
            iIndex = it.i - 1
            kIndex = it.k - 1
            while( len(self.fingerPrints) < it.i):
                self.fingerPrints.append([])
            while( len(self.fingerPrints[iIndex]) < it.k):
                self.fingerPrints[iIndex].append([])
            while( len(self.fingerPrints[iIndex][kIndex]) < it.j):
                self.fingerPrints[iIndex][kIndex].append(False)  
        return
            


    def go_until_correct_time(self):
        print("go until")
        self.find_next_event()
        if self.typeOfNextEvent == "END SIMULATION":
            self.operate_next_event()
            return
        if self.currentTime == self.ENDTIME:
            print("EASY TIGER!")
        print(self.currentTime)
        while self.typeOfNextEvent != "END TASK":
            self.operate_next_event()
            self.find_next_event()
        self.operate_next_event()
        return

    def find_correctness_operation(self, input_i, input_k, numOfExecution):
        print("find correctness")
        i = input_i - 1
        k = input_k - 1
        num = numOfExecution - 1
        for x in range(num):
            if self.fingerPrints[i][k][x] == False:
                return False
        return True

    def END_SIMULATION(self):
        print("end")
        M = 0
        TotalNum = 0
        for i in range(len(self.correctlyDone)):
            TotalNum += len(self.correctlyDone[i])
        for i in range(len(self.correctlyDone)):
            for k in range(len(self.correctlyDone[i])):
                if self.correctlyDone[i][k] == True:
                    M += 1
        self.Feasibility = M / TotalNum
        F = 1
        for i in range(len(self.fingerPrints)):
            for k in range(len(self.fingerPrints[i])):
                if len(self.fingerPrints[i][k]) > 1:
                    if self.correctlyDone[i][k] == True:
                        # TODO: for y in range(self.taskList[i].numOfExecution): /self.taskList[i].numOfExecution
                        F *= 1 - (1 - exp((self.taskList[i].worstCaseHigh) * (10**(-5)) * -1))
        self.Reliability = F
        self.ENDBOOL = True
        return

    def find_index_task(self, i, j, k):
        print("find index")
        for x in range(len(self.Qready)):
            if ( (self.Qready[x].i == i) and (self.Qready[x].j == j) and (self.Qready[x].k == k) ):
                return x
        if True:
            print("294")
            return -1

    def find_next_event(self): # Output = relativeTime and codeNumber of the next event
        print("find next event")
        self.indexOfNextRelease = argmin(self.nextReleseTimes)
        timeNextRelease = self.nextReleseTimes[self.indexOfNextRelease]
        timeNextEnd = self.cpu.find_end_of_currentTask()
        self.timeNextEvent = min(timeNextRelease, timeNextEnd, self.ENDTIME)
        if self.timeNextEvent == self.ENDTIME:
            self.typeOfNextEvent = "END SIMULATION"

        elif self.timeNextEvent == timeNextEnd:
            self.typeOfNextEvent = "END TASK"

        elif self.timeNextEvent == timeNextRelease:
            self.typeOfNextEvent = "RELEASE TASK"
        return

    def find_k_of_task_with_i(self, i):
        print("find k")
        kMax = 0
        for x in range(len(self.modifiedTaskList)):
            if self.modifiedTaskList[x].i == i:
                if kMax < self.modifiedTaskList[x].k:
                    kMax = self.modifiedTaskList[x].k
        if kMax == 0:
            print("Definitly kill yourself.")
        return kMax

    def operate_next_release(self):
        print("operate next release")
        taskToRelease = self.taskList[self.indexOfNextRelease]
        k = self.find_k_of_task_with_i(taskToRelease.i)
        k += 1
        newTask = Task(taskToRelease.period, taskToRelease.rDeadline, taskToRelease.numOfTolerance, taskToRelease.numOfExecution, taskToRelease.criticality, taskToRelease.worstCaseLow, taskToRelease.worstCaseHigh, taskToRelease.taskName,taskToRelease.i, taskToRelease.j, k, self.timeNextEvent)
        newModifiedTasks = newTask.preprocessPT()
        self.Qready += newModifiedTasks
        self.modifiedTaskList += newModifiedTasks
        self.set_correctlydone()
        self.set_fingerprints()
        self.nextReleseTimes[self.indexOfNextRelease] = self.timeNextEvent + self.taskList[self.indexOfNextRelease].period 
        self.currentTime = self.timeNextEvent
        return

    def operate_next_termination(self):
        print("next termination")
        terminatedTask = self.cpu.terminate_task()
        self.currentTime = self.cpu.currTime
        i = terminatedTask.i - 1
        k = terminatedTask.k - 1 
        j = terminatedTask.j - 1
        # if terminatedTask.fingerPrint == False:
        #     print("What?")
        self.fingerPrints[i][k][j] = terminatedTask.fingerPrint
        return

    def operate_next_event(self):
        print("operate next event")
        if self.typeOfNextEvent == "END SIMULATION":
            self.END_SIMULATION()
        elif self.typeOfNextEvent == "END TASK":
            self.operate_next_termination()
        elif self.typeOfNextEvent == "RELEASE TASK":
            self.operate_next_release()
        return

    def find_H(self):
        lcm = self.taskList[0].period
        for i in range(1, len(self.taskList)):
            lcm = int( lcm * self.taskList[i].period / gcd(lcm, self.taskList[i].period) )
        self.H = lcm
        return

    def set_uLow(self):
        self.uLow = 0
        for i in range(self.taskNum):
            if self.taskList[i].criticality == 'Low':
                self.uLow += (self.taskList[i].worstCaseLow / self.taskList[i].period) 
        return

    def set_uHigh(self):
        self.uHigh = 0
        for i in range(self.taskNum):
            if self.taskList[i].criticality == 'High':
                self.uHigh += (self.taskList[i].worstCaseHigh / self.taskList[i].period)
        return

    def set_usage(self):# setting self.uAverage, self.uLow, self.uHigh
        self.set_uLow()
        self.set_uHigh()
        self.uAverage = (self.uHigh + self.uLow) # / 2
        return

    def add_task(self):    
            worstCaseLow = randGen.randint(1, self.cLoMax) # TODO: exclusive or inclusive?
            if randGen.random() < self.pH: # criticality of task is High
                criticality = 'High'
                numOfTolerance = self.numOfTolerance
                worstCaseHigh = randGen.randint(worstCaseLow, self.rH * worstCaseLow + 1)
            else: #  criticality of task is Low
                criticality = 'Low'
                numOfTolerance = 0
                worstCaseHigh = worstCaseLow
            k = 1
            numOfExecution = (2 * numOfTolerance)+ 1
            taskName = str( len(self.taskList) + 1)
            i = len(self.taskList) + 1
            j = 1
            worstCaseHighTotal = worstCaseHigh * numOfExecution
            period = randGen.randint(worstCaseHighTotal, self.tMax + 1)
            rDeadline = period
            newTask = Task(period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHighTotal, taskName, i, j, k) # TODO: Adding ReleaseTime and VirtualDeadline (if Needed).
            self.taskList.append(newTask)
            self.taskNum = len(self.taskList)
            return
            
    def reset_usage(self):
        self.uAverage = self.uStarMin - self.errorVal # set uAverage minimum, first of all.
        self.uLow = 0
        self.uHigh = 0
        return
    
    def empty_taskList(self):
        self.taskList[:] = []
        self.taskNum = len(self.taskList)
        self.reset_usage()
        return

    def Is_same_critical(self):
        firstCriticality = self.taskList[0].criticality
        for i in range (len(self.taskList)):
            if self.taskList[i].criticality != firstCriticality:
                return False
        return True

    def abstract_make_task_set(self):
        while (self.taskListMade == False):
            self.make_task_set()
        return

    def make_task_set(self):
        if self.sizeImportance == True:
            while(self.taskNum < self.taskNumShouldBe):
                self.add_task()
                self.set_usage()
            self.taskListMade = True
            return
        else: 
            while(self.uAverage < self.uStarMin):
                self.add_task()
                self.set_usage()
            if self.uAverage > self.uStarMax:
                self.empty_taskList()
                self.taskListMade = False
                return
            elif( (self.uStarMin <= self.uAverage) and (self.uAverage <= self.uStarMax) ):
                # if ( ((self.uLow > 0.99) and (self.uHigh > 0.99)) or (self.Is_same_critical()) ): # TODO: AND or OR?
                if ( (self.uAverage > 0.99) or (self.Is_same_critical()) ): # TODO: AND or OR?
                    self.empty_taskList()
                    self.taskListMade = False
                    return
                self.taskListMade = True
                return

    def initial_pt_preprocess(self):
        self.modifiedTaskList [:] = []
        for i in range (self.taskNum):
            self.modifiedTaskList += self.taskList[i].preprocessPT()
        return
    
    def empty_log(self):
        g = open(self.logBefore, "+w")
        g.close()
        h = open(self.logAfter, "+w")
        h.close()
        return
        
    def tasksLog(self, beforeAfter):
        if beforeAfter == False:
            f = open(self.logBefore, "+a")
            f.write("H = " + str(self.H) + "\n")
            for i in range(self.taskNum):
                f.write("task " + str(i+1) + " is:\n")
                self.taskList[i].log(f)
                f.write("\n")
            f.close()
        else:
            f = open(self.logAfter, "+a")
            for i in range(len(self.modifiedTaskList)):
                f.write("modified Task " + self.modifiedTaskList[i].taskName + " is:\n")
                self.modifiedTaskList[i].log(f)
                f.write("\n")
            f.close()
        return
    def endLog(self):
        g = open("correctlyDone.txt", "+w")
        g.close()
        h = open("fingerPrints.txt", "+w")
        h.close()
        f = open("correctlyDone.txt", "+a")
        f.write("correctlyDone is:\n")
        for i in range(len(self.correctlyDone)):
            for k in range(len(self.correctlyDone[i])):
                f.write(str(self.correctlyDone[i][k]))
            f.write('\n')
        f.close()
        u = open("fingerPrints.txt", "+a")
        u.write("fingerPrints is:\n")
        for i in range(len(self.fingerPrints)):
            for k in range(len(self.fingerPrints[i])):
                u.write(str(self.fingerPrints[i][k]))
            u.write('\n')
        u.close()
        return
        


if __name__ == "__main__":
    print("This is the main")
    numOfTolerance = 1
    pH = 0.5
    rH = 4
    cLoMax = 10
    tMax = 200
    uStar = 0.90
    errorVal = 0.005
    taskNumShouldBe = 200
    sizeImportance = False
    numOfSimulationPeriods = 5
    mySimulation = Simulation(numOfTolerance, pH, rH, cLoMax, tMax, uStar, errorVal, sizeImportance, taskNumShouldBe, numOfSimulationPeriods)
    # mySimulation.empty_log()
    # mySimulation.tasksLog(False)
    # mySimulation.tasksLog(True)
    print(mySimulation.uAverage)