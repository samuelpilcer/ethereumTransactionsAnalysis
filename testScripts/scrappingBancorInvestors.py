import sys
sys.path.append("..")
from ethScrapping import EthScrapping
import logging

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s : %(processName)s : %(levelname)s : %(message)s'))
logger.addHandler(log_handler)
logger.setLevel(logging.getLevelName("DEBUG"))

if len(sys.argv) > 1:
	scrapper=EthScrapping(sys.argv[1])
	address="0xbbc79794599b19274850492394004087cbf89710"
	file_to_save="../Results/bancorInvestors.csv"
	logger.debug("Loading transactions...")
	scrapper.transactions_to_csv(address, file_to_save)
	scrapper.investors_to_csv(address, file_to_save)