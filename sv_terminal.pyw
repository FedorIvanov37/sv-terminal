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
# Version: v0.15 Production Beta
#
# Author: Fedor Ivanov | Unlimit
#
# Released in Jun 2023
#
# For test environment only!
#
#
# Release notes
#
# NEW: Added fields basic pre-validation, validation can be switched off by the settings
# NEW: Added transaction timeouts: in case of no response for 60 seconds operator will be notified
# NEW: Added possibility to set MTI map in GUI. See specification window
# NEW: Added warning when Specification was changed but not saved
# NEW: Added specification fields validation
#
# UPD: Updated requirements - framework changed to PyQt6, SvTerminal does not support PyQt5 since v0.15
# UPD: Since v0.15 Specification settings are required for any field
# UPD: SvTerminal library is separated, and the GUI runs as a specific implementation of the library
# UPD: Incoming JSON-files format simplified respecting the backward compatibility
# UPD: New section [CONFIG] added in INI incoming files. Two options are available - MAX_AMOUNT and GENERATE_FIELDS
# UPD: Hide card numbers in log and data field
# UPD: Added date to logfile. Log on display wasn't changed
# UPD: Renovation of the window "About"
#
# FIX: Fixed incorrect field name in INI files
# FIX: Optimized work with bitmap in GUI
# FIX: Terminal fall down when empty field number is set in Specification
# FIX: Fixed small bugs inherited from v0.14
# FIX: Code and project structure optimization such as separated log-handler, divided connection thread, etc
#

import common.sv_terminal
