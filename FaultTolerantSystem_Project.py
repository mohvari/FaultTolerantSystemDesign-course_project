#IN THE NAME OF ALLAAH
import numpy.random as randGen
from math import gcd

class CPU:
    def __init__(self):
        
class Simulation:
    def __init__(self, landa):
        self.numOfFaults = 0
        self.taskSet = []
        self.lcmOfPeriods = find_lcm(self.taskSet)

    def find_lcm(self, taskSetOnProcessor):
        lcm = taskSetOnProcessor[0].period
        for i in range(1, len(taskSetOnProcessor)):
            lcm = int (lcm * taskSetOnProcessor[i].period/gcd(lcm, taskSetOnProcessor[i].period))
        self.lcmOfPeriods = lcm

    def make_Fault(self):
        return(randGen.exponential(1 / self.landa) )
        
    def make_Task(self, n, T):
                
    def find_next_event(self):
        
        if self.nextEvent == "Fault":
            self.numOfFaults += 1
    def find_utiilization(self, taskSetOnProcessor):
        usage = 0
        for task in taskSetOnProcessor:
            usage += (taskSetOnProcessor.worstCase * (2 * taskSetOnProcessor.numOfFaults + 1) )/ taskSetOnProcessor.period
        return usage
        
class Task:
    def __init__(self, period, deadline, numOfFaults, criticality, worstCase):
        self.period = period
        self.deadline = deadline
        self.numOfFaults = numOfFaults
        self.criticality = criticality
        self.worstCase = worstCase
        
if __name__ == "__main__":
    print("This is the main")
    #print(1/3.2)
    print(makeFault(3.2))