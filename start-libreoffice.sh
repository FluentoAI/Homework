#!/bin/bash

# Start LibreOffice in headless mode
libreoffice --headless --invisible --nologo --nofirststartwizard --accept='socket,host=0.0.0.0,port=8100,tcpNoDelay=1;urp;'
