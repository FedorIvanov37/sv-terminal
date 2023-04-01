  # SmartVista Electronic Commerce Terminal

```
  ::::::::  :::     ::: ::::::::::: :::::::::: :::::::::  ::::    ::::  ::::::::::: ::::    :::     :::     :::
 :+:    :+: :+:     :+:     :+:     :+:        :+:    :+: +:+:+: :+:+:+     :+:     :+:+:   :+:   :+: :+:   :+:
 +:+        +:+     +:+     +:+     +:+        +:+    +:+ +:+ +:+:+ +:+     +:+     :+:+:+  +:+  +:+   +:+  +:+
 +#++:++#++ +#+     +:+     +#+     +#++:++#   +#++:++#:  +#+  +:+  +#+     +#+     +#+ +:+ +#+ +#++:++#++: +#+
        +#+  +#+   +#+      +#+     +#+        +#+    +#+ +#+       +#+     +#+     +#+  +#+#+# +#+     +#+ +#+
 #+#    #+#   #+#+#+#       #+#     #+#        #+#    #+# #+#       #+#     #+#     #+#   #+#+# #+#     #+# #+#
  ########      ###         ###     ########## ###    ### ###       ### ########### ###    #### ###     ### ##########
  
 SmartVista Electronic Commerce Terminal v0.15 
```


Released in Apr 2023, under construction

## Description


SV-Terminal simplifies sending of banking card e-commerce transactions to SmartVista using a useful visual interface making simple things simple to achieve.

The Terminal uses ISO-8583 E-pay protocol for transactions sending, instead of PSP. It can be used during the Payment Systems certification test, for checking and setting up the system on the test environment, during the application development process, and so on.

Also, the Terminal builds like a kit of weakly connected modules like a Parser, Connector, Queue, etc. It allows to reuse or extend the Terminal's functionality making emulators, loaders, parsers, converters, application interfaces, and many other things based on SV-Terminal modules.

SV-Terminal is not an emulator of PSP or SmartVista. It doesn't try to be similar to these systems. It is more positioned as a simplified version card payment terminal, developed with respect for the everyday needs of the Card Processing Support Team.

Written on Python 3.10 with using of PyQt6 and pydantic packages


