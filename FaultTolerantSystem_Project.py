#IN THE NAME OF ALLAAH
import numpy.random as randGen
from math import gcd
from numpy import argmin, argmax

class CPU:
    def __init__(self):
        self.state = 'idle'
    def find_end_of_currentTask(self):
        pass
    def subtractTime(self, diffTime):
        pass
        
class Task:
    def __init__(self, period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHigh, taskName, releaseTime=None, virtualDeadline=None): # TODO: remove None 
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
                newTask = Task(period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHigh, name, self.releaseTime, vD) # TODO: Add ReleaseTime
                ptTaskList.append(newTask)
        else:
            vD = self.virtualDeadline
            name = self.taskName + ",1"
            period = self.period
            rDeadline = self.rDeadline
            worstCaseLow = self.worstCaseLow
            worstCaseHigh = self.worstCaseHigh
            criticality = self.criticality
            numOfTolerance = self.numOfTolerance
            numOfExecution = self.numOfExecution
            newTask = Task(period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHigh, name, None, vD) # TODO: Add ReleaseTime
            ptTaskList.append(newTask)
        return ptTaskList

    def log(self, f):
            f.write("taskName = " + str(self.taskName) + "\n")
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
    def __init__(self, numOfTolerance, pH, rH, cLoMax, tMax, uStar, errorVal, sizeImportance, taskNumShouldBe):
        self.logBefore = "LogSet.txt"
        self.logAfter = "LogSetPrime.txt"
        self.taskList = []
        self.modifiedTaskList = []
        self.numOfTolerance = numOfTolerance
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
        self.landa = 10**(-5)
        self.numOfFaults = 0
        self.currentTime = 0
        self.cpu = CPU()
        self.indexOfNextRelease = 0
        self.timeNextEvent = 0
        self.typeOfNextEvent = "ReleaseTask"

        while (self.taskListMade == False):
            self.make_task_set()
        
        self.find_lcm()
        self.pt_preprocess()
        self.taskNum = len(self.taskList)
        self.nextReleseTimes = []
        for i in range(self.taskNum):
            self.nextReleseTimes.append(self.taskList[i].period)
        
    def find_next_event(self): # Output = relativeTime and codeNumber of the next event
        self.indexOfNextRelease = argmin(self.nextReleseTimes)
        timeNextRelease = self.nextReleseTimes[self.indexOfNextRelease]
        timeNextEnd = self.cpu.find_end_of_currentTask()
        self.timeNextEvent = min(timeNextRelease, timeNextEnd)
        if timeNextRelease < timeNextEnd:
            self.typeOfNextEvent = "ReleaseTask"
        else:
            self.typeOfNextEvent = "EndTask"
        return

    def release_task(self, releaseTime):
        taskToRelease = self.taskList[self.indexOfNextRelease]
        newTask = Task(taskToRelease.period, taskToRelease.rDeadline, taskToRelease.numOfTolerance, taskToRelease.numOfExecution, taskToRelease.criticality, taskToRelease.worstCaseLow, taskToRelease.worstCaseHighTotal, taskToRelease.taskName, releaseTime)
        newModifiedTasks = newTask.preprocessPT()
        self.modifiedTaskList += newModifiedTasks
        return

    def operateNextRelease(self):
        diffTime = self.timeNextEvent - self.currentTime 
        self.release_task(self.timeNextEvent)
        self.cpu.subtractTime(diffTime)
        self.nextReleseTimes[self.indexOfNextRelease] += self.taskList[self.indexOfNextRelease].period
        self.currentTime = self.timeNextEvent
        return

    def operateNextEnd(self):
        pass

    def operateNextEvent(self):
        # TODO: find nextEvent, operate task related to the nextEvent
        pass

    def make_Fault(self): # TODO: Is it right?
        return(randGen.exponential(1 / self.landa) )

    def find_lcm(self):
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

            numOfExecution = (2 * numOfTolerance)+ 1
            taskName = str( len(self.taskList) + 1)
            worstCaseHighTotal = worstCaseHigh * numOfExecution
            period = randGen.randint(worstCaseHighTotal, self.tMax + 1)
            rDeadline = period
            newTask = Task(period, rDeadline, numOfTolerance, numOfExecution, criticality, worstCaseLow, worstCaseHighTotal, taskName) # TODO: Adding ReleaseTime and VirtualDeadline (if Needed).
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

    def pt_preprocess(self):
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
    uStar = 0.95
    errorVal = 0.005
    taskNumShouldBe = 200
    sizeImportance = False
    mySimulation = Simulation(numOfTolerance, pH, rH, cLoMax, tMax, uStar, errorVal, sizeImportance, taskNumShouldBe)
    mySimulation.empty_log()
    mySimulation.tasksLog(False)
    mySimulation.tasksLog(True)
    print(mySimulation.uAverage)