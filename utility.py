import asyncio

class utility:
    def fire_and_forget(task, *args, **kwargs):
        loop = asyncio.get_event_loop()
        if callable(task):
            return loop.run_in_executor(None, task, *args, **kwargs)
        else:    
            print("fire and forget error")
            raise TypeError('Task must be a callable')
