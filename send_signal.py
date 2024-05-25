import sys
import asyncio

async def sendSig(signal:str):
    
    reader, writer = await asyncio.open_connection("127.0.0.1", 6667)
    
    writer.write(signal.encode())
    
    writer.close()
    
    
if __name__ == "__main__":
    
    # First arg after filename.py
    signal = sys.argv[1]
    
    asyncio.run(sendSig(signal))