In case of any questions about SvTerminal [contact author](#author). Your feedback and suggestions are general drivers of SvTerminal evolution.

## User interface
![image](https://user-images.githubusercontent.com/116465333/197392351-dee7f5a0-1e27-4bf0-9356-3f412ebc3f29.png)


## Modules package


## Requirements 
 
* [Python 3.10+](https://www.python.org/)
* [PyQt6](https://www.qt.io/product/qt6)
* [pydantic](https://docs.pydantic.dev/)

## Installation
To begin, you have to install Python 3.10 or above and run the following command in the program directory. Then use double click on sv_terminal.pyw file for run SvTerminal UI

```
pip install -r requirements.txt
```

## Modules usage 

### Intro
SvTerminal is a group of independent modules, connected by PyQt6 Signal / Slot mechanism. You can use the SvTerminal modules package for your own project or when GUI running is impossible. This section provided a quick introduction, at the moment library's documentation is in the development stage.

In case of separated modules usage the [requirements](#requirements) staying the same

### What's inside

The table describes fundamental system objects. In fact, SvTerminal contains much more modules for achieving the result. At the moment the only way to be familiar with the whole package is through code investigation 

| Module      | Purpose                                                                                                                                                                              |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SvTerminal  | The core implementation of low-level SvTerminal functions. Ready to use out of the box. In the general case, this module should be a low-level entry point                           |
| Parser      | Generates and parses files and data sets. Oriented on ISO8583 specification                                                                                                          |
| Generator   | Generates specific field values according to ISO8583 specification                                                                                                                   |
| TransQueue  | Low-level transaction queue. Uses the FIFO principle with access possibility of arbitrary data access. Stores the transactions objects and controls and match transactions messages  |
| Connector   | TCP-connection socket interface                                                                                                                                                      |
| Transaction | Pydantic data model contains transaction fields and additional transaction info. All internal data exchange should be made with the Transaction objects                              |
| Config      | Pydantic data model contains configuration parameters set                                                                                                                            |


![image](https://camo.githubusercontent.com/dccafcb932d549e921b2adb6d56d1bc521c51e2bc8e0f4be5fbaade5c7fef22f/68747470733a2f2f692e696d6775722e636f6d2f75444a334b78352e706e67)

## Usage example
In this case, we'll see the general usage of the SvTerminal library. The example below is ready to start out of the box, without any changes. 

Using build SvTerminal object without separated modules. Same as user, but without UI:

1. Import SvTerminal's library toolkit 
2. Create the Config object using Pydantic's parser
3. Create the Transaction object using Pydantic's parser
4. Create the Terminal object
5. Run SvTerminal as separated process
6. Send the transaction using the terminal
7. Wait for the transaction response 
8. In case of success reverse the transaction 

```python
from multiprocessing import Process
from common.lib.data_models.Config import Config
from common.lib.Terminal import SvTerminal
from common.lib.data_models.Transaction import Transaction
from common.gui.constants.TermFilesPath import TermFilesPath


config: Config = Config.parse_file(TermFilesPath.CONFIG)
transaction: Transaction = Transaction.parse_file(TermFilesPath.DEFAULT_FILE)
terminal: SvTerminal = SvTerminal(config)

sv_terminal: Process = Process(target=terminal.run)
sv_terminal.run()

terminal.send(transaction)

for second in range(60):
    transaction: Transaction = terminal.get_transaction(transaction.trans_id)

    if transaction.matched:
        break

if not transaction.matched:  # SV Timeout
    exit(100)

print(transaction.json())

if transaction.success:
    terminal.reverse_transaction(transaction)

```

Building uwn solution, using SvTerminal's modules library:

1. Import SvTerminal's library toolkit
2. Create the Config object using Pydantic's parser
3. Create the Transaction object using Pydantic's parser
4. Construct the logical data conveyor with transactions files on one side and SmartVista on another
5. Run the conveyor, sending the transactions to SV 

```python
from multiprocessing import Process
from common.lib.data_models.Config import Config
from common.lib.Terminal import SvTerminal
from common.lib.data_models.Transaction import Transaction
from common.gui.constants.TermFilesPath import TermFilesPath


config: Config = Config.parse_file(TermFilesPath.CONFIG)
transaction: Transaction = Transaction.parse_file(TermFilesPath.DEFAULT_FILE)
terminal: SvTerminal = SvTerminal(config)

sv_terminal: Process = Process(target=terminal.run)
sv_terminal.run()

terminal.send(transaction)

for second in range(60):
    transaction: Transaction = terminal.get_transaction(transaction.trans_id)

    if transaction.matched:
        break

if not transaction.matched:  # SV Timeout
    exit(100)

print(transaction.json())

if transaction.success:
    terminal.reverse_transaction(transaction)
```

## What's new in v0.15

* NEW: Fields basic validation, validation can be switched off in the settings
* NEW: Transaction timeouts: in case of no response for 60 seconds transaction will be marked as timeout with a warning
* NEW: ISO8583 Message Type Indicators (MTI) setting window. Opens by the button "Set MTI" in the Specification window
* NEW: Small warning window in case when Specification was changed but not saved 
* NEW: Background music, play control button, and interactive contact link to the About window
* UPD: Framework changed to PyQt6, SvTerminal does not support PyQt5 since v0.15
* UPD: Since v0.15 Specification settings are required for any fields
* UPD: SvTerminal library is separated, and the GUI runs as a specific implementation of the library
* UPD: Incoming JSON-files format simplified with backward compatibility respect
* UPD: New section [CONFIG] added in INI incoming files. Two options are available - MAX_AMOUNT and GENERATE_FIELDS
* FIX: No freeze GUI while opening the connection. The Connector moved to its own thread, separated from the event loop
* FIX: Incorrect field names in INI files
* FIX: Terminal fall down when empty field number set in Specification
* FIX: Small bugs inherited from v0.14
* FIX: Code and project structure optimization

## ⚠️ Important notes  

* Allowed usage on test environment only. SvTerminal only implements basic security checks
* Since v0.15 SvTerminal doesn't support PyQt5 anymore
* At the moment SvTerminal doesn't support byte-fields
* Logfile rotation included in the build. SvTerminal stores 10 logfiles by 10M each
* The author is always open for comments, advice, code review, suggestions, etc. Feel free to ask any questions directly 

## Author

Designed and developed by [Fedor Ivanov](mailto:f.ivanov@unlimint.com)
