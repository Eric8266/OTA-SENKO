print('\nBooting . . . . ')
# This file is executed on every boot (including wake-boot from deepsleep)

import os, machine
import gc
gc.collect()
gc.enable()

#import webrepl_setup
#import webrepl
#webrepl.start()

print('Boot completed !')