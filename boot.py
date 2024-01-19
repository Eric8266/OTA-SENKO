print('\nBooting . . . . ')
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, machine
#os.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()
gc.enable()
import ugit

#ugit.backup() # good idea to backup your files!
print('Download all latest files from GitHub.')
ugit.pull_all()

print('Boot completed !')
input('New files downloaded')