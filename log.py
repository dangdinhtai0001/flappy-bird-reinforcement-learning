import time

def log_score(file_name, score, counter):
    with open(file_name, "a") as file:
        file.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')},{counter},{score}\n")
