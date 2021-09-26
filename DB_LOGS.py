# -*- coding: utf-8 -*-

import psycopg2
import json
import time
from datetime import datetime
import os
def convert_to_num(str_num):
    if ":" not in str_num:
        return str_num
    minute = int(str_num.split(':')[0])
    sec = int(str_num.split(':')[1].split(".")[0])
    milisec = int(str_num.split(':')[1].split(".")[1])
    final_num = 60 * minute + sec + milisec/100
    return final_num


def add_log_of_request(request, ip, status, cube=None, error=None):
    DB_HOST = "ec2-44-196-44-90.compute-1.amazonaws.com"
    DB_NAME = "dc4npj3mroe80u"
    DB_USER = "zhejkeslajejbt"
    DB_PASS = "88e5c43fbbf892eb62a835e9945b76ede2890b691c060173d91df2bedb820ae8"
    post_data = json.loads(request)
    id = os.environ["ID"]
    cur_time_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    if cube:
        memo_time = convert_to_num(cube.memo_time)
        time_solve =convert_to_num(cube.time_solve)
        exe_time = convert_to_num(cube.exe_time)
        fluidness = cube.fluidness
        success = cube.success

    post_data = json.loads(request)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    if cube:
        cur.execute("INSERT INTO LOGS (REQUEST, POST_TXT, POST_URL, STATUS, IP, SOLVE_TIME, EXE, MEMO, FLUIDNESS, DATE, SUCCESS, ID) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)", (json.dumps(post_data, ensure_ascii=False).encode('utf-8').decode('utf-8'),cube.parsed_solve["txt"],cube.parsed_solve["cubedb"], status, ip, time_solve, exe_time, memo_time, fluidness, cur_time_str, success, id))
    else:
        cur.execute("INSERT INTO LOGS (REQUEST, STATUS, IP,DATE, ID ,ERROR) VALUES (%s,%s,%s,%s,%s,%s)", (json.dumps(post_data),status, ip, cur_time_str,id,error))
    conn.commit()
    cur.close()
    conn.close()