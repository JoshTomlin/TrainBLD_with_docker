import os
import json
import psycopg2
from datetime import datetime

def convert_to_num(value):
    
    if value is None:
        return None

    value = value.strip()

    if ":" in value:
        print('found colon')
        minutes, seconds = value.split(":")
        print(minutes, seconds, float(minutes) * 60 + float(seconds))
        return float(minutes) * 60 + float(round(seconds, 2))

    print(float(value))
    return float(value)
    

# cube.solve_stats is a list of info about each move. When a comm is found, info about the comm is stored in ['comment']
# Want to form a list of algs used, how long each alg too to execute, how many edge, corner, flip, twists and parities there are and recog time between algs.

# {'count': 1, 'move': 'L', 'ed': 5, 'cor': 1, 'comment': {}, 'diff': 0.7908496732026143, 'perm': 'blah'} I think ed, cor are number solved
def process_solve_stats(stats):
    edge_comms = [] # (comm, recog, exec, alg)
    cor_comms = [] # (comm, recog, exec, alg)


    #for move in stats:



def add_log_of_request(request, ip, status, cube=None, error=None):
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    


    post_data = json.dumps(request)
  
    user_id = os.environ["ID"]
    cur_time_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    
    if cube:
        memo_time = convert_to_num(cube.memo_time)
        time_solve = convert_to_num(cube.time_solve)
        exe_time = convert_to_num(cube.exe_time)
        fluidness = cube.fluidness
        success = cube.success
        #print(memo_time, time_solve, exe_time)
        print(cube.solve_stats)
        #process_solve_stats(cube.solve_stats)

        cur.execute("INSERT INTO LOGS (REQUEST, POST_TXT, POST_URL, STATUS, IP, SOLVE_TIME, EXE, MEMO, FLUIDNESS, DATE, SUCCESS, ID) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)", 
                    (post_data, cube.parsed_solve["txt"], cube.parsed_solve["cubedb"], status, ip, time_solve, exe_time, memo_time, fluidness, cur_time_str, success, user_id))
    else:
        cur.execute("INSERT INTO LOGS (REQUEST, STATUS, IP, DATE, ID, ERROR) VALUES (%s,%s,%s,%s,%s,%s)", 
                    (post_data, status, ip, cur_time_str, user_id, error))
    
    conn.commit()
    cur.close()
    conn.close()