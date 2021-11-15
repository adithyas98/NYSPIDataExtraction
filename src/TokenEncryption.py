






class TokenEncryptor:
    '''
        This class is meant to handle the storage, retrieval, and creation
        of encrypted passwords.
    '''
    def __init__(self):
        '''
        Initialize the Token Encryptor
        Inputs:
            - encryptedTokenLocation: Holds the location of the json file with 
                                        users and encrypted passwords.
