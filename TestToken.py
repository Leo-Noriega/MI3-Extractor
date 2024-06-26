import os

from RetrieveToken import update_token_env


def test_update_token_env():
    update_token_env()
    new_token = os.getenv("SISMEDIA_TOKEN")
    print(f'Token: {new_token}')


test_update_token_env()
