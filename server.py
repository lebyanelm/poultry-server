"""
_________________________________
SERVER_NAME
Server description goes here
__________________________________
"""
import gspread
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv

from models.response import Response

"""
__________________________________
DEVELOPMENTAL ENVIRONMENT VARIABLES
__________________________________
"""
if environ.get("environment") != "production":
	load_dotenv()


"""
__________________________________
SERVER INSTANCE SETUP
__________________________________
"""
server_instance = Flask(__name__,
			static_folder="./assets/",
            static_url_path="/server_name/assets/")
server_instance.config["PROPAGATE_EXCEPTIONS"] = True
server_instance.config["TRAP_HTTP_EXCEPTIONS"] = True
CORS(server_instance, resources={r"*": {"origins": "*"}})



"""
__________________________________
DATABASE CONNECTION
__________________________________
"""
gc = gspread.service_account("service-account.json")
sheet = gc.open("Flock controls").worksheet("Controls Panel")

CELLS_MAP = {
		# Flock cycle start date to count flock age
		"flock_age": "B9",

		# Heat lamp toggle states.
		"heatlamps": "B3",
		"lights": "B4",
		"cycle_manual_end": "B5",

		"last_update_time": "B10",
		"system_uptime": "B11"
	}


"""
__________________________________
SERVER INSTANCE ROUTES
__________________________________
"""
# Update a cell of the flock sheet
"""
@server_instance.route("/status", methods=["GET"])
@cross_origin()
def status():
	return {"status": "ok"}

"""
# Update a cell of the flock sheet
@server_instance.route("/control/<control>/<value>", methods=["POST"])
@cross_origin()
def update_cell(control, value):
	cell = CELLS_MAP[control]
	value = value.strip().upper()
	sheet.update(cell, [[value]], value_input_option="USER_ENTERED")
	return jsonify({
		"status": "ok",
		"control": control,
		"cell": cell,
		"value": value })


# Reads the value of a cell from a sheet
@server_instance.route("/control/<control>", methods=["GET"])
@cross_origin()
def get_control(control):
	cell = sheet.acell(CELLS_MAP[control])
	value = cell.value
	return jsonify({
		"control": control,
        "cell": cell.address,
        "value": value })