import os
import json
import psycopg2
from datetime import datetime

def convert_to_num(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
    
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
        cur.execute("INSERT INTO LOGS (REQUEST, POST_TXT, POST_URL, STATUS, IP, SOLVE_TIME, EXE, MEMO, FLUIDNESS, DATE, SUCCESS, ID) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)", 
                    (post_data, cube.parsed_solve["txt"], cube.parsed_solve["cubedb"], status, ip, time_solve, exe_time, memo_time, fluidness, cur_time_str, success, user_id))
    else:
        cur.execute("INSERT INTO LOGS (REQUEST, STATUS, IP, DATE, ID, ERROR) VALUES (%s,%s,%s,%s,%s,%s)", 
                    (post_data, status, ip, cur_time_str, user_id, error))
    
    conn.commit()
    cur.close()
    conn.close()