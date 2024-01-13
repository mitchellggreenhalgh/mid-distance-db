class TimeParser:
    def parse_time(time:str):
        temp = time.split(':')
        minutes = int(temp[0])
        seconds = float(temp[1])
           
        return 60*minutes + seconds
    
