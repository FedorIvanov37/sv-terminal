from enum import StrEnum
from common.lib.enums.ReleaseDefinition import ReleaseDefinition
from common.lib.enums.LicenseAgreement import LicenseAgreement


class TextConstants(StrEnum):
    SYSTEM_NAME = "SIGNAL"

    HELLO_MESSAGE = f"""
  ::::::::  :::::::::::  ::::::::   ::::    :::      :::      :::        
 :+:    :+:     :+:     :+:    :+:  :+:+:   :+:    :+: :+:    :+:        
 +:+            +:+     +:+         :+:+:+  +:+   +:+   +:+   +:+        
 +#++:++#++     +#+     :#:         +#+ +:+ +#+  +#++:++#++:  +#+        
        +#+     +#+     +#+   +#+#  +#+  +#+#+#  +#+     +#+  +#+        
 #+#    #+#     #+#     #+#    #+#  #+#   #+#+#  #+#     #+#  #+#        
  ########  ###########  ########   ###    ####  ###     ###  ########## 

  Simplified ISO generation algorithm {ReleaseDefinition.VERSION}"""

    LICENSE_AGREEMENT = LicenseAgreement.AGREEMENT
