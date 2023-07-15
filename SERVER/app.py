import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from logging import log
from dotenv import dotenv_values, load_dotenv
from commands.command_handler import Command_Handler
import openai

load_dotenv()
app = Flask(__name__)
CORS(app)
handler = Command_Handler()
print(os.getenv('OPENAI'))
openai.api_key = os.getenv('OPENAI')

BASE_URL = "/v1/flowde/"

@app.route("/")
def index():
  return render_template("index.html")

@app.route(f"{BASE_URL}ready")
def ready():
  return {"result": "OK", "details": "flowDE service is READY"}

@app.route(f"{BASE_URL}live")
def live():
  return {"result": "OK", "details": "flowDE service is ALIVE"}

@app.route(f"{BASE_URL}<command>", methods=["POST"])
def command(command):
  request_data = request.get_json()
  return handler.handle_request(command,dict(request_data))

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
