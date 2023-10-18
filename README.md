# Simplified ISO generation algorithm

```
  ::::::::  :::::::::::  ::::::::   ::::    :::      :::      :::
 :+:    :+:     :+:     :+:    :+:  :+:+:   :+:    :+: :+:    :+:        
 +:+            +:+     +:+         :+:+:+  +:+   +:+   +:+   +:+        
 +#++:++#++     +#+     :#:         +#+ +:+ +#+  +#++:++#++:  +#+        
        +#+     +#+     +#+   +#+#  +#+  +#+#+#  +#+     +#+  +#+        
 #+#    #+#     #+#     #+#    #+#  #+#   #+#+#  #+#     #+#  #+#        
  ########  ###########  ########   ###    ####  ###     ###  ########## 
                                                                                                                      
 Simplified ISO generation algorithm | v0.16 Oct 2023
```


# Contents 

* [Description](#description)
  * [SIGNAL overview](#signal-overview)
  * [Important notes](#important-notes)
  * [Release info](#release-info)

 
* [Graphic User Interface](#graphic-user-interface)
  * [GUI overview](#gui-overview)
  * [Main Window hotkeys](#main-window-hotkeys)
  * [Specification settings](#specification-settings)
    * [Specification Overview](#specification-overview) 
    * [Settings description](#settings-description)
  * [Transaction data files format](#transaction-data-files-format)
    * [Overview](#overview)
    * [The data formats description](#the-data-formats-description)
    * [Loading to the SIGNAL](#loading-to-the-signal)
    * [Save transaction to file](#save-transaction-to-file)


* [Author](#author) 

# Description

## SIGNAL Overview

SIGNAL simplifies sending of banking card e-commerce transactions to banking card processing systems using a useful 
visual interface making simple things simple to achieve

The SIGNAL uses ISO-8583 E-pay protocol for transactions sending, instead of PSP. It can be used during the Payment 
Systems certification test, for checking and setting up the system on the test environment, during the application 
development process, and so on

Also, the SIGNAL builds like a kit of weakly connected modules like a Parser, Connector, Queue, etc. It allows to 
reuse or extend the SIGNAL's functionality making emulators, loaders, parsers, converters, application interfaces, 
and many other things based on SIGNAL modules

[UBC SV API](http://feapi.unlimint.io:7171/documentation) is a good example of using SIGNAL modules without any GUI 
  
SIGNAL is not an emulator of PSP or SmartVista. It doesn't try to be similar to these systems. It is more 
positioned as a simplified version card payment terminal, developed with respect for the everyday needs of the Card 
Processing Support Team

Written on Python 3.10 with using of PyQt6 and pydantic packages


In case of any questions about SIGNAL [contact author](#author). Your feedback and suggestions are general drivers 
of SIGNAL evolution.

## Important notes  

* Allowed usage on test environment only. SIGNAL only implements basic security checks
* At the moment SIGNAL doesn't support byte-fields
* Logfile rotation included in the build. SIGNAL stores 10 logfiles by 10M each


## Release info

* New features
  * Need to accept the license agreement on first run  
  * Transactions repeat loop button
  * Main / Spec Window search line, key sequence 
  * Incoming message header length settings 
  * Button "Set default" in settings window
  * Command "Set reversal fields" in Reversal button menu


* Updates
  * Changed name to SIGNAL
  * Hiding of secrets in logs and transaction constructor now possible for every field
  * Simplified JSON mode, work without specification
  * Default message corrected according to mandatory changes 23Q4
  * Lines wrap on log display 
  * Many small useful updates such as
    * Improved checkboxes
    * Instant field length counting
    * Tag Length cascading
    * Lines wrap on log display
    * Predefined max amounts
  

* Fixed
  * All problems around old JSON files incompatibility  
  * Transaction field max_amount has no effect
  * SIGNAL fall down in some cases of fields validation
  * Code optimization, minor bug fixes
  

# Graphic User Interface

## GUI overview

⚠️Only Windows x64 build exists. Use the source code to run SIGNAL on another platform. Tests were done on 
Windows 10-11 only

SIGNAL GUI is a friendly interface, based on the SIGNAL library. Since v0.15 SIGNAL GUI is released as a 
binary `.exe` file. No dependencies need to run the SIGNAL, it is ready to use from the box. No installation or 
settings are needed to run SIGNAL GUI on a Windows machine. Run `signal.exe` executable file for start the SIGNAL

Check the parameters, opened by the "Configuration" button to make your settings  

![image](https://i.imgur.com/7kZuHsR.png)

## Main Window hotkeys

The list of key sequence and corresponding actions 

| Key sequence          | Action                    |
|-----------------------|---------------------------|
| F1                    | About SIGNAL              |
| Ctrl + Enter          | Send transaction          |
| Ctrl + Shift + Enter  | Reverse last transaction  |
| Ctrl + Alt + Enter    | Send Echo-Test            |
| Ctrl + N              | Add new field             |
| Ctrl + N              | Add new field             |
| Ctrl + Shift + N      | Add new subfield          |
| Ctrl + F              | Search                    |
| Delete                | Remove field              |
| Ctrl + E              | Edit current field data   |
| Ctrl + W              | Edit current field number |
| Ctrl + R              | Reconnect to host         |
| Ctrl + L              | Clear log                 |
| Ctrl + O              | Open transaction file     |
| Ctrl + S              | Save transaction to file  |
| Ctrl + P              | Print transaction         |
| Ctrl + T              | Print SIGNAL logo         |
| Ctrl + Alt + Q        | Quit SIGNAL               |

## Specification settings

### Specification Overview 

This chapter describes the specification settings and maintenance. Refer to SVFE E-pay specification for more info.

The Specification is a root data structure, describing data processing mechanics, such as fields hierarchy, types, 
validation, and other things. SIGNAL needs the correct settings in the Specification for regular work. From v0.15 
specification settings are required for transaction processing.

The specification can be set using the button "Specification" of MainWindow. Settings through GUI are highly recommended 
by the author. 


### Settings description

![image](https://i.imgur.com/DZOImP4.png)

The table below describes the settings window columns from left to right

| Field       | Purpose                                                                                                                                                                                                                                                | Used to                                                      | Type                       | Mandatory    |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|----------------------------|--------------|
| Field       | The field or subfield number                                                                                                                                                                                                                           | Define main fields structure, describe fields nesting        | Number                     | Yes          |
| Description | Free text field purpose explanation                                                                                                                                                                                                                    | Show field description on MainWindow transaction constructor | Text, no min or max length | No           |
| Min Len     | Field value minimum length                                                                                                                                                                                                                             | Fields validation during data processing                     | Number, min value is 1     | Yes          |
| Max Len     | Field value maximum length                                                                                                                                                                                                                             | Fields validation during data processing                     | Number, min value is 1     | Yes          | 
| Data Len    | Applicable for variable-length fields. How many numbers marks the field own length. Should ba take from E-pay specification document. In the specification usually marks as `LLVAR` - 2 digits, `LLLVAR` - 3 digits, and so on                         | Message construction, Fields validation, Message parsing     | Number, min value is 0     | Yes          |
| Tag Len     | For complex fields only (field should contain subfields). How many numbers marks each subfield length. In the specification usually marks as `LLVAR` - 2 digits, `LLLVAR` - 3 digits, and so on. Tag Len of field should equal to field's own Data Len | Message construction, Fields validation, Message parsing     | Number, min value is 0     | Yes          |
| Alpha       | Are the alphabetic letters allowed in this field                                                                                                                                                                                                       | Fields validation                                            | Checkbox                   | Yes          |
| Numeric     | Are the digits  allowed in this field                                                                                                                                                                                                                  | Fields validation                                            | Checkbox                   | Yes          |
| Special     | Are the special characters allowed in this field                                                                                                                                                                                                       | Fields validation                                            | Checkbox                   | Yes          |
| Matching    | If yes the field will be used for matching requests and responses. It means SIGNAL, sending the transaction expects the same field value in the SV response                                                                                            | Message matching                                             | Checkbox                   | Yes          |
| Reversal    | When Yes then the field value will be taken from the original message and put to the reversal in case of reversal                                                                                                                                      | Message matching, message construction                       | Checkbox                   | Yes          |
| Generated   | Can the fields be auto-generated by SIGNAL before sending? If yes then the corresponding checkbox appears in Main Window¹                                                                                                                              | Message construction                                         | Checkbox                   | Yes          |
| Secret      | If yes field value will be hidden in the log, transaction constructor, and on MainWindow display³                                                                                                                                                      | Display data, log writing                                    | Checkbox                   | Yes          |

¹ Currently, SIGNAL supports randomly generated field values only. No date-time and other specific format are supported, except pre-defined fields 7 and 11

² Due to security reasons, it is impossible to set Primary Account Number (Field 2) as non-secret. The field has a non-removable "secret" mark  

## Transaction data files format


### Overview

The SIGNAL supports multiple representations of transaction-data files. The data can be put to the SIGNAL using 
one of three formats - `JSON`, `INI`, and `DUMP`. The data is stored in text files, which can be read or written 
by SIGNAL. This chapter describes each format's features and purpose

### The data formats description 

| Format | File extension | Incoming  | Outgoing | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------|----------------|-----------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| JSON   | `.json`        | Yes       | Yes      | Equally well suited for operator reading and machine analysis. The main goal is to make complex fields not so complicated, through structure-readable decomposition. Fields and subfields lengths are left out because they will be calculated later according to the Specification. All the transactions, incoming and outgoing stored in memory in JSON representation. Strictly requires Specification settings for each subfield                                                          | 
| INI    | `.ini`         | Yes       | Yes      | Flat format, where each field is written in one string. Fields fill in Tag-Length-Value (TLV) style with no separators. All the lengths have to be calculated and set by the operator. The format skips the data validation process. Recommended when you definitely understand what you do. Requires specification for top-level fields only, subfields specification is not required                                                                                                        | 
| DUMP   | `.txt`         | Yes       | Yes      | Raw SV-dump format. Used for loading and generating SVFE-compatible dump messages for parsing incoming and generating outgoing SV messages. Low-level data exchange with SVFE makes using this format. The DUMP is the fully ready-read message for the SVFE epayint module. For the sv-dump building recommended set fields data through the transaction constructor using JSON or INI style, then generating the dump by SIGNAL interface. Manual analysis or generation is not recommended | 

### Loading to the SIGNAL

To read the incoming data file in the open SIGNAL window press `CTRL + O`, or hit the button "Parse file" on the 
MainWindow bottom, then choose the file using the file-navigation window. SIGNAL recognizes the incoming file format 
by file extension. When the extension is absent or unknown the SIGNAL will try to parse the file using each format 
pattern one by one. Better to set correct extension for each format. Refer to the
[data formats description](#the-data-formats-description) to define correct extension for each file format

### Save transaction to file

... 

## Author

Designed and developed by Fedor Ivanov   

In case of any question contract [fedornivanov@gmail.com](mailto:fedornivanov@gmail.com?subject=SIGNAL%27s%20user%20request&body=Dear%20Fedor%2C%0A%0A%0A%3E%20Put%20your%20request%20here%20%3C%20%0A%0A%0A%0AMy%20SIGNAL%20version%20is%20v0.16%20%7C%20Released%20in%20Oct%202023%0A)