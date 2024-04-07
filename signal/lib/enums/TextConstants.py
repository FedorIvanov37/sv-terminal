from enum import StrEnum
from signal.lib.enums.ReleaseDefinition import ReleaseDefinition
from signal.lib.enums.LicenseAgreement import LicenseAgreement


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
