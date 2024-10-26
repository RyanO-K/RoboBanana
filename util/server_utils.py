from config import YAMLConfig as Config

HOST = os.getenv("SERVER_HOST")
PORT = os.getenv("SERVER_PORT")


def get_base_url():
    return f"http://{HOST}:{PORT}"
