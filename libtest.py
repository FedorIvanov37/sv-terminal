from common.lib.data_models.Config import Config
from common.lib.EpaySpecification import EpaySpecification
from common.lib.Parser import Parser
from common.lib.Connector import Connector
from common.lib.TransactionQueue import TransactionQueue
from common.lib.data_models.Transaction import Transaction

spec = EpaySpecification()
config = Config.parse_file("common/settings/config.json")
transaction = Transaction.parse_file("common/settings/transaction.json")
parser = Parser(config)
connector = Connector(config)
queue = TransactionQueue(connector)
