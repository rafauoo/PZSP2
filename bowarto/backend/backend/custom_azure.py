from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'pzsp2storage' # Must be replaced by your <storage_account_name>
    account_key = 'Us9XiJ4uxdcCxWMCCCE3v+ADhmO7X4waefYq9/7C9lI0lGQMh3yy3PSwPBWF6pgsThdvZkpR+ine+AStE6leSA==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'pzsp2storage' # Must be replaced by your storage_account_name
    account_key = 'Us9XiJ4uxdcCxWMCCCE3v+ADhmO7X4waefYq9/7C9lI0lGQMh3yy3PSwPBWF6pgsThdvZkpR+ine+AStE6leSA==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None