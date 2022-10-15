from common.app.constants.ReleaseDefinitoin import ReleaseDefinition
from dataclasses import dataclass


@dataclass(frozen=True)
class TextConstants:
    RUN_TERMINAL_COMMAND = "import common.sv_terminal"

    EASTER = (int("1101000", 2),  # croak
              int("1111001", 2),
              int("1110000", 2),
              int("1101110", 2),
              int("1101111", 2),
              int("1110100", 2),
              int("1101111", 2),
              int("1100001", 2),
              int("1100100", 2))

    HELLO_MESSAGE = f"""
  ::::::::  :::     ::: ::::::::::: :::::::::: :::::::::  ::::    ::::  ::::::::::: ::::    :::     :::     :::        
 :+:    :+: :+:     :+:     :+:     :+:        :+:    :+: +:+:+: :+:+:+     :+:     :+:+:   :+:   :+: :+:   :+:        
 +:+        +:+     +:+     +:+     +:+        +:+    +:+ +:+ +:+:+ +:+     +:+     :+:+:+  +:+  +:+   +:+  +:+        
 +#++:++#++ +#+     +:+     +#+     +#++:++#   +#++:++#:  +#+  +:+  +#+     +#+     +#+ +:+ +#+ +#++:++#++: +#+        
        +#+  +#+   +#+      +#+     +#+        +#+    +#+ +#+       +#+     +#+     +#+  +#+#+# +#+     +#+ +#+        
 #+#    #+#   #+#+#+#       #+#     #+#        #+#    #+# #+#       #+#     #+#     #+#   #+#+# #+#     #+# #+#        
  ########      ###         ###     ########## ###    ### ###       ### ########### ###    #### ###     ### ########## 
 
 :: {ReleaseDefinition.VERSION} ::
 """

    RUNNING_SCRIPT = f"""#
#  ::::::::  :::     ::: ::::::::::: :::::::::: :::::::::  ::::    ::::  ::::::::::: ::::    :::     :::     :::
# :+:    :+: :+:     :+:     :+:     :+:        :+:    :+: +:+:+: :+:+:+     :+:     :+:+:   :+:   :+: :+:   :+:
# +:+        +:+     +:+     +:+     +:+        +:+    +:+ +:+ +:+:+ +:+     +:+     :+:+:+  +:+  +:+   +:+  +:+
# +#++:++#++ +#+     +:+     +#+     +#++:++#   +#++:++#:  +#+  +:+  +#+     +#+     +#+ +:+ +#+ +#++:++#++: +#+
#        +#+  +#+   +#+      +#+     +#+        +#+    +#+ +#+       +#+     +#+     +#+  +#+#+# +#+     +#+ +#+
# #+#    #+#   #+#+#+#       #+#     #+#        #+#    #+# #+#       #+#     #+#     #+#   #+#+# #+#     #+# #+#
#  ########      ###         ###     ########## ###    ### ###       ### ########### ###    #### ###     ### ##########
#
#
# SmartVista Electronic Commerce Terminal
#
# Version: {ReleaseDefinition.VERSION} 
#
# Author: {ReleaseDefinition.AUTHOR}
#
# Released in {ReleaseDefinition.RELEASE} 
#
# For test environment only!
#
#
# {ReleaseDefinition.RELEASE_NOTES}
#

{RUN_TERMINAL_COMMAND}
"""
