class TimeParser:
    def parse_time(time:str):
        temp = time.split(':')
        minutes = int(temp[0])
        seconds = float(temp[1])
        total_time_sec = 60*minutes + seconds
    
        return total_time_sec
    
