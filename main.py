from http_server import run_http_server
from multiprocessing import Process
from DB_LOGS import logging

def main():
    p1 = Process(target=logging)
    p1.start()
    p2 = Process(target=run_http_server)
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    main()