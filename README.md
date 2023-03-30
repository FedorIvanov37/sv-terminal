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


In case of any questions about the Terminal contact Fedor Ivanov. Your feedback and suggestions are general drivers of SvTerminal evolution.

## User interface

![image](https://user-images.githubusercontent.com/116465333/197392351-dee7f5a0-1e27-4bf0-9356-3f412ebc3f29.png)


## Modules
![image](https://camo.githubusercontent.com/dccafcb932d549e921b2adb6d56d1bc521c51e2bc8e0f4be5fbaade5c7fef22f/68747470733a2f2f692e696d6775722e636f6d2f75444a334b78352e706e67)




## Requirements and installation

* [Python 3.10+](https://www.python.org/)
* [PyQt6](https://www.qt.io/product/qt6)
* [pydantic](https://docs.pydantic.dev/)


To begin, you have to install Python 3.10 or above and run the following command in the program directory. Then use double click on sv_terminal.pyw file for run the Terminal.

```
pip install -r requirements.txt
```

## What's new in v0.15

* NEW: Added fields basic validation, validation can be switched off in the settings
* NEW: Added transaction timeouts: in case of no response for 60 seconds transaction will be declined
* NEW: Added possibility to set MTI map in GUI. See specification window
* NEW: Added warning when Specification was changed but not saved
* UPD: Updated requirements - framework changed to PyQt6, SvTerminal does not support PyQt5 since v0.15
* UPD: Since v0.15 Specification settings are required for any fields
* UPD: SvTerminal library is separated, and the GUI runs as a specific implementation of the library
* UPD: Incoming JSON-files format simplified with backward compatibility respect
* UPD: New section [CONFIG] added in INI incoming files. Two options are available - MAX_AMOUNT and GENERATE_FIELDS
* FIX: Fixed incorrect field name in INI files
* FIX: Optimized work with bitmap in GUI
* FIX: Terminal fall down when empty field number set in Specification
* FIX: Fixed small bugs inherited from v0.14
* FIX: Code and project structure optimization

## ⚠️ Important notes  

* Allowed usage on test environment only. SvTerminal only implements basic security checks
* Since v0.15 SvTerminal doesn't support PyQt5 anymore
* At the moment SvTerminal doesn't support byte-fields
* Logfile rotation included in the build. SvTerminal stores 10 logfiles by 10M each
* SvTerminal is always free of charge, no way to sell it
* Comments, advice, and review of the code are highly appreciated 

## Author

Designed and developed by [Fedor Ivanov](mailto:f.ivanov@unlimint.com)
