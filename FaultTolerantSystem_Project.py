#IN THE NAME OF ALLAAH
import numpy.random as randGen

class CPU:
    def __init__(self):
        
class Simulation:
    def __init__(self, landa):
        self.numOfFaults = 0
        
    def make_Fault(self):
        return(randGen.exponential(1 / self.landa) )
        
    def make_Task(self, n, T):
                
    def find_next_event(self):
        
        if self.nextEvent == "Fault":
            self.numOfFaults += 1
        
        
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