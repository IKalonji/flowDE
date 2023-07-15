from datetime import datetime
def log(data):
    with open("logs.txt", "a") as file:
        file.write(datetime.now(), data)
        file.close()
