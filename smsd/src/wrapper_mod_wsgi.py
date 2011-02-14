# """
smsd_path = '/home/jimmyz/smsd/src'

from os import chdir
chdir(smsd_path)

import sys
sys.path.insert(0, '.')
# """
from os import getcwd
import sys
print 'wrapper: pwd : ' + getcwd()
print 'wrapper: path : ' + ', '.join(sys.path)

from smsd import smsd
application = smsd()
