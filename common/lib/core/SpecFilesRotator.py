from os import remove, listdir
from logging import error
from common.lib.data_models.Config import Config
from common.lib.constants import TermFilesPath


class SpecFilesRotator:
    def __init__(self, config: Config):
        self.config: Config = config

    def clear_spec_backup(self):
        storage_debt = self.config.remote_spec.backup_storage_depth

        if not self.config.remote_spec.backup_storage:
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

            if not (file.startswith('spec_backup_20') and file.endswith('.json')):
                continue

            try:
                remove(f"{TermFilesPath.SPEC_BACKUP_DIR}/{file}")
            except Exception as remove_error:
                error(f"Cannot cleanup specification backup directory: {remove_error}")
                return
