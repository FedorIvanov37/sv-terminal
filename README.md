# SmartVista Electronic Commerce Terminal

![image](https://camo.githubusercontent.com/568a4f77e5187cca9e602fb8e108ea3f4b44884c7f3010abe2db2b6d5a12f105/68747470733a2f2f692e696d6775722e636f6d2f5378656e4d55512e706e67)

SmartVista Electronic Commerce Terminal | v0.16 Nov 2023 | Powered by <a href="https://www.unlimit.com">Unlimit</a></p>

# Contents 

* [Description](#description)
  * [SvTerminal overview](#svterminal-overview)
  * [Important notes](#important-notes)
  * [Release info](#release-info)

 
* [Graphic User Interface](#graphic-user-interface)
  * [GUI overview](#gui-overview)
  * [Main Window hotkeys](#main-window-hotkeys)


* [Modules package](#modules-package)
  * [Library overview](#library-overview)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Modules usage](#modules-usage)
    * [Intro](#modules-intro)
    * [What's inside](#what-is-inside)
    * [Usage example](#usage-example)


* [Author](#author) 

# Description

## SvTerminal Overview

SV-Terminal simplifies sending of banking card e-commerce transactions to SmartVista using a useful visual interface 
making simple things simple to achieve

The Terminal uses ISO-8583 E-pay protocol for transactions sending, instead of PSP. It can be used during the Payment 
Systems certification test, for checking and setting up the system on the test environment, during the application 
development process, and so on

Also, the Terminal builds like a kit of weakly connected modules like a Parser, Connector, Queue, etc. It allows to 
reuse or extend the Terminal's functionality making emulators, loaders, parsers, converters, application interfaces, 
and many other things based on SV-Terminal modules

[UBC SV API](http://feapi.unlimint.io:7171/documentation) is a good example of using SvTerminal modules without any GUI 
  
SV-Terminal is not an emulator of PSP or SmartVista. It doesn't try to be similar to these systems. It is more 
positioned as a simplified version card payment terminal, developed with respect for the everyday needs of the Card 
Processing Support Team

Written on Python 3.10 with using of PyQt6 and pydantic packages


In case of any questions about SvTerminal [contact author](#author). Your feedback and suggestions are general drivers 
of SvTerminal evolution.

## ⚠️ Important notes  

* Allowed usage on test environment only. SvTerminal only implements basic security checks
* Since v0.15 SvTerminal library doesn't support PyQt5 anymore
* At the moment SvTerminal doesn't support byte-fields
* Logfile rotation included in the build. SvTerminal stores 10 logfiles by 10M each



## Release info

* New features
  * Secret fields can be hidden in logs and transaction constructor
  * Transactions repeat loop
  * Main Window search line 
  * Spec Window search line
  * Pydantic native data validation


* Updates
  * User doc update: main settings, the specification, files format, and many other things are reflected in the document
  * Default message corrected according to mandatory changes 23Q4

  
* Fixed
  * All problems around old JSON files incompatibility  
  * Transaction field max_amount has no effect
  * Code optimization, minor bug fixes
  

# Graphic User Interface

## GUI overview

⚠️Only Windows x64 build exists. Use the source code to run SvTerminal on another platform. Tests were done on 
Windows 10-11 only

SvTerminal GUI is a friendly interface, based on the SvTerminal library. Since v0.15 SvTerminal GUI is released as a 
binary `.exe` file. No dependencies need to run the SvTerminal, it is ready to use from the box. No installation or 
settings are needed to run GUI on a Windows machine. Run "sv_terminal.exe" executable file for start the SvTerminal

Check the parameters, opened by the "Configuration" button to make your settings  

![image](https://i.imgur.com/1BFr77N.png)

## Main Window hotkeys

The list of key sequence and corresponding actions 

| Key sequence         | Action                    |
|----------------------|---------------------------|
| F1                   | About SvTerminal          |
| Ctrl + Enter         | Send transaction          |
| Ctrl + Shift + Enter | Reverse last transaction  |
| Ctrl + Alt + Enter   | Send Echo-Test            |
| Ctrl + N             | Add new field             |
| Ctrl + Shift + N     | Add new subfield          |
| Delete               | Remove field              |
| Ctrl + E             | Edit current field data   |
| Ctrl + W             | Edit current field number |
| Ctrl + R             | Reconnect SV              |
| Ctrl + L             | Clear log                 |
| Ctrl + O             | Open transaction file     |
| Ctrl + S             | Save transaction to file  |
| Ctrl + P             | Print transaction         |
| Ctrl + T             | Print SV Terminal logo    |
| Ctrl + Alt + Q       | Quit SV Terminal          |

## Specification settings

### Specification Overview 

This chapter describes the specification settings and maintenance. Refer to SVFE E-pay specification for more info.

The Specification is a root data structure, describing data processing mechanics, such as fields hierarchy, types, 
validation, and other things. SvTerminal needs the correct settings in the Specification for regular work. From v0.15 
specification settings are required for transaction processing.

The specification can be set using the button "Specification" of MainWindow. Settings through GUI are highly recommended 
by the author. 


### Settings description

![image](https://i.imgur.com/ICXUWD8.png)

The table below describes the settings window columns from left to right

| Field       | Purpose                                                                  | Used to                                                      | Type                       | Mandatory |
|-------------|--------------------------------------------------------------------------|--------------------------------------------------------------|----------------------------|-----------|
| Field       | The field or subfield number                                             | Define main fields structure, describe fields nesting        | Number in range 1-128      | Yes       |
| Description | Free text field purpose explanation                                      | Show field description on MainWindow transaction constructor | Text, no min or max length | No        |
| Min Len     | Field value minimum length                                               | Fields validation during data processing                     | Number, min value is 1     | Yes       |
| Max Len     | Field value maximum length                                               | Fields validation during data processing                     | Number, min value is 1     | Yes       | 
| Data Len    | How many numbers describes the (sub)field own length. E.g. for F2 (PAN)  |                                                              |                            |           |
|             |                                                                          |                                                              |                            |           |
|             |                                                                          |                                                              |                            |           |
|             |                                                                          |                                                              |                            |           |
|             |                                                                          |                                                              |                            |           |
|             |                                                                          |                                                              |                            |           |



## Transaction data files format


### Overview

The SvTerminal supports multiple representations of transaction-data files. The data can be put to the Terminal using 
one of three formats - `JSON`, `INI`, and `DUMP`. The data is stored in text files, which can be read or written 
by SvTerminal. This chapter describes each format's features and purpose

### The data formats description 

| Format | File extension | Incoming  | Outgoing | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|--------|----------------|-----------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| JSON   | `.json`        | Yes       | Yes      | Equally well suited for operator reading and machine analysis. The main goal is to make complex fields not so complicated, through structure-readable decomposition. Fields and subfields lengths are left out because they will be calculated later according to the Specification. All the transactions, incoming and outgoing stored in memory in JSON representation. Strictly requires Specification settings for each subfield                                                              | 
| INI    | `.ini`         | Yes       | Yes      | Flat format, where each field is written in one string. Fields fill in Tag-Length-Value (TLV) style with no separators. All the lengths have to be calculated and set by the operator. The format skips the data validation process. Recommended when you definitely understand what you do. Requires specification for top-level fields only, subfields specification is not required                                                                                                            | 
| DUMP   | `.txt`         | Yes       | Yes      | Raw SV-dump format. Used for loading and generating SVFE-compatible dump messages for parsing incoming and generating outgoing SV messages. Low-level data exchange with SVFE makes using this format. The DUMP is the fully ready-read message for the SVFE epayint module. For the sv-dump building recommended set fields data through the transaction constructor using JSON or INI style, then generating the dump by SvTerminal interface. Manual analysis or generation is not recommended | 

### Loading to the SvTerminal

To read the incoming data file in the open SvTerminal window press `CTRL + O`, or hit the button "Parse file" on the 
MainWindow bottom, then choose the file using the file-navigation window. SvTerminal recognizes the incoming file format 
by file extension. When the extension is absent or unknown the Terminal will try to parse the file using each format 
pattern one by one. Better to set correct extension for each format. Refer to the
[data formats description](#the-data-formats-description) to define correct extension for each file format

-*-*-*-GIF-*-*-*-*-*




# Modules package

## Library overview 

For using SvTerminal modules installation is required. Also, check the [Requirements](#requirements) chapter of 
this document 

Go to the program directory, then follow to `common/source/common/lib` directory to get access to the SvTerminal's 
library 


## Requirements 

These dependencies should be installed in case of library usage only. GUI delivers as a `.exe` build, without neediness 
install any dependencies 
 
* [Python 3.10+](https://www.python.org/)
* [PyQt6](https://www.qt.io/product/qt6)
* [pydantic](https://docs.pydantic.dev/)

## Installation
For using SvTerminal's library you have to install Python 3.10 or above and run the following command in the program 
directory

All dependencies can be installed by a single command in SvTerminal's directory 

```
pip install -r requirements.txt
```

## Modules usage 

### Modules Intro
SvTerminal is a group of independent modules, connected by PyQt6 Signal / Slot mechanism. You can use the SvTerminal 
modules package for your own project or when GUI running is impossible. This section provided a quick introduction, at 
the moment library's documentation is in the development stage

Don't forget to install the [requirements](#requirements) before using SvTerminal's package

### What is inside

The table describes fundamental system objects. In fact, SvTerminal contains much more modules for achieving the result. 
At the moment the only way to be familiar with the whole package is through code investigation 

| Module        | Purpose                                                                                                                                                                             |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SvTerminal    | The core implementation of low-level SvTerminal functions. Ready to use out of the box. In the general case, this module should be a low-level entry point                          |
| Parser        | Generates and parses files and data sets. Oriented on ISO8583 specification                                                                                                         |
| Generator     | Generates specific field values according to ISO8583 specification                                                                                                                  |
| TransQueue    | Low-level transaction queue. Uses the FIFO principle with access possibility of arbitrary data access. Stores the transactions objects and controls and match transactions messages |
| Connector     | TCP-connection socket interface                                                                                                                                                     |
| Transaction   | Pydantic data model contains transaction fields and additional transaction info. All internal data exchange should be made with the Transaction objects                             |
| Config        | Pydantic data model contains configuration parameters set                                                                                                                           |
 | Logger        | Log writer, Stores settings and manages Python's logging module                                                                                                                     |      

![image](https://camo.githubusercontent.com/dccafcb932d549e921b2adb6d56d1bc521c51e2bc8e0f4be5fbaade5c7fef22f/68747470733a2f2f692e696d6775722e636f6d2f75444a334b78352e706e67)

## Usage example
In this case, we'll see the general usage of the SvTerminal library. The example below is ready to start out of the box, 
without any changes. 

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
from common.lib.core.Terminal import SvTerminal
from common.lib.data_models.Transaction import Transaction
from common.lib.constants.TermFilesPath import TermFilesPath

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

Building own solution, using SvTerminal's modules library:

1. Import SvTerminal's library toolkit
2. Create the Config object using Pydantic's parser
3. Create the Transaction object using Pydantic's parser
4. Construct the logical data conveyor with transactions files on one side and SmartVista on another
5. Run the conveyor, sending the transactions to SV

```python
from multiprocessing import Process
from common.lib.data_models.Config import Config
from common.lib.core.Terminal import SvTerminal
from common.lib.data_models.Transaction import Transaction
from common.lib.constants.TermFilesPath import TermFilesPath

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

## Author

Designed and developed by Fedor Ivanov   

In case of any question contract [f.ivanov@unlimit.com](mailto:f.ivanov@unlimit.com?subject=SvTerminal%27s%20user%20request&body=Dear%20Fedor%2C%0A%0A%0A%3E%20Put%20your%20request%20here%20%3C%20%0A%0A%0A%0AMy%20SvTerminal%20version%20is%20v0.16%20%7C%20Released%20in%20Dec%202023%0A)
