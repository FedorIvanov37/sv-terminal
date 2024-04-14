from common.lib.core.Parser import Parser
from common.lib.data_models.Config import Config
from common.lib.data_models.Transaction import Transaction
from common.lib.core.Connector import Connector
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.enums.TermFilesPath import TermFilesPath


# Create objects

with open(TermFilesPath.CONFIG) as json_file:
    config: Config = Config.model_validate_json(json_file.read())

parser = Parser(config)
connector = Connector(config)

with open(TermFilesPath.DEFAULT_FILE) as json_file:
    transaction = Transaction.model_validate_json(json_file.read())

spec: EpaySpecification = EpaySpecification()


# Set variables

transaction.data_fields[spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER] = '4154816888808164'
config.host.host = '127.0.0.1'
config.host.port = 16677


# Begin processing

connector.connect_sv()
dump = parser.create_dump(transaction)
connector.send_transaction_data(trans_id=transaction.trans_id, transaction_data=dump)
