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
# Author: Fedor Ivanov | Unlimit
#
# Released in Apr 2023
#
# For test environment only!
#
#
# Release notes
#
# NEW: Added fields basic validation, validation can be switched off in the settings
# NEW: Added transaction timeouts: in case of no response for 60 seconds transaction will be declined
# NEW: Added possibility to set MTI map in GUI. See specification window
# NEW: Added warning when Specification was changed but not saved
#
# UPD: Updated requirements - framework changed to PyQt6, SvTerminal does not support PyQt5 since v0.15
# UPD: Since v0.15 Specification settings are required for any fields
# UPD: SvTerminal library is separated, and the GUI runs as a specific implementation of the library
# UPD: Incoming JSON-files format simplified with backward compatibility respect
# UPD: New section [CONFIG] added in INI incoming files. Two options are available - MAX_AMOUNT and GENERATE_FIELDS
#
# FIX: Fixed incorrect field name in INI files
# FIX: Optimized work with bitmap in GUI
# FIX: Terminal fall down when empty field number set in Specification
# FIX: Fixed small todo-list.txt inherited from v0.14
# FIX: Code and project structure optimization
#

import common.sv_terminal
