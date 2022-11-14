  # SmartVista Electronic Commerce Terminal

```
  ::::::::  :::     ::: ::::::::::: :::::::::: :::::::::  ::::    ::::  ::::::::::: ::::    :::     :::     :::
 :+:    :+: :+:     :+:     :+:     :+:        :+:    :+: +:+:+: :+:+:+     :+:     :+:+:   :+:   :+: :+:   :+:
 +:+        +:+     +:+     +:+     +:+        +:+    +:+ +:+ +:+:+ +:+     +:+     :+:+:+  +:+  +:+   +:+  +:+
 +#++:++#++ +#+     +:+     +#+     +#++:++#   +#++:++#:  +#+  +:+  +#+     +#+     +#+ +:+ +#+ +#++:++#++: +#+
        +#+  +#+   +#+      +#+     +#+        +#+    +#+ +#+       +#+     +#+     +#+  +#+#+# +#+     +#+ +#+
 #+#    #+#   #+#+#+#       #+#     #+#        #+#    #+# #+#       #+#     #+#     #+#   #+#+# #+#     #+# #+#
  ########      ###         ###     ########## ###    ### ###       ### ########### ###    #### ###     ### ##########
  
  ⚝⚝⚝⚝⚝
```


Released in Oct 2022, under construction

## Description


SV-Terminal simplifies sending of banking card e-commerce transactions to SmartVista using a useful visual interface making simple things simple to achieve.

The Terminal uses ISO-8583 E-pay protocol for transactions sending, instead of PSP. It can be used during the Payment Systems certification test, for checking and setting up the system on the test environment, during the application development process, and so on.

Also, the Terminal builds like a kit of weakly connected modules like a Parser, Connector, Queue, etc. It allows to reuse or extend the Terminal's functionality making emulators, loaders, parsers, converters, application interfaces, and many other things based on SV-Terminal modules.

SV-Terminal is not an emulator of PSP or SmartVista. It doesn't try to be similar to these systems. It is more positioned as a simplified version card payment terminal, developed with respect for the everyday needs of the Card Processing Support Team.

Written on Python 3.10 with using of PyQt5 and pydantic packages

Allowed use on the test environment only

In case of any questions about the Terminal contact Fedor Ivanov. Your feedback and suggestions are general drivers of SV-Terminal evolution.

## Demo

![image](https://user-images.githubusercontent.com/116465333/197392351-dee7f5a0-1e27-4bf0-9356-3f412ebc3f29.png)


## Author

Designed and developed by Fedor Ivanov


## Requirements and installation

* Python 3.10+
* PyQt5 or PyQt6
* pydantic


To begin, you have to install Python 3.10 or above and use the following command in the program directory. Then use double click on sv_terminal.pyw file for run the Terminal.

```
pip install -r requirements.txt
```

## What's new in this version


* Fields validation added to the Terminal. The validation can be turned off through settings window
* Added internal config to ini files for storing max amount and generated fields
* Added transaction timeouts - after 60 seconds after sending transaction will be deleted from the Queue
* JSON format simplified, backward compatibility exists


