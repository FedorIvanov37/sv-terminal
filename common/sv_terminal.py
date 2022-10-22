def main():
    try:
        from common.app.core.windows.error_window import ErrorWindow
        from common.app.constants.FilePath import FilePath
        from common.app.data_models.config import Config
        from common.app.core.tools.validator import Validator
        from common.app.constants.TextConstants import TextConstants

        config = Config.parse_file(FilePath.CONFIG)
        Validator(config)

        from common.app.core.tools.terminal import Terminal
        from PyQt5 import QtWidgets
        from sys import argv

        application = QtWidgets.QApplication(argv)
        terminal = Terminal(config)
        terminal.run()

        with open(FilePath.RUN_SCRIPT, "w") as run_file:
            run_file.write(TextConstants.RUNNING_SCRIPT)

        exit(application.exec_())

    except Exception as error:
        try:
            ErrorWindow(exception=error).exec_()
        except Exception as sub_error:
            print(sub_error)

        print(error)
        exit(100)


try:
    main()
except Exception as execution_error:
    print(f"Execution error: {execution_error}")
