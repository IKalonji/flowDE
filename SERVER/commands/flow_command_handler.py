import json
import subprocess
import os
from logging import log

from commands.response_codes import Response_Codes

class Flow_Command_Handler(Response_Codes):
    def __init__(self) -> None:
        super().__init__()
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

    def handle_request(self, command, request):
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
            command = f"cd {self.BASE_DIR} && cd {user} && flow setup {workspace}"
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
        try:
            user = parameters["user"]
            users_folder_path = os.path.join(os.getcwd(),"users", user)
            workspace_builder = []
            userDir = os.listdir(users_folder_path)
            for workspace in userDir :
                new_workspace = {
                    "workspace": workspace,
                    "folders": {

                    },
                    "flow.json": "",
                    "README.md": ""
                }
                for file_or_folder in os.listdir(os.path.join(users_folder_path, workspace)):
                    if os.path.isfile(os.path.join(users_folder_path, workspace, file_or_folder)) :
                        with open(os.path.join(users_folder_path, workspace, file_or_folder), "r", encoding='utf8') as file:
                            file_content = file.readlines()
                            new_workspace[file_or_folder] = "\n".join(file_content)
                    elif file_or_folder == "cadence":
                        for folder in os.listdir(os.path.join(users_folder_path, workspace, "cadence")):
                            new_workspace["folders"][folder] = []
                            for file_in_folder in os.listdir(os.path.join(users_folder_path, workspace, "cadence", folder)):
                                if file_in_folder[0] == ".":
                                    continue
                                with open(os.path.join(users_folder_path, workspace, "cadence", folder, file_in_folder), "r", encoding='utf8') as file:
                                    file_content = file.readlines()
                                    new_workspace["folders"][folder].append(
                                        {
                                            "name": file_in_folder,
                                            "content": "\n".join(file_content)
                                        }
                                    )
                workspace_builder.append(new_workspace)
            return {"result": self.SUCCESS, "detail": "Retrieved Workspaces", "data": workspace_builder}
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response

    def create_file(self, parameters):
        try:
            user, workspace, folder, file = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"]
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd cadence && cd {folder} && touch {file}"
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
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd cadence && cd {folder}, mv {old_file} {new_file}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
        
    def add_to_file(self, parameters):
        try:
            user, workspace, folder, file, contents = parameters["user"], parameters["workspace"], parameters["folder"], parameters["file"], parameters["contents"]
            with open(os.path.join(os.getcwd(),self.BASE_DIR, user, workspace, "cadence", folder, file), "w", encoding="utf-8") as file:
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
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && cd cadence && cd {folder} && rm -rf {file}"
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
            path_to_contract = os.path.join("./","cadence", "contracts", file)
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && flow accounts add-contract {path_to_contract} {self.parseExecutionArgs(args)} --network {network} --signer {account}"
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
            path_to_transaction_file = f"./cadence/transactions/{file}"
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && flow transactions send {path_to_transaction_file} {self.parseExecutionArgs(args)} --proposer {account} --authorizer {account} --payer {account} --filter payload --network {network}"
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
            path_to_script = os.path.join("./","cadence", "scripts", file)
            command = f"cd {self.BASE_DIR} && cd {user} && cd {workspace} && flow scripts execute {path_to_script} {self.parseExecutionArgs(args)} --network {network}"
            response = self.execute_shell_command(command=command)
            return response
        except KeyError as missing_args:
            return self.invalid_command_response
        except Exception as exception:
            return self.invalid_server_response
    
    def execute_shell_command(self, command):
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf8', text=False)
        stdout, stderr = process.communicate()
        return {"result": self.SUCCESS if not stderr else self.ERROR, "detail": stdout, "error": stderr}

    def parseExecutionArgs(self, argsList):
        if argsList:
            return " ".join(argsList)
        return ''


