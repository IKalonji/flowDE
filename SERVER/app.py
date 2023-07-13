from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from commands.command_handler import Command_Handler

app = Flask(__name__)
CORS(app)
handler = Command_Handler()

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

if __name__ == "__main__":
  app.run(port=5555, host="localhost", debug=True)
