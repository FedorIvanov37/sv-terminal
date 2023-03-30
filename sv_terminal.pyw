#
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
# Version: v0.15 
#
# Author: Fedor Ivanov | Unlimint
#
# Released in Apr 2023
#
# For test environment only!
#
#
# Release notes
#
# NEW: Added basic fields validation, validation can be switched off in the settings
# NEW: Added possibility to set MTI map in GUI
# NEW: Warning when Specification was changed but not saved
#
# UPD: Updated requirements - framework changed to PyQt6, SvTerminal does not support PyQt5 since v0.15
# UPD: Specification for any fields now required
# UPD: Separated SvTerminal library, GUI runs as a specific implementation of the library
# UPD: New section [CONFIG] was added in ini transaction files. Two options available - MAX_AMOUNT and GENERATE_FIELDS
#      See updated ini file example in /sv-terminal/messages/ini/example.ini
#
# FIX: Fixed incorrect field name in INI files
# FIX: Optimized work with bitmap in GUI
# FIX: Fixed small bugs inherited from v0.14
# FIX: Code and project structure optimization
#

import common.sv_terminal
