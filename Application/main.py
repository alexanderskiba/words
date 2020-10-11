import os
import json
from scripts.server.flask_server import app


def main():
    app.run(*conf_server())


def conf_server():
    """Returns tuple(host, server) from the file: config.json"""
    path = os.getcwd() + "/Application/config.json"
    with open(path) as config:
        json_str = config.read()
        json_str = json.loads(json_str)

    host = json_str['server']['host']
    port = json_str['server']['port']
    return host, port


if __name__ == "__main__":
    main()
