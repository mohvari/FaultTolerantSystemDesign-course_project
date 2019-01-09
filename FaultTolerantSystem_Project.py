#IN THE NAME OF ALLAAH
import numpy.random as randGen
from math import gcd
from numpy import argmin, argmax
from copy import deepcopy

class CPU:
    def __init__(self):
        self.state = 'idle'
        self.currTask = None
        self.endOfTask = 10000
        self.currTime = 0
        self.landa = 10**(-1)

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
        self.currTime = self.endOfTask # TODO: Is it right?
        self.state = 'idle'
        self.endOfTask = 10000
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
        self.ENDTIME = 100000# TODO: self.numOfSimulationPeriods * self.H
        self.simulate_Slice_EDF_VD()
        print(self.Reliablity)
        
    def simulate_EDF(self):
        pass

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
        self.firstTime = True 
        while (True):
            if self.firstTime == False:
                self.find_next_event()
                self.operate_next_event()
            else: 
                self.firstTime = False
            self.VDs = []
            for i in range(len(self.Qready)):
                self.VDs.append(self.Qready[i].virtualDeadline)
  
            if self.cpu.state == 'idle' and len(self.Qready) != 0:
                indexMinVD = argmin(self.VDs)
                taskToOperate = self.Qready[indexMinVD]
                if taskToOperate.criticality == 'High':
                    for j in range(1, taskToOperate.numOfExecution): # Not numOfExecution + 1  
                        index = self.find_index_task(taskToOperate.i, j)
                        if index != None:
                            self.cpu.do_task(self.Qready[index], self.currentTime)
                        else:
                            print("Kill yourself")
                        self.go_until_correct_time()
                    result = self.find_correctness_operation(taskToOperate.i, taskToOperate.k, taskToOperate.numOfExecution)
                    if result == True:  
                        index = self.find_index_task(taskToOperate.i, taskToOperate.numOfExecution)
                        del self.Qready[index]
                        self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = True
                    else:
                        numFor = len(self.Qready)
                        for y in range(numFor):
                            for eachTask in self.Qready: # TODO: WTF?
                                if eachTask.criticality == "Low":
                                    self.Qready.remove(eachTask)
                        index = self.find_index_task(taskToOperate.i, taskToOperate.numOfExecution)
                        self.cpu.do_task(self.Qready[index], self.currentTime)
                        self.go_until_correct_time()
                        if self.fingerPrints[taskToOperate.i - 1][taskToOperate.k - 1][taskToOperate.numOfExecution - 1] == True:
                            self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = True
                        else:
                            self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = False
                else:
                    index = self.find_index_task(taskToOperate.i, taskToOperate.j)
                    self.cpu.do_task(self.Qready[index], self.currentTime)
                    self.go_until_correct_time()
                    if self.fingerPrints[taskToOperate.i - 1][taskToOperate.k - 1][taskToOperate.numOfExecution - 1] == True:
                            self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = True
                    else:
                        self.correctlyDone[taskToOperate.i - 1][taskToOperate.k - 1] = False

    def go_until_correct_time(self):
        self.find_next_event()
        while self.typeOfNextEvent != "END TASK":
            self.operate_next_event()
            self.find_next_event()
        self.operate_next_event()
        return

    def find_correctness_operation(self, input_i, input_k, numOfExecution):
        i = input_i - 1
        k = input_k - 1
        num = numOfExecution - 1
        for x in range(num):
            if self.fingerPrints[i][k][x] == False:
                return False
        return True

    def END_SIMULATION(self, type):
        M = 0
        TotalNum = 0
        for i in self.correctlyDone:
            TotalNum += len(self.correctlyDone[i])
        for i in self.correctlyDone:
            for k in self.correctlyDone[i]:
                if k == True:
                    M += 1
        self.Reliablity = M / TotalNum
        return

    def find_index_task(self, i, j):
        for x in range(len(self.Qready)):
            if ( (self.Qready[x].i == i) and (self.Qready[x].j == j) ):
                return x
        if True:
            print("Kill yourself!")
            return -1

    def find_next_event(self): # Output = relativeTime and codeNumber of the next event
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
        kMax = 0
        for x in range(len(self.modifiedTaskList)):
            if self.modifiedTaskList[x].i == i:
                if kMax < self.modifiedTaskList[x].k:
                    kMax = self.modifiedTaskList[x].k
        if kMax == 0:
            print("Definitly kill yourself.")
        return kMax

    def operate_next_release(self):
        taskToRelease = self.taskList[self.indexOfNextRelease]
        k = self.find_k_of_task_with_i(taskToRelease.i)
        k += 1
        newTask = Task(taskToRelease.period, taskToRelease.rDeadline, taskToRelease.numOfTolerance, taskToRelease.numOfExecution, taskToRelease.criticality, taskToRelease.worstCaseLow, taskToRelease.worstCaseHigh, taskToRelease.taskName,taskToRelease.i, taskToRelease.j, k, self.timeNextEvent)
        newModifiedTasks = newTask.preprocessPT()
        self.Qready += newModifiedTasks
        self.modifiedTaskList += newModifiedTasks
        self.nextReleseTimes[self.indexOfNextRelease] += self.taskList[self.indexOfNextRelease].period
        self.currentTime = self.timeNextEvent
        return

    def operate_next_termination(self):
        terminatedTask = self.cpu.terminate_task()
        self.currentTime = self.cpu.currTime
        i = terminatedTask.i - 1
        k = terminatedTask.k - 1 
        # j = terminatedTask.j - 1
        while len(self.fingerPrints[i]) <  (k + 1):
            self.fingerPrints[i].append([])
            self.correctlyDone[i].append([])
        self.fingerPrints[i][k].append(terminatedTask.fingerPrint)
        index = self.find_index_task(terminatedTask.i, terminatedTask.j)
        try:
            del self.Qready[index]
        except:
            print("nothing")
        return

    def operate_next_event(self):
        if self.typeOfNextEvent == "END SIMULATION":
            self.END_SIMULATION("Slice EDF_VD")
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


if __name__ == "__main__":
    print("This is the main")
    numOfTolerance = 1
    pH = 0.5
    rH = 4
    cLoMax = 10
    tMax = 200
    uStar = 0.70
    errorVal = 0.005
    taskNumShouldBe = 200
    sizeImportance = False
    numOfSimulationPeriods = 5
    mySimulation = Simulation(numOfTolerance, pH, rH, cLoMax, tMax, uStar, errorVal, sizeImportance, taskNumShouldBe, numOfSimulationPeriods)
    mySimulation.empty_log()
    mySimulation.tasksLog(False)
    mySimulation.tasksLog(True)
    print(mySimulation.uAverage)