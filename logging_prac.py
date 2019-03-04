import logging

if __name__ == '__main__':
    mylogger = logging.getLogger("my")
    mylogger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    mylogger.addHandler(stream_handler)

    file_handler = logging.FileHandler("my.log")
    mylogger.addHandler(file_handler)

    mylogger.info("server start!!")