from os import remove, listdir
from json import dump
from datetime import datetime
from logging import error
from common.lib.data_models.Config import Config
from common.lib.constants import TermFilesPath
from common.lib.core.EpaySpecification import EpaySpecification


class SpecFilesRotator:
    spec: EpaySpecification = EpaySpecification()
    filename_head = "spec_backup_"
    filename_tail = ".json"
    date_format = "%Y%m%d_%H%M%S"

    def backup_spec(self):
        filename = f"{self.filename_head}{datetime.now():{self.date_format}}{self.filename_tail}"

        with open(f'{TermFilesPath.SPEC_BACKUP_DIR}/{filename}', "w") as file:
            dump(self.spec.spec.model_dump(), file, indent=4)

        return filename

    def clear_spec_backup(self, config: Config):
        storage_debt = config.remote_spec.backup_storage_depth

        if not config.remote_spec.backup_storage:
            storage_debt = int()

        try:
            files = listdir(TermFilesPath.SPEC_BACKUP_DIR)
        except Exception as dir_access_error:
            error(f"Cannot get specification backup files list: {dir_access_error}")
            return

        files.sort(reverse=True)

        while files:
            if len(files) < storage_debt:
                return

            file = files.pop()

            if not (file.startswith(self.filename_head) and file.endswith(self.filename_tail)):
                continue

            try:
                remove(f"{TermFilesPath.SPEC_BACKUP_DIR}/{file}")
            except Exception as remove_error:
                error(f"Cannot cleanup specification backup directory: {remove_error}")
                return
