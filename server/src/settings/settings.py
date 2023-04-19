import os

NEED_NEW_BASE = False

# Настройки локальной базы
LOCAL_BASE_HOST = '10.0.2.18'
LOCAL_BASE_NAME = 'OrdoAbChaos'
LOCAL_BASE_USER_NAME = 'ordo' #os.environ.get('LOCAL_BASE_USER_NAME')
LOCAL_BASE_USER_PASSWORD = 'ordo7532159' #os.environ.get('LOCAL_BASE_USER_PASSWORD')
LOCAL_BASE_DRIVER = 'mysql+asyncmy'

# Настройки сервера
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8010