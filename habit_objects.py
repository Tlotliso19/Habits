''' on this module to record all object related code'''

##important modules 
import sqlite3 # for data recording 
import calendar # for time and take 
from datetime import datetime,timedelta # for time and take
import pickle # for serialization 


'''our first class to handle all habit related code '''
'''class Habits: 
    highest_streaks = {} # to hold the highest streaks as a dictionery

    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
        self.streak = 0

    def __repr__(self):
        return f"Habits(name={self.name}, frequency={self.frequency}, streak={self.streak})"

    def update_streak(self):
        if self.name in self.__class__.highest_streaks: #when there is the streak 
            #then lets check if its higher than our current one 
            if self.streak > self.__class__.highest_streaks[self.name]:
                self.__class__.highest_streaks[self.name] = self.streak
        else:
            #when it is not there at all lets add it
            self.__class__.highest_streaks[self.name] = self.streak'''
#slidely revised 
class Habits_101:
    highest_streaks = {}

    def __init__(self, name, frequency):
        if name:
            self.name = name
        else:
            raise ValueError("ENTER A VALID NAME ")
        try:
            self.frequency = int(frequency)
        except ValueError:
            raise ValueError("FREQUENCY MUST BE AN INTEGER")
        self.streak = 0

    def __repr__(self):
        return f"Habits(name={self.name}, frequency={self.frequency}, streak={self.streak})"

'''the second class that will handle the good habits code'''
'''class Good_habits(Habits):
    streaks_times = {}
    
    def __init__(self, name, frequency):
        super().__init__(name, frequency)
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.num_days = calendar.monthrange(self.year, self.month)[1]
        # Initialize the performed time for this habit if it doesn't exist
        if name not in self.__class__.streaks_times:
            self.__class__.streaks_times[name] = None

    def display_data(self):
        target = self.num_days / self.frequency
        current = self.streak
        return current, target

    def update_streak(self):
        if self.performed_on_time():
            self.streak += 1 #firstly lets update the streak 
            # secondly lets update the last perfomance time 
            self.__class__.streaks_times[self.name] = datetime.now()
        else:
           self.streak =0 #this will be set to zero
           self.__class__.streaks_times[self.name] = datetime.now() #this will remain the same 

    def performed_on_time(self):
        # Check if the habit was performed within the allowed frequency
        last_streak_time = self.__class__.streaks_times.get(self.name, None)
        if last_streak_time:
            if (datetime.now() - last_streak_time) > timedelta(days=self.frequency):
                return True
        else:
            return True
        return False

    def performed(self):
       #check if the habit has been performed 
        last_streak_time = self.__class__.streaks_times.get(self.name, None)
        if last_streak_time:
            if (datetime.now() - last_streak_time) > timedelta(days=self.frequency):
                return True
        else:
            return False
        return False'''
    
    #slidely improvements 

class Good_habits_101(Habits_101):
    streaks_times = {}

    def __init__(self, name, frequency):
        super().__init__(name, frequency)
        self.year = datetime.now().year #keeping track of time 
        self.month = datetime.now().month
        self.num_days = calendar.monthrange(self.year, self.month)[1]
        if name not in self.__class__.streaks_times:
            self.__class__.streaks_times[name] = None #adding it to the dictionery if it is not present at initialiazation

    def perform(self): #when we perform the habit
        if self.performed():
            self.update_streak()
            print(f"Habit '{self.name}' performed successfully. Streak updated.")
        else:
            print(f"Habit '{self.name}' was not performed within the allowed frequency.")

    def display_data(self): #for vidualizing 
        target = self.num_days / self.frequency
        current = self.streak
        return current, target

    def update_streak(self):
        if self.performed():

            self.streak += 1 #updating the streak
            print('has been run 1')
        else:
          print('has been run 2')
          self.streak += 0  

    def performed(self):
       
        current_time = datetime.now()
        last_streak_time = self.__class__.streaks_times.get(self.name, None)

        # Update the last performed time weather it is performed all not 
        self.__class__.streaks_times[self.name] = current_time    
        if last_streak_time is None: #then valid    
            return True
            #return False
        # If last performance was within the allowed frequency
        time_defference =(current_time - last_streak_time) < timedelta(days=int(self.frequency))
        if time_defference:
            return True
            #return False
        
        return False
    
'''for some reasons they are needed here '''
def serialize_object(obj):
    return pickle.dumps(obj)

def deserialize_object(serialized_data):
    return pickle.loads(serialized_data)
