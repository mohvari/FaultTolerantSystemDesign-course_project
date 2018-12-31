#IN THE NAME OF ALLAAH
import numpy.random as randGen
from math import gcd

# class CPU:
#     def __init__(self):
#         self.state = 'idle'
        
# class Simulation:
#     def __init__(self, landa):
#         self.numOfFaults = 0
#         self.taskSet = []
#         self.lcmOfPeriods = find_lcm(self.taskSet)

#     def find_lcm(self, taskSetOnProcessor):
#         lcm = taskSetOnProcessor[0].period
#         for i in range(1, len(taskSetOnProcessor)):
#             lcm = int (lcm * taskSetOnProcessor[i].period/gcd(lcm, taskSetOnProcessor[i].period))
#         self.lcmOfPeriods = lcm

#     def find_VD(self):
#         for task in self.modifiedTaskSet:
#             if task.criticality == True : # Criticality Hi = True
#                 task.virtualDeadline = task.arivalTime + task.deadline - task.worstCase
#             else:
#                 task.virtualDeadline = task.arivalTime + task.deadline
#         return

#     def make_Fault(self):
#         return(randGen.exponential(1 / self.landa) )
        
#     def make_Task(self, n, T):
                
#     def find_next_event(self):
        
#         if self.nextEvent == "Fault":
#             self.numOfFaults += 1
#     def find_utiilization(self, taskSetOnProcessor):
#         usage = 0
#         for task in taskSetOnProcessor:
#             usage += (taskSetOnProcessor.worstCase * (2 * taskSetOnProcessor.numOfFaults + 1) )/ taskSetOnProcessor.period
#         return usage
        
class Task:
    def __init__(self, period, rDeadline, numOfFaults, numOfExecution, criticality, worstCaseLow, worstCaseHigh, taskName, releaseTime=None, virtualDeadline=None): # TODO: remove None 
        self.taskName = taskName
        self.period = period
        self.rDeadline = rDeadline
        self.criticality = criticality
        self.worstCaseLow = worstCaseLow
        self.worstCaseHigh = worstCaseHigh
        self.numOfFaults = numOfFaults
        self.numOfExecution = numOfExecution
        if self.criticality == 'High':
            # self.numOfFaults = numOfFaults
            self.delta = self.worstCaseHigh
        else:
            # self.numOfFaults = 0
            self.delta = 0
        # self.numOfExecution = 2 * self.numOfFaults + 1
        if releaseTime == None:
            self.releaseTime = 0
        else:
            self.releaseTime = releaseTime
        if virtualDeadline == None :
            self.virtualDeadline = int(self.releaseTime) + self.rDeadline - self.delta
        else:
            self.virtualDeadline = virtualDeadline

    def preprocessPT(self):
        ptTaskList = []
        if self.criticality == 'High':
            for j in range(1, self.numOfExecution + 1):
                possibleRVD = ( (self.rDeadline * j) / self.numOfExecution ) - self.worstCaseHigh
                vD = self.releaseTime + max(0, possibleRVD)
                name = self.taskName + "," + str(j)
                period = self.period
                rDeadline = self.rDeadline
                worstCaseLow = self.worstCaseLow
                worstcaseHigh = self.worstCaseHigh / self.numOfExecution
                criticality = self.criticality
                numOfFaults = self.numOfFaults
                numOfExecution = self.numOfExecution
                newTask = Task(period, rDeadline, numOfFaults, numOfExecution, criticality, worstCaseLow, worstcaseHigh, name, None, vD) # TODO: Add ReleaseTime
                ptTaskList.append(newTask)
        else:
            vD = self.virtualDeadline
            name = self.taskName + ",1"
            period = self.period
            rDeadline = self.rDeadline
            worstCaseLow = self.worstCaseLow
            worstcaseHigh = self.worstCaseHigh
            criticality = self.criticality
            numOfFaults = self.numOfFaults
            numOfExecution = self.numOfExecution
            newTask = Task(period, rDeadline, numOfFaults, numOfExecution, criticality, worstCaseLow, worstcaseHigh, name, None, vD) # TODO: Add ReleaseTime
            ptTaskList.append(newTask)
        return ptTaskList

    def log(self, f):
            f.write("taskName = " + str(self.taskName) + "\n")
            f.write("worsCaseLow = " + str(self.worstCaseLow) + "\n")
            f.write("worsCaseHigh = " + str(self.worstCaseHigh) + "\n")
            f.write("T = " + str(self.period) + "\n")
            f.write("D = " + str(self.rDeadline) + "\n")
            f.write("criticality = " + str(self.criticality) + "\n")
            f.write("numOfFaults = " + str(self.numOfFaults) + "\n")
            f.write("numOfExecution = " + str(self.numOfExecution) + "\n")
            f.write("releaseTime = " + str(self.releaseTime) + "\n")
            f.write("delta = " + str(self.delta) + "\n")
            f.write("VD = " + str(self.virtualDeadline) + "\n")
            return

class TaskSet: # TODO: Replace U_star with targetAverageUtilization at the end of the work! 
    def __init__(self, numOfFaults, pH, rH, cLoMax, tMax, uStar, errorVal, sizeImportance, taskNumShouldBe):
        self.taskList = []
        self.numOfFaults = numOfFaults
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

        while (self.taskListMade == False):
            self.make_task_set()
        
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
                numOfFaults = self.numOfFaults
                worstCaseHigh = randGen.randint(worstCaseLow, self.rH * worstCaseLow + 1)
            else: #  criticality of task is Low
                criticality = 'Low'
                numOfFaults = 0
                worstCaseHigh = worstCaseLow

            numOfExecution = (2 * numOfFaults)+ 1
            taskName = str( len(self.taskList) + 1)
            worstCaseHighTotal = worstCaseHigh * numOfExecution
            period = randGen.randint(worstCaseHighTotal, self.tMax + 1)
            rDeadline = period
            newTask = Task(period, rDeadline, numOfFaults, numOfExecution, criticality, worstCaseLow, worstCaseHighTotal, taskName) # TODO: Adding ReleaseTime and VirtualDeadline (if Needed).
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

    def tasksLog(self):
        f = open("Log.txt", "+a")
        print (self.uAverage)
        self.set_usage()
        print (self.uAverage)
        for i in range(self.taskNum):
            f.write("task " + str(i+1) + " is:\n")
            self.taskList[i].log(f)
            f.write("\n")
        f.close()
        return


        
if __name__ == "__main__":
    print("This is the main")
    numOfFaults = 1
    pH = 0.5
    rH = 4
    cLoMax = 10
    tMax = 200
    uStar = 0.95
    errorVal = 0.005
    taskNumShouldBe = 200
    sizeImportance = False
    myTaskSet = TaskSet(numOfFaults, pH, rH, cLoMax, tMax, uStar, errorVal, sizeImportance, taskNumShouldBe)
    myTaskSet.tasksLog()
    print(myTaskSet.uAverage)