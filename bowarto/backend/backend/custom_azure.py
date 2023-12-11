from storages.backends.azure_storage import AzureStorage
import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

class AzureMediaStorage(AzureStorage):
    account_name = env('STORAGE_NAME') # Must be replaced by your <storage_account_name>
    account_key = env('STORAGE_KEY') # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = env('STORAGE_NAME') # Must be replaced by your storage_account_name
    account_key = env('STORAGE_KEY') # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None