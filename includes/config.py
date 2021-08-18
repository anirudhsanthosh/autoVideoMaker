BASE_URL = 'https://an1.com/tags/MOD/' 
PAGE = 'page/'
MAX_NUMBER_OF_GAMES = 15
VIDEO_DURATION = 1

# all proj directories
dirs = dict(
BASE_IMAGE_DIR = './images',
BASE_AUDIO_DIR = './audios',
BASE_DATA_DIR = './data',
BASE_PROCCESSED_IMAGE_DIR = './proccessedImages',
BASE_PROCCESSED_VIDEO_DIR = './proccessedVideos'
)


# all proj file
files = dict(
OLD_GAME_LIST = dirs['BASE_DATA_DIR'] + '/oldlist.json',
VIDEO_DB = dirs['BASE_DATA_DIR'] + '/VIDEO_DB.json',
GAME_DB = dirs['BASE_DATA_DIR'] + '/GAME_DB.json',
NEW_GAMES = dirs['BASE_DATA_DIR'] + '/NEW_GAMES.json',
RUNTIME_CONFIG = dirs['BASE_DATA_DIR'] +'/config.json'
)
