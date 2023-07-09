import json
import subprocess
import os
import time

from commands.response_codes import Response_Codes

class Command_Handler(Response_Codes):
    def __init__(self) -> None:
        super().__init__()
        process = subprocess.Popen(['pwd'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout, stderr)
        self.valid_commands = {
            "create_workspace": self.create_workspace,
            "delete_workspace": self.delete_workspace,
            "get_workspace": self.get_workspace,
            "create_file": self.create_file,
            "rename_file": self.rename_file,
            "add_to_file": self.add_to_file,
            "delete_file": self.delete_file,
            "deploy_contracts":self.deploy_contracts,
            "run_transaction":self.run_transaction,
            "run_script": self.run_script,
            "create_account": self.create_account,
            "create_user": self.create_user,
        }
        self.BASE_DIR = "users"
        self.invalid_command_response = json.dumps({"result": self.ERROR, "detail": self.invalid_command})

    def handle_request(self, request) -> json:
        try:
            execution_response = self.valid_commands[request["command"]](request)
            return json.dumps(execution_response)
        except KeyError as invalid_command:
            return self.invalid_command_response
    
    def create_user(self, parameters):
        process = subprocess.run("pwd", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.stdout, process.stderr
        print("CURRENT DIR: ", stdout)
        print("ERROR ", stderr)

        try:
            user = parameters["user"]
            command = f"cd {self.BASE_DIR}  && mkdir {user}" #
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response

    def create_workspace(self, parameters):
        try:
            user, workspace = parameters["user"], parameters["workspace"]
            command = f"cd {self.BASE_DIR} && cd {user} && flow setup {workspace}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response

    def delete_workspace(self, parameters):
        try:
            user, workspace = parameters["user"], parameters["workspace"]
            command = f"cd {self.BASE_DIR} && cd {user} && rm -rf {workspace}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response

    def get_workspace(self, parameters): ##TODO
        '''
        [
            {
                workspace: name,
                folders: {
                        "contracts": [
                            {
                                name: name,
                                content: content
                            },
                        ]
                    }
                },
                flow.json: "content",
                readme: "content"
            }
        ]
        '''
        try:
            user = parameters["user"]

            workspace = ""
            contracts = []
            transactions = []
            scripts = []
            tests = []

            return {"result": self.codes.SUCCESS, "detail": "command executed successfully"}
        except KeyError as missing_args:
            return self.invalid_command_response

    def create_file(self, parameters):
        try:
            user, workspace, folder, file = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd cadence && cd {folder} && touch {file}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
    
    def rename_file(self, parameters):
        try:
            user, workspace, folder, old_file, new_file = parameters["user"], parameters["workspace"], parameters["folder"],parameters["old_file"], parameters["new_file"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd cadence && cd {folder}, mv {old_file} {new_file}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        
    def add_to_file(self, parameters):
        try:
            user, workspace, folder, file, contents = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"], parameters["contents"]
            with open(os.path.join(os.getcwd(),self.BASE_DIR, user, workspace, "cadence", folder, file), "w") as file:
                file.write(contents)
                file.close()
            return {"result": self.SUCCESS, "detail": "File written to disk"}
        except KeyError as missing_args:
            return self.invalid_command_response
        
    def delete_file(self, parameters):
        try:
            user, workspace, folder, file = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd cadence && cd {folder} && rm -rf {file}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response

    def deploy_contracts(self, parameters): #TODO
        try:
            user, workspace, account, network, file = parameters["user"], parameters["workspace"], parameters["account"], parameters["network"], parameters["file"]
            path_to_contract = os.path.join("./","cadence", "contracts", file)
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && flow accounts add-contract {path_to_contract} --network {network} --signer {account}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        
    def run_transaction(self, parameters): #TODO
        try:
            user, workspace, account, network = parameters["user"], parameters["workspace"], parameters["account"], parameters["network"]
            return {"result": self.codes.SUCCESS, "detail": "command executed successfully"}
        except KeyError as missing_args:
            
            return self.invalid_command_response
        
    def create_account(self, parameters): #TODO
        try:
            return {"result": self.codes.SUCCESS, "detail": "command executed successfully"}
        except KeyError as missing_args:
            return self.invalid_command_response
            
    def run_script(self, parameters): #TODO
        try:
            user, workspace, account, network = parameters["user"], parameters["workspace"], parameters["account"], parameters["network"]
            return {"result": self.codes.SUCCESS, "detail": "command executed successfully"}
        except KeyError as missing_args:
            return self.invalid_command_response
    
    def execute_shell_command(self, command):
        print("Command: ", command)
        print("DIR: ", os.getcwd())
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return {"result": self.SUCCESS if not stderr else self.ERROR, "detail": stdout.decode(), "error": stderr.decode()}

