import os

developmentAppServerToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoxLCJuYW1lIjoibmV3TW9kaWZpZWROYW1lIiwiaXNfYWRtaW4iOmZhbHNlfSwiaWF0IjoxNTI5ODk1MTAwfQ.Ndwy-nWLQs43BImyuqZITFdR3xA2dgYshNP4qAl8iFs'

SHARED_SERVER_URI = 'https://shared-server-stories.herokuapp.com'
SHARED_SERVER_APPLICATION_OWNER = os.getenv('SHARED_SERVER_NAME', 'newModifiedName')
APP_SERVER_TOKEN = os.getenv('APP_SERVER_TOKEN', developmentAppServerToken)
SHARED_SERVER_TOKEN_VALIDATION_PATH = SHARED_SERVER_URI + '/api/token_check'
SHARED_SERVER_PING_PATH = SHARED_SERVER_URI + '/api/ping'
SHARED_SERVER_USER_PATH = SHARED_SERVER_URI + '/api/user'
SHARED_SERVER_TOKEN_PATH = SHARED_SERVER_URI + '/api/token'
SHARED_SERVER_FILE_UPLOAD_PATH = SHARED_SERVER_URI + '/api/files/upload_multipart'
