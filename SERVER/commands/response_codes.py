class Response_Codes():
    def __init__(self) -> None:
        self.ERROR = "ERROR"
        self.SUCCESS = "OK"
        self.user_exists = "User Exists"
        self.no_user = "Could not find user"
        self.invalid_request = "Invalid Request"
        self.invalid_argument = "Invalid/Incorrect Arguments"
        self.invalid_file = "Invalid file name/file name syntax"
        self.workspace_exists = "Workspace exists, delete to recreate"
        self.no_file = "No file found with the name provided"
        self.invalid_command = "Command not found"
