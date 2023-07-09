from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from commands.command_handler import Command_Handler

app = Flask(__name__)
CORS(app)
handler = Command_Handler()

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/v1/flowde", methods=["POST"])
def command():
  request_data = request.get_json()
  return handler.handle_request(dict(request_data))

if __name__ == "__main__":
  app.run(port=5555, host="localhost", debug=True)
