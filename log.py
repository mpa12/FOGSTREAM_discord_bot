from datetime import datetime


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT_FILE = "%Y_%m_%d"


def log_command(command_name, user_name, result):
    time_use = datetime.now()
    log_text = (
        f'[INFO]: {user_name} {result} used '
        f'the "!{command_name}" command '
        f'at {time_use:{TIME_FORMAT}}'
    )
    print(log_text)

    with open(f"logs/{time_use:{TIME_FORMAT_FILE}}.txt", 'a') as f:
        f.write(f'{log_text}\n')
