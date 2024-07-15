from loguru import logger
from common.lib.enums.TermFilesPath import TermFilesPath
from common.lib.data_models.Config import Config
from common.lib.constants import LogDefinition
from common.gui.core.WirelessHandler import WirelessHandler


class Logger:
    def __init__(self, config: Config):
        self.config = config
        self.setup()

    def setup(self):
        logger.remove()

        logger.add(
            TermFilesPath.LOG_FILE_NAME,
            format=LogDefinition.LOGFILE_DATE_FORMAT,
            level=self.config.debug.level,
            rotation=f"{LogDefinition.LOG_MAX_SIZE_MEGABYTES} MB",
            compression=LogDefinition.COMPRESSION
        )

    def add_wireless_handler(self, log_browser, wireless_handler: WirelessHandler | None = None) -> int:
        if wireless_handler is None:
            wireless_handler = WirelessHandler()

        wireless_handler.new_record_appeared.connect(log_browser.append)

        handler_id = logger.add(
            wireless_handler,
            format=LogDefinition.DISPLAY_DATE_FORMAT,
            level=self.config.debug.level
        )

        return handler_id
