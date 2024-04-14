# Simplified ISO generation algorithm

```
  ::::::::  :::::::::::  ::::::::   ::::    :::      :::      :::
 :+:    :+:     :+:     :+:    :+:  :+:+:   :+:    :+: :+:    :+:        
 +:+            +:+     +:+         :+:+:+  +:+   +:+   +:+   +:+        
 +#++:++#++     +#+     :#:         +#+ +:+ +#+  +#++:++#++:  +#+        
        +#+     +#+     +#+   +#+#  +#+  +#+#+#  +#+     +#+  +#+        
 #+#    #+#     #+#     #+#    #+#  #+#   #+#+#  #+#     #+#  #+#        
  ########  ###########  ########   ###    ####  ###     ###  ########## 
                                                                                                                      
 Simplified ISO generation algorithm | v0.18 Apr 2024
```


# Contents 

* [SIGNAL](#signal)
  * [SIGNAL general overview](#signal-general-overview)
  * [Important notes](#important-notes)
  * [Release info](#release-info)
  
 
* [Graphic User Interface](#graphic-user-interface)
  * [GUI overview](#gui-overview)
  * [Main Window]
  * [Windows hotkeys](#windows-hotkeys)
  * [GUI Tools]
    * [Complex fields parser]
    * [Reversal]
    * [Transactions auto-repeat]
    * [Search line]
    * [Print data]
    * [Fields generators]
    * [Secret features]  


* [Command Line Interface](#command-line-interface)
  * [CLI usage](#cli-usage)
  * [CLI examples](#cli-examples)


* [Library re-usage]
  * [Requirements]
  * [Library installation]
  * [Modules purpose]
  * [Modules usage example]
  * [Compilation of executable binary]
  * [Recommendations]
  

 * [Specification settings](#specification-settings)
   * [Specification Overview](#specification-overview) 
   * [Settings description](#settings-description)
   * [MTI setting]
   * [Fields extended parameters]
   * [Remote specification](#remote-specification)
   * [Remote specification endpoint setting](#remote-specification-endpoint-setting)
  

* [Fields validation]
  * [Main validation]
  * [Extended validation]
  * [Violation mode]
  * [Directions]
  * [Complex fields flat / JSON representation]
  * [Manual entry mode]


* [Configuration]
  * [Config overview]
  * [Config file]
  * [Settings] 
    * [Remote host]
    * [Specification]
    * [On startup]
    * [Log]
    * [Validation]
    * [Fields]
   
 
 * [Transaction data files](#transaction-data-files)
   * [Overview](#overview)
   * [The data formats description](#the-data-formats-description)
   * [Loading to the SIGNAL](#loading-to-the-signal)
   * [Save transaction to file](#save-transaction-to-file)

 
* [Logging]
  * [Log levels]
  * [Storage and rotation]
  * [Hide secrets]
   

* [Bugs]
  * [List of known bugs]


* [About](#about)
  * [Concept and design] 
  * [License](#license)
  * [Resources]
  * [Author](#author)
  
# SIGNAL

## SIGNAL general overview

SIGNAL simplifies the sending of banking card e-commerce transactions to banking card processing systems using a useful 
visual and program interface making simple things simple to achieve

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

Written on Python 3.12 with the use of PyQt6 and Pydantic packages


In case of any questions about SIGNAL [contact the author](#author). Your feedback and suggestions are general drivers 
of SIGNAL evolution.

## Important notes

* Allowed usage on test environment only. SIGNAL only implements basic security checks
* At the moment SIGNAL doesn't support byte-fields
* GUI tests were made on Windows 10/11 x64 only

[//]: # (* Logfile rotation included in the build. SIGNAL stores 10 logfiles by 10M each)


## Release info

* New features
  * Remote Specification in Settings and SpecWindow. See [Remote specification](#remote-specification)
  * Log screen on SpecWindow 
  * Complex fields conductor
  * Fields validation button and key sequence
  * Extended validation settings window
  * Validation violation processing modes
  

* Updates
  * JSON constructors color scheme optimization 
  * Added key sequences on SpecWindow
  * SpecWindow checkboxes are protected in read-only mode
  * Spec backup storage depth
  * Added config.json to the "Print" menu
  * SettingsWindow form optimization
  * Manual setting of logfiles backup storage depth
  * Transaction ID "Generate" checkbox


* Fixed
  * Small code optimization
  * JSON mode by default
  

# Graphic User Interface

## GUI overview

⚠️Only Windows x64 build exists. Use the source code to run SIGNAL on another platform. Tests were done on 
Windows 10-11 only

SIGNAL GUI is a friendly interface, based on the SIGNAL library. Since v0.15 SIGNAL GUI is released as a 
binary `.exe` file. No dependencies need to run the SIGNAL, it is ready to use from the box. No installation or 
settings are needed to run SIGNAL GUI on a Windows machine. Run the `signal.exe` executable file to start the SIGNAL

Check the parameters, opened by the "Configuration" button to make your settings  

![image](https://i.imgur.com/Pj49PG1.png)

## Windows hotkeys

The list of key sequences and corresponding actions 

| Key sequence         | MainWindow                | SpecWindow                       |
|----------------------|---------------------------|----------------------------------|
| F1                   | About SIGNAL              | -                                |
| Ctrl + Enter         | Send transaction          | -                                |
| Ctrl + Shift + Enter | Reverse last transaction  | -                                |
| Ctrl + Alt + Enter   | Send Echo-Test            | -                                |
| Ctrl + N             | Add new field             | Add new field                    |
| Ctrl + Shift + N     | Add new subfield          | Add new subfield                 |
| Ctrl + Shift + V     | Validate current message  | -                                |
| Ctrl + F             | Search                    | Search                           |
| Delete               | Remove field              | Remove field                     |
| Ctrl + E             | Edit current field data   | Edit current field description   |
| Ctrl + W             | Edit current field number | Edit current field number        |
| Ctrl + R             | Reconnect to host         | -                                |
| Ctrl + L             | Clear log                 | Clear log                        |
| Ctrl + O             | Open transaction file     | Open specification file          |
| Ctrl + S             | Save transaction to file  | Backup current specification     |
| Ctrl + P             | Print transaction         | -                                |
| Ctrl + T             | Open new tab              | -                                |
| Ctrl + F4            | Close current tab         | -                                |
| Ctrl + PgUp / PgDown | Tabs navigation           | -                                |
| Ctrl + Alt + Q       | Quit SIGNAL               | -                                |


# Command Line Interface
By usage of a specific flag `-c` or `--console` the SIGNAL can be run in Command Line Interface mode (CLI). In CLI mode GUI will not be run, all the output will be placed in the command line instead. CLI mode is useful when some external tool or script needs to send a transaction without the usage of GUI 

The console-mode flag `-c` or `--console` is required to run CLI mode (see [examples](#cli-examples)). In case of absence console-mode flags GUI mode will be run by default

Flag `-h` or `--help` does not require console-mode flags

## CLI Usage

To see usage hint call `signal.exe --help`

```text
usage: signal.exe [-h] -c [-f FILE] [-d DIR] [-a ADDRESS] [-p PORT] [-r] [-l LOG_LEVEL] [-i INTERVAL] [--parallel] [-t TIMEOUT] [--about] [-e] [--default] [-v] [--config]

SIGNAL v0.18

options:
  -h, --help            show this help message and exit
  -c, --console         Run SIGNAL in Command Line Interface mode
  -f FILE, --file FILE  File or file-mask to parse
  -d DIR, --dir DIR     Directory with files to parse. SIGNAL will try all of the files from the directory
  -a ADDRESS, --address ADDRESS
                        Host TCP/IP address
  -p PORT, --port PORT  TCP/IP port to connect
  -r, --repeat          Repeat transactions after sending
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Debug level DEBUG, INFO, etc
  -i INTERVAL, --interval INTERVAL
                        Wait (seconds) before send next transaction
  --parallel            Send new transaction with no waiting of answer for previous one
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout of waiting resp
  --about               Show info about the SIGNAL
  -e, --echo-test       Send echo-test
  --default             Send default transaction message
  -v, --version         Print current version of SIGNAL
  --config              Print configuration parameters
```

## CLI examples
| Command                                                      | Action                                                                                    | 
|--------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `signal.exe --console --default`                             | Send default transaction to the host                                                      |
| `signal.exe --console --echo-test`                           | Send echo-test to the host                                                                |
| `signal.exe --console --about`                               | Show info about the SIGNAL                                                                |
| `signal.exe --console --file /transactions/transaction.json` | Parse specific file `/transactions/transaction.json` and send the transaction to the host |
| `signal.exe --console --default --repeat --interval 2`       | Begin transaction loop, sending new transaction every 2 sec                               |
| `signal.exe --console --dir /transactions --parallel`        | Immediate send all the transactions from the directory /transactions                      |

```text
PS C:\signal> signal.exe --about
02:57:15 [INFO] 
02:57:15 [INFO]   ::::::::  :::::::::::  ::::::::   ::::    :::      :::      :::        
02:57:15 [INFO]  :+:    :+:     :+:     :+:    :+:  :+:+:   :+:    :+: :+:    :+:        
02:57:15 [INFO]  +:+            +:+     +:+         :+:+:+  +:+   +:+   +:+   +:+        
02:57:15 [INFO]  +#++:++#++     +#+     :#:         +#+ +:+ +#+  +#++:++#++:  +#+        
02:57:15 [INFO]         +#+     +#+     +#+   +#+#  +#+  +#+#+#  +#+     +#+  +#+        
02:57:15 [INFO]  #+#    #+#     #+#     #+#    #+#  #+#   #+#+#  #+#     #+#  #+#        
02:57:15 [INFO]   ########  ###########  ########   ###    ####  ###     ###  ########## 
02:57:15 [INFO] 
02:57:15 [INFO]   Simplified ISO generation algorithm v0.18
02:57:15 [INFO] 
02:57:15 [INFO]   Use only on test environment
02:57:15 [INFO] 
02:57:15 [INFO]   Version v0.18
02:57:15 [INFO] 
02:57:15 [INFO]   Released in Apr 2024
02:57:15 [INFO] 
02:57:15 [INFO]   Developed by Fedor Ivanov
02:57:15 [INFO] 
02:57:15 [INFO]   Contact fedornivanov@gmail.com
02:57:15 [INFO]
```

```text
PS C:\signal> signal.exe --console --echo-test 
03:05:12 [INFO] ## Running SIGNAL in Console mode ##
03:05:12 [INFO] Press CTRL+C to exit
03:05:12 [INFO] 
03:05:12 [INFO] 
03:05:12 [INFO] Processing file echo-test.json
03:05:12 [WARNING] Host disconnected. Trying to establish the connection
03:05:12 [INFO] Connection ESTABLISHED
03:05:12 [INFO] 
03:05:12 [INFO] [TRANS_ID][20240414_030512_8695314843]
03:05:12 [INFO] [MSG_TYPE][0800]
03:05:12 [INFO] [BITMAP  ][7, 11, 70]
03:05:12 [INFO] [007][010][0414030512]
03:05:12 [INFO] [011][006][615012]
03:05:12 [INFO] [070][003][301]
03:05:12 [INFO] 
03:05:12 [INFO] Outgoing transaction ID [20240414_030512_8695314843] sent
03:05:13 [INFO] Incoming transaction ID [20240414_030512_8695314843] received
03:05:13 [INFO]
03:05:13 [INFO] [TRANS_ID][20240414_030512_8695314843]
03:05:13 [INFO] [MSG_TYPE][0810]
03:05:13 [INFO] [BITMAP  ][7, 11, 39, 70]
03:05:13 [INFO] [007][010][0414030512]
03:05:13 [INFO] [011][006][615012]
03:05:13 [INFO] [039][002][00]
03:05:13 [INFO] [070][002][30]
03:05:13 [INFO]
03:05:13 [INFO] Transaction ID [20240414_030512_8695314843] matched, response time seconds: 1.082
```

# Specification settings

## Specification Overview

This chapter describes the specification settings and maintenance. Refer to SVFE E-pay specification for more info.

The Specification is a root data structure, describing data processing mechanics, such as fields hierarchy, types, 
validation, and other things. SIGNAL needs the correct settings in the Specification for regular work. From v0.15 
specification settings are required for transaction processing.

The specification can be set using the button "Specification" of MainWindow. Settings through GUI are highly recommended 
by the author. 


## Settings description

![image](https://i.imgur.com/Wvg8EuX.png)

The table below describes the settings window columns from left to right

| Field       | Purpose                                                                                                                                                                                                                                                | Used to                                                      | Type                       | Mandatory    |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|----------------------------|--------------|
| Field       | The field or subfield number                                                                                                                                                                                                                           | Define main fields structure, describe fields nesting        | Number                     | Yes          |
| Description | Free text field purpose explanation                                                                                                                                                                                                                    | Show field description on MainWindow transaction constructor | Text, no min or max length | No           |
| Min Len     | Field value minimum length                                                                                                                                                                                                                             | Fields validation during data processing                     | Number, min value is 1     | Yes          |
| Max Len     | Field value maximum length                                                                                                                                                                                                                             | Fields validation during data processing                     | Number, min value is 1     | Yes          | 
| Data Len    | Applicable for variable-length fields. This means count numbers mark the field's own length. Should be taken from the E-pay specification document. In the specification usually marks as `LLVAR` - 2 digits, `LLLVAR` - 3 digits, and so on           | Message construction, Fields validation, Message parsing     | Number, min value is 0     | Yes          |
| Tag Len     | For complex fields only (field should contain subfields). This means count numbers mark. In the specification usually marked as `LLVAR` - 2 digits, `LLLVAR` - 3 digits, and so on. Tag Len of the field should be equal to the field's own Data Len   | Message construction, Fields validation, Message parsing     | Number, min value is 0     | Yes          |
| Alpha       | Are the alphabetic letters allowed in this field                                                                                                                                                                                                       | Fields validation                                            | Checkbox                   | Yes          |
| Numeric     | Are the digits  allowed in this field                                                                                                                                                                                                                  | Fields validation                                            | Checkbox                   | Yes          |
| Special     | Are the special characters allowed in this field                                                                                                                                                                                                       | Fields validation                                            | Checkbox                   | Yes          |
| Matching    | If yes the field will be used for matching requests and responses. It means SIGNAL, sending the transaction expects the same field value in the SV response                                                                                            | Message matching                                             | Checkbox                   | Yes          |
| Reversal    | When Yes then the field value will be taken from the original message and put to the reversal in case of reversal                                                                                                                                      | Message matching, message construction                       | Checkbox                   | Yes          |
| Generated   | Can the fields be auto-generated by SIGNAL before sending? If yes then the corresponding checkbox appears in Main Window¹                                                                                                                              | Message construction                                         | Checkbox                   | Yes          |
| Secret      | If yes field value will be hidden in the log, transaction constructor, and on MainWindow display³                                                                                                                                                      | Display data, log writing                                    | Checkbox                   | Yes          |

¹ Currently, SIGNAL supports randomly generated field values only. No date-time and other specific format are supported, except pre-defined fields 7 and 11

² Due to security reasons, it is impossible to set Primary Account Number (Field 2) as non-secret. The field has a non-removable "secret" mark  


## MTI setting



## Remote specification
The local specification `JSON` file always is at the path `common/data/settings/specification.json`, however, SIGNAL can get general specification `JSON` remotely on the startup stage and by the user's request in SpecWindow. The specification URL should be set in the settings. In case when the remote specification is set by settings but the SIGNAL is unable to get remote specification data the local spec data will be taken instead from the "settings" directory

SIGNAL can get general specification JSON remotely on the startup stage and by the user's request in SpecWindow. The specification URL should be set in the settings.

In general, the specification endpoint has to return the Spec JSON by GET request without any additional actions

The conditions for the remote spec endpoint:


* Be available when SIGNAL starts
* Support GET requests with no additional actions
* Respond by HTTP-status 200
* Send header "Content-type": "application/json" in the response
* Return valid specification data in response-body


### Remote specification endpoint setting

The following [code](#remote-spec-endpoint-code-example) illustrates the endpoint example. In this example, endpoint http://127.0.0.1:4242/specification returns specification file data `/opt/spec/specification.json`

  
**To begin remote specification endpoint**

1. Prepare specification.json file. You can get it from the directory `common/data/settings` or save a copy using SpecWindow which executes by button `Specification` on the MainWindow 
2. Prepare file `signal_spec.py`, containing [endpoint script](#remote-spec-endpoint-code-example)
3. Set `SERVER_ADDRESS`, `PORT`, `FILE` parameters in the file `signal_spec.py`
4. Put both files `specification.json` and `signal_spec.py` to remote server
5. Run the code using command `nohup python signal_spec.py &`
6. For checking open specified URL in browser, it should show the specification `JSON`. In example below the URL is http://127.0.0.1:4242/specification


**Test of remote specification endpoint**

![image](https://i.imgur.com/mhjheFj.png)


### Remote spec endpoint code example

```python
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

"""
Basic realization of SIGNAL Specification remote endpoint. This endpoint returns specification.json by GET request

Check and set the required configuration parameters below before run 

Was tested on Python3 only
"""

SERVER_ADDRESS = '127.0.0.1'  # The address of the server machine
PORT = 4242  # Port for incoming connection
PATH = '/specification'  # URL path to get the specification file
FILE = '/opt/spec/specification.json'  # The Specification file path, the file should be returned by GET request

# By these settings we create URL http://127.0.0.1:4242/specification which returns file /opt/spec/specification.json

class HttpSpec(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != PATH:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        with open(FILE) as json_file:
            self.wfile.write(json_file.read().encode())


server = HTTPServer((SERVER_ADDRESS, PORT), HttpSpec)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
```


# Transaction data files


## Overview

The SIGNAL supports multiple representations of transaction data files. The data can be put to the SIGNAL using 
one of three formats - `JSON`, `INI`, and `DUMP`. The data is stored in text files, which can be read or written 
by SIGNAL. This chapter describes each format's features and purpose

## The data formats description 

| Format | File extension | Incoming  | Outgoing | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------|----------------|-----------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| JSON   | `.json`        | Yes       | Yes      | Equally well suited for operator reading and machine analysis. The main goal is to make complex fields not so complicated, through structure-readable decomposition. Fields and subfield lengths are left out because they will be calculated later according to the Specification. All the transactions, incoming and outgoing stored in memory in JSON representation. Strictly requires Specification settings for each subfield                                                            | 
| INI    | `.ini`         | Yes       | Yes      | Flat format, where each field is written in one string. Fields fill in Tag-Length-Value (TLV) style with no separators. All the lengths have to be calculated and set by the operator. The format skips the data validation process. Recommended when you definitely understand what you do. Requires specification for top-level fields only, subfields specification is not required                                                                                                         | 
| DUMP   | `.dmp`         | Yes       | Yes      | Raw SV-dump format. Used for loading and generating SVFE-compatible dump messages for parsing incoming and generating outgoing SV messages. Low-level data exchange with SVFE makes using this format. The DUMP is the fully ready-read message for the SVFE epayint module. For the sv-dump building recommended setting field data through the transaction constructor using JSON or INI style, then generate the dump by SIGNAL interface. Manual analysis or generation is not recommended | 

## Loading to the SIGNAL

To read the incoming data file in the open SIGNAL window press `CTRL + O`, or hit the button "Parse file" on the 
MainWindow bottom, then choose the file using the file-navigation window. SIGNAL recognizes the incoming file format 
by file extension. When the extension is absent or unknown the SIGNAL will try to parse the file using each format 
pattern one by one. Better to set the correct extension for each format. Refer to the
[data formats description](#the-data-formats-description) to define the correct extension for each file format

## Save transaction to file

... 

# About

## License

SIGNAL is distributed under the GNU/GPL license as free software. See more on [GNU page](https://www.gnu.org/licenses/)


## Author

Designed and developed by Fedor Ivanov   


In case of any question feel free to [contract author](mailto:fedornivanov@gmail.com?subject=SIGNAL%27s%20user%20request&body=Dear%20Fedor%2C%0A%0A%0A%3E%20Put%20your%20request%20here%20%3C%20%0A%0A%0A%0AMy%20SIGNAL%20version%20is%20v0.18%20%7C%20Released%20in%20Apr%202024%0A) directly
