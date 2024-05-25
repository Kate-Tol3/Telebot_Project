import asyncio
from crontab import CronTab
from dataclasses import dataclass
from typing import List
import pathlib
from helper import HelperManager

@dataclass
class SignalEvent:
    signal: str
    func: any
    kwargs: dict
    
@dataclass
class InfinitFunc:
    timeout: int
    func: any
    kwargs: dict
      


class UpdateManager:
    
    __EventListenerList: List[SignalEvent]
    
    __InfinityFunctionsList: List[InfinitFunc]
    
    __pathToSignalSender: pathlib.Path
    __cronTag: str
    
    def __init__(self) -> None:

        
        self.__EventListenerList = []
        self.__InfinityFunctionsList = []
        self.__pathToSignalSender = HelperManager.getDirFromFile(__file__, "send_signal.py")
        
        self.__cronTag = "BOT"
        self.clearAllCronSignals()
    
    def clearAllCronSignals(self):
        cron = CronTab("root")
        listToRemove = []
        for item in cron.crons:
            if(item.comment == self.__cronTag):
                listToRemove.append(item)
        cron.remove(listToRemove)
        cron.write()
    
    async def addCronSignal(self, signal, cronTimeStr):
        cron = CronTab("root")
        cronCommand = f"python3 {self.__pathToSignalSender} {signal}"
        comment = self.__cronTag
        action = cron.new(cronCommand, comment)
        action.setall(cronTimeStr)
        cron.write()
          
    # Listen signals and execute list of target functions
    async def addSignalCronListener(self, cronTime:str, signal: str, func, **func_kwargs):
        '''
            cron-format:
            - * * * * * <= minute-hours-days-month-day_of_week
        '''
        await self.addCronSignal(signal, cronTime)
        signal = SignalEvent(signal, func, func_kwargs)
        self.__EventListenerList.append(signal)
        print(f"Add cron signal Event => {cronTime} {signal}")
        
    # Execute functions with his own timeout
    async def addInfinityFunction(self, timeout:int, func, **func_kwargs):
        infinitFunction = InfinitFunc(timeout, func, func_kwargs)
        self.__InfinityFunctionsList.append(infinitFunction)
        print(f"{func} was added to InfinityList")
        
    async def __hundleSignal(self, rd:asyncio.StreamReader, wr:asyncio.StreamWriter):

        buffer = await rd.read()
        signal = buffer.decode()
        print(f'GET SIGNAL {signal}')
        ans = "Unknown signal".encode()
        for event in self.__EventListenerList:
            if(event.signal == signal):
                ans = "Signal found".encode()
                func = event.func
                kwargs = event.kwargs
                await func(**kwargs)
                
        wr.write(ans)
        await wr.drain()
        
        wr.close()
    
    async def startSignalListener(self):
        server = await asyncio.start_server(self.__hundleSignal, "127.0.0.1", 6667)
        async with server:
            await server.serve_forever()
    
    
    async def __InfinityTask(self, timeout, func, kwarg):
        while True:
            try:
                await func(**kwarg)
                await asyncio.sleep(timeout)
            except Exception as e:
                print(f"{func} raise the exception: {e}")
    
    async def startInfinityFunc(self):
        
        task_list = []
        
        for infinity_func in self.__InfinityFunctionsList:
            task = asyncio.create_task(self.__InfinityTask(infinity_func.timeout, infinity_func.func, infinity_func.kwargs))
            task_list.append(task)
        print(task_list)
        await asyncio.wait(task_list)
    
    pass

