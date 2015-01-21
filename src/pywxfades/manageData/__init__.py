import localInventory
import remoteInventory
import sys

localInventory.gen_available_runs()
if [i for i in ['-r','-R'] if i in sys.argv]:
    remoteInventory.gen_available_runs()