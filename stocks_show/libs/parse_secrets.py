import os
from importlib import import_module


def _get_credential_from_secrets(credential_key):
    try:  # will succeed locally if secret.py file is available
        secret_module = import_module("proj_secrets")
        return getattr(secret_module, credential_key)
    except ModuleNotFoundError:  # will fail on Heroku after deployments
        return None


def get_credential(credential_key):
    return os.environ.get(credential_key, _get_credential_from_secrets(credential_key))


ALPHA_ADVANTAGE_API_KEY = get_credential("ALPHA_ADVANTAGE_API_KEY")
