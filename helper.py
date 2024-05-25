import pathlib
import os
import inspect
import re
import datetime
from dateutil.relativedelta import relativedelta
import time

class HelperManager:
    
    
    
    @staticmethod
    def getDirFromFile(__file__, fileInSameDir):
        return pathlib.Path(os.path.dirname(__file__), fileInSameDir)
        
    @staticmethod
    def getFuncArgsNamedDict(func: object, locals:dict, notAllowedValues:list):
    
        funcArgs = inspect.getfullargspec(func).args
        
        namedParamsDict: dict = {}
        
        # Iterate func args and insert allowed values to the namedParamsDict
        for arg in funcArgs:
            if(locals[arg] not in notAllowedValues):
                namedParamsDict[arg] = locals[arg]
        return namedParamsDict
    
    
    @staticmethod
    def getMonthPeriodByStartDate(monthDate:str, dateInputFormat = "%Y-%m-%d", dateOutputFormat="%Y-%m-%d"):
        '''
            - Created for custom field in OkDesk, that point on Active start date.

            - # By default await date like %Y-%m-%d
            
            - return dateStart, dateEnd
        '''
        
        
        baseDate = datetime.datetime.strptime(monthDate, dateInputFormat)
        
        activeStartDay = baseDate.day
        
        currentDate = datetime.datetime.fromtimestamp(time.time()).date()
        
        
        dateStart = currentDate + relativedelta(day = activeStartDay)
        
        currentDay = currentDate.day
        
        dateStart:datetime.datetime = None
        
        dateEnd:datetime.datetime = None
        
        if(currentDay < activeStartDay):
            # take with last month
            dateEnd = currentDate + relativedelta(day = activeStartDay)
            
            dateStart = dateEnd - relativedelta(months=1)
            
            
            dateEnd = dateEnd - relativedelta(days=1)
            
        else:
            # take next month
            dateStart = currentDate + relativedelta(day = activeStartDay)
            
            dateEnd = dateStart + relativedelta(months=1)
            
            
            dateEnd = dateEnd - relativedelta(days=1)
            
        
        
        correctDateStart = dateStart.strftime(dateOutputFormat)
        correctDateEnd = dateEnd.strftime(dateOutputFormat)
        
        return [correctDateStart, correctDateEnd]