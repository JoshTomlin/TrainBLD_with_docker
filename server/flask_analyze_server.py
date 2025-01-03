# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import json
import traceback
from BLD_Parser import parse_solve
from DB_LOGS import add_log_of_request  # Update this import statement

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def init_env_var(dict_params):
    os.environ["SMART_CUBE"] = "True" if dict_params["SMART_CUBE"] == True else "False"
    os.environ["GEN_PARSED_TO_CUBEDB"] = "True" if dict_params["GEN_PARSED_TO_CUBEDB"] == True else "False"
    os.environ["GEN_PARSED_TO_TXT"] = "True" if dict_params["GEN_PARSED_TO_TXT"] == True else "False"
    os.environ["NAME_OF_SOLVE"] = dict_params["NAME_OF_SOLVE"]
    os.environ["TIME_SOLVE"] = dict_params["TIME_SOLVE"]
    os.environ["COMMS_UNPARSED"] = "True" if dict_params["COMMS_UNPARSED"]  == True else "False"
    os.environ["GEN_WITH_MOVE_COUNT"] = "True" if dict_params["GEN_WITH_MOVE_COUNT"] == True else "False"
    os.environ["DIFF_BETWEEN_ALGS"] = dict_params["DIFF_BETWEEN_ALGS"]
    os.environ["PARSE_TO_LETTER_PAIR"] = "True" if dict_params["PARSE_TO_LETTER_PAIR"] == True else "False"
    os.environ["EDGES_BUFFER"] = dict_params["EDGES_BUFFER"]
    os.environ["CORNER_BUFFER"] = dict_params["CORNER_BUFFER"]
    os.environ["CUBE_OREINTATION"] = dict_params["CUBE_OREINTATION"]
    os.environ["LETTER_PAIRS_DICT"] = dict_params["LETTER_PAIRS_DICT"]
    os.environ["SCRAMBLE"] = dict_params["SCRAMBLE"]
    os.environ["SOLVE"] = dict_params["SOLVE"]
    os.environ["MEMO"] = dict_params["MEMO"]
    os.environ["SOLVE_TIME_MOVES"] = dict_params["SOLVE_TIME_MOVES"]
    os.environ["DATE_SOLVE"] = dict_params["DATE_SOLVE"]
    os.environ["SCRAMBLE_TYPE"] = dict_params["SCRAMBLE_TYPE"]
    os.environ["ID"] = dict_params["ID"]


def parse(dict_params):
    init_env_var(dict_params)
    cube = parse_solve(dict_params["SCRAMBLE"], dict_params["SOLVE"])
    parsed_solve = json.dumps(cube.parsed_solve)
    return parsed_solve, cube

@app.route('/parse', methods=['POST'])
def handle_parse_request():
    try:
        address = request.remote_addr
        post_data = request.get_json()

        if not post_data:
            return make_response("Invalid JSON payload", 400)

        data = parse(post_data)
        solve_str = data[0]
        cube = data[1]
        
        # Optionally log the request (commented out)
        try:
            add_log_of_request(post_data, address, '200', cube=cube)
        except:           
            add_log_of_request(post_data, address, '404', error=traceback.format_exc())

        response = make_response(solve_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        print(traceback.format_exc())
        add_log_of_request(post_data, address, '404', error=traceback.format_exc())
        return make_response({"error": "An error occurred", "details": traceback.format_exc()}, 500)

@app.route('/options', methods=['OPTIONS'])
def handle_options_request():
    response = make_response("", 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

def run_flask_server():
    # Using Flask's built-in server
    app.run(host='0.0.0.0', port=8080)
    # app.run(host='127.0.0.1', port=8080)

def main():
    run_flask_server()

if __name__ == '__main__':
    main()