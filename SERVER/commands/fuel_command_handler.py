import json
import subprocess
import os
from logging import log
from pprint import pprint

from commands.response_codes import Response_Codes

class Fuel_Command_Handler(Response_Codes):
    def __init__(self) -> None:
        super().__init__()
        self.isForcInstalled()
        self.valid_commands = {
            "create_workspace": self.create_workspace,
            "delete_workspace": self.delete_workspace,
            "get_workspaces": self.get_workspace,
            "create_file": self.create_file,
            "rename_file": self.rename_file,
            "add_to_file": self.add_to_file,
            "delete_file": self.delete_file,
            "deploy_contracts":self.deploy_contracts,
            "run_transaction":self.run_transaction,
            "run_script": self.run_script,
            "create_account": self.create_account,
            "create_user": self.create_user,
            "is_user": self.is_user
        }
        self.BASE_DIR = "users"
        self.invalid_command_response = {"result": self.ERROR, "detail": self.invalid_command}
        self.invalid_server_response = {"result": self.ERROR, "detail": self.invalid_server, "error": "Server erred @ FLOW CLI inputs, please check your input values"}
        self.WALLET_CREATOR_ACCOUNT = "0x7721b98bbf12fcb9"
        self.WALLET_CREATOR_KEY = "4d2834338c2a35aca39ab8be94b45fc5d5722975a1114e0f3dac80ee32813e5e"

    def isForcInstalled(self):
        command = "forc --version"
        response = self.execute_shell_command(command=command)
        print(response)

    def handle_request(self, command, request):
        print(request, command)
        try:
            execution_response = self.valid_commands[command](request)
            return execution_response
        except KeyError as invalid_command:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
        
    def is_user(self, parameters):
        try:
            user = parameters["user"]
            if user in os.listdir(os.path.join(os.getcwd(),self.BASE_DIR)):
                return {"result": self.SUCCESS, "detail": "Valid user"}
            return {"result": self.ERROR, "detail": "No user on file"}
        except KeyError as missing_args:
            self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def create_user(self, parameters):
        try:
            user = parameters["user"]
            command = f"cd {self.BASE_DIR}  && mkdir {user}" #
            response = self.execute_shell_command(command=command)
            if response["result"] == "OK":
                response['detail'] = "User created successfully"
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def create_workspace(self, parameters):
        try:
            user, workspace = parameters["user"], parameters["workspace"]
            command = f"cd {self.BASE_DIR} && cd {user} && forc new {workspace}"
            response = self.execute_shell_command(command=command)
            if response["result"] == "OK":
                response['detail'] = f"Workspace {workspace} created successfully"
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def delete_workspace(self, parameters):
        try:
            user, workspace = parameters["user"], parameters["workspace"]
            command = f"cd {self.BASE_DIR} && cd {user} && rm -rf {workspace}"
            response = self.execute_shell_command(command=command)
            if response["result"] == "OK":
                response['detail'] = f"Workspace {workspace} deleted successfully"
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def get_workspace(self, parameters):
        print("getting fuel workspaces")
        try:
            user = parameters["user"]
            users_folder_path = os.path.join(os.getcwd(),"users", user)
            workspace_builder = []
            userDir = os.listdir(users_folder_path)
            for workspace in userDir :
                new_workspace = {
                    "workspace": workspace,
                    "dir": self.process_folder(os.path.join(users_folder_path, workspace)),
                }
                workspace_builder.append(new_workspace)
            return {"result": self.SUCCESS, "detail": "Retrieved Workspaces", "data": workspace_builder}
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def create_file(self, parameters):
        try:
            user, workspace, folder, file = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd {folder} && touch {file}"
            response = self.execute_shell_command(command=command)
            if response["result"] == "OK":
                response['detail'] = f"File {file} created successfully"
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
    
    def rename_file(self, parameters):
        try:
            user, workspace, folder, old_file, new_file = parameters["user"], parameters["workspace"], parameters["folder"],parameters["old_file"], parameters["new_file"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd {folder}, mv {old_file} {new_file}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
        
    def add_to_file(self, parameters):
        try:
            user, workspace, folder, file, contents = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"], parameters["contents"]
            with open(os.path.join(os.getcwd(),self.BASE_DIR, user, workspace, folder, file), "w", encoding="utf-8") as file:
                file.write(contents)
                file.close()
            return {"result": self.SUCCESS, "detail": f"File written to {folder}"}
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
        
    def delete_file(self, parameters):
        try:
            user, workspace, folder, file = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd {folder} && rm -rf {file}"
            response = self.execute_shell_command(command=command)
            if response["result"] == "OK":
                response['detail'] = f"File: {file} deleted successfully"
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def deploy_contracts(self, parameters):
        try:
            user, workspace, account, network, file, args = parameters["user"], parameters["workspace"], parameters["account_name"], parameters["network"], parameters["file"], parameters["args"]
            # path_to_contract = os.path.join("./","cadence", "contracts", file)
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && forc build"
            response = self.execute_shell_command(command=command)
            if response["result"] == "OK":
                response['detail'] = f"{file} deployed to {account} on {network} successfully"
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
        
    def run_transaction(self, parameters): 
        try:
            user, workspace, account, network, file, args = parameters["user"], parameters["workspace"], parameters["account"], parameters["network"], parameters["file"], parameters["args"]
            # path_to_transaction_file = f"./cadence/transactions/{file}"
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && forc build"
            build_response = self.execute_shell_command(command=command)
            return build_response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
        
    def create_account(self, parameters):
        try:
            user, workspace, account_name, network = parameters["user"], parameters["workspace"], parameters["account_name"], parameters["network"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && flow keys generate --output json --save ./keys.json"
            response = self.execute_shell_command(command=command)
            if response["result"] == self.SUCCESS:
                with open(os.path.join(os.getcwd(), self.BASE_DIR, user, workspace, "flow.json"), "r", encoding='utf8') as file:
                    flow_config = json.load(file)
                flow_config["accounts"]["wallet-creator-account"] = {
                    "address": self.WALLET_CREATOR_ACCOUNT,
                    "key": self.WALLET_CREATOR_KEY
                }
                with open(os.path.join(os.getcwd(), self.BASE_DIR, user, workspace, "flow.json"), "w", encoding='utf8') as file:
                    json_obj = json.dumps(flow_config, indent=4)
                    file.write(json_obj)
                    file.close()
                    with open(os.path.join(os.getcwd(), self.BASE_DIR, user, workspace, "keys.json"), "r", encoding='utf8') as keys_file:
                        generated_keys = json.load(keys_file)
                        pub_key = generated_keys.get("public")
                        priv_key = generated_keys.get("private")
                        signer = "wallet-creator-account" if network == "testnet" else "emulator-account"
                        command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && flow accounts create --key {pub_key} --signer {signer} --network {network} --config-path flow.json --output json --save new-wallet.json"
                        response = self.execute_shell_command(command=command)
                        if response["result"] == self.SUCCESS:
                            with open(os.path.join(os.getcwd(), self.BASE_DIR, user, workspace, "new-wallet.json"), "r", encoding='utf8') as new_wallet_file:
                                new_wallet = json.load(new_wallet_file)
                                address = new_wallet.get("address")
                                del flow_config["accounts"]["wallet-creator-account"]
                                flow_config["accounts"][account_name] = {
                                    "address": address,
                                    "key": priv_key
                                }
                                with open(os.path.join(os.getcwd(), self.BASE_DIR, user, workspace, "flow.json"), "w", encoding='utf8') as file:
                                    json_obj = json.dumps(flow_config, indent=4)
                                    file.write(json_obj)
                                    file.close()
                                response["data"] = {
                                    "address": address,
                                    "pubkey": pub_key,
                                    "privkey": priv_key
                                }
                                new_wallet_file.close()
                        keys_file.close()
            self.execute_shell_command(f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && rm -rf ./keys.json")
            self.execute_shell_command(f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && rm -rf ./new-wallet.json")
            if response["result"] == "OK":
                response['detail'] = f"Account {account_name} created and added to flow.json"
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def run_script(self, parameters): 
        try:
            user, workspace, network, file, args = parameters["user"], parameters["workspace"], parameters["network"], parameters["file"], parameters["args"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && forc build"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
    
    def execute_shell_command(self, command):
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf8', text=False)
        stdout, stderr = process.communicate()
        return {"result": self.SUCCESS if not stderr else self.ERROR, "detail": stdout.strip(), "error": stderr.strip()}

    def parseExecutionArgs(self, argsList):
        if argsList:
            return " ".join(argsList)
        return ''

    def process_folder(self, folder_path):
        folder_data = {
            'files': [],
            'subfolders': []
        }
        
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) and not item[0] == ".":
                with open(item_path, 'r') as file:
                    data = file.readlines()
                    file_object = {
                        'filename': item,
                        'content': "\n".join(data)
                    }
                    folder_data['files'].append(file_object)
            elif not os.path.isfile(item_path):
                subfolder = {
                    "name": item,
                    "root": self.process_folder(item_path)
                }
                folder_data['subfolders'].append(subfolder)
        return folder_data






