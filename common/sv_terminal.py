"""

  ::::::::  :::     ::: ::::::::::: :::::::::: :::::::::  ::::    ::::  ::::::::::: ::::    :::     :::     :::
 :+:    :+: :+:     :+:     :+:     :+:        :+:    :+: +:+:+: :+:+:+     :+:     :+:+:   :+:   :+: :+:   :+:
 +:+        +:+     +:+     +:+     +:+        +:+    +:+ +:+ +:+:+ +:+     +:+     :+:+:+  +:+  +:+   +:+  +:+
 +#++:++#++ +#+     +:+     +#+     +#++:++#   +#++:++#:  +#+  +:+  +#+     +#+     +#+ +:+ +#+ +#++:++#++: +#+
        +#+  +#+   +#+      +#+     +#+        +#+    +#+ +#+       +#+     +#+     +#+  +#+#+# +#+     +#+ +#+
 #+#    #+#   #+#+#+#       #+#     #+#        #+#    #+# #+#       #+#     #+#     #+#   #+#+# #+#     #+# #+#
  ########      ###         ###     ########## ###    ### ###       ### ########### ###    #### ###     ### ##########

 SvTerminal v0.15 starting file

 This file runs SvTerminal GUI. The GUI runs once the file is imported, no any additional actions required

 e.g.: import common.sv_terminal

"""


if __name__ == "__main__":  # Do not run directly
    raise RuntimeError(f"The file common/sv_terminal.py should be imported from main working directory, " 
                       "direct run has no effect")


from common.gui.core.SvTerminalGui import SvTerminalGui
from common.gui.constants.TermFilesPath import TermFilesPath
from common.lib.data_models.Config import Config
from sys import exit


config: Config = Config.parse_file(TermFilesPath.CONFIG)
status: int = SvTerminalGui(config).run()
exit(status)
