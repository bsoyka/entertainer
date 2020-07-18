from os import getenv
from dotenv import load_dotenv

def load_configs():
    load_dotenv(verbose=True)

def get_env(env):
    return getenv(env)
