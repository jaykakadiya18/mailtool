import os

def folder_messgae_file():
    try:
        folder_path = os.path.abspath('data/message_file')
        filenames = os.listdir(folder_path)
        return filenames

    except Exception as e:
        print(e)

def folder_sending_file():
    try:
        folder_path = os.path.abspath('data/sending_file')
        filenames = os.listdir(folder_path)
        return filenames

    except Exception as e:
        print(e)

