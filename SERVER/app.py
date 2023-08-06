import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from logging import log
from dotenv import dotenv_values, load_dotenv
from commands.flow_command_handler import Flow_Command_Handler
from commands.fuel_command_handler import Fuel_Command_Handler
import openai

load_dotenv()
app = Flask(__name__)
CORS(app)
flow_handler = Flow_Command_Handler()
fuel_handler = Fuel_Command_Handler()

print(os.getenv('OPENAI'))
openai.api_key = os.getenv('OPENAI')

BASE_FLOWDE_URL = "/v1/flowde/"
BASE_FUELSTATION_URL = "/v1/fuelstation/"


@app.route("/")
def index():
  return render_template("index.html")

# flowDE routes
@app.route(f"{BASE_FLOWDE_URL}ready")
def ready_flow():
  return {"result": "OK", "details": "flowDE service is READY"}

@app.route(f"{BASE_FLOWDE_URL}live")
def live_flow():
  return {"result": "OK", "details": "flowDE service is ALIVE"}

@app.route(f"{BASE_FLOWDE_URL}<command>", methods=["POST"])
def command_flow(command):
  request_data = request.get_json()
  return flow_handler.handle_request(command,dict(request_data))

# fuelstation routes
@app.route(f"{BASE_FUELSTATION_URL}ready")
def ready_fuel():
  return {"result": "OK", "details": "Fuel Station service is READY"}

@app.route(f"{BASE_FUELSTATION_URL}live")
def live_fuel():
  return {"result": "OK", "details": "Fuel Station service is ALIVE"}

@app.route(f"{BASE_FUELSTATION_URL}<command>", methods=["POST"])
def command_fuel(command):
  request_data = request.get_json()
  return fuel_handler.handle_request(command,dict(request_data))

# ricardian routes
@app.route(f"/v1/ricardian", methods=["POST"])
def ricardian():
  request_data = request.get_json()
  # create a chat completion
  chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[request_data])
  # print the chat completion
  response = chat_completion.choices[0].message.content
  if response:
    return {"result": "OK", "response": response}
  else:
    return {"result": "ERROR", "response": "ERROR in the response"}

if __name__ == "__main__":
  app.run(port=5555, host="0.0.0.0", debug=True)
