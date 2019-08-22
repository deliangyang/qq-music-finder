import logging


logging.basicConfig(
    #filename='query.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

debug = logging.FileHandler('query.debug.log', encoding='utf-8')
debug.setLevel(logging.DEBUG)
debug.setFormatter(_format)

info = logging.FileHandler('query.log', encoding='utf-8')
info.setLevel(logging.INFO)
info.setFormatter(_format)

error = logging.FileHandler('query.error.log', encoding='utf-8')
error.setLevel(logging.ERROR)
error.setFormatter(_format)

logger = logging.getLogger(__name__)
logger.addHandler(debug)
logger.addHandler(info)
logger.addHandler(error)
