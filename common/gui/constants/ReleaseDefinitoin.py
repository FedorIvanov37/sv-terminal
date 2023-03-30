from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseDefinition(object):
    AUTHOR = "Fedor Ivanov | Unlimint"
    VERSION = "v0.15"
    CONTACT = "f.ivanov@unlimint.com"
    RELEASE = "Jul 2022"
    RELEASE_NOTES: str = """# For test environment only!
#
#
# Release notes
#
# NEW: New setting - Send internal SVTerminal transaction ID to SV. Can be switched off using Setting Window 
# NEW: New Setting - Build Original Data Elements (Field 90) in Reversal. Can be switched off using Setting Window
# NEW: Saving log to file - all output will be saved in logfile common/log/sv_terminal.log
# NEW: Logfiles rotation - SVTerminal stores 10 last logfiles by 10M each
# NEW: New button "Set MTI" in Spec Window - MTI should be set manually in Spec
# NEW: New button "Pasre File"  in Spec Window - allows to parse external Specification JSON file saved by SVTerminal
# NEW: Read only mode in Specification Window. Switched on by default 
#
# UPD: Dependency optimization - SVTerminal now has two dependencies only - PyQt5 and Pydantic  
# UPD: IDs in log - Internal SVTerminal transaction ID and SV Utrnno are now in the log for each message when existing 
# UPD: SV Utrnno added to Reversal Window
# UPD: Output and Main Window optimization oriented on single screen separation in Microsoft Windows 
# UPD: Print Button Menu updated - now operator can also print Specification and SVTerminal text-logo  
#
# FIX: Main Window freeze while SVTerminal connecting
# FIX: Fix bugs inherited from v0.13 
# FIX: Code optimization by Pydantic toolkit
#
"""
