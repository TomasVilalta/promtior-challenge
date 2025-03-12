import logging

# I don't know if this is the best way to do this
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('uvicorn.error')