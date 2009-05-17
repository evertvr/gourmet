#!/usr/bin/python
# Copyright (c) 2004, 2005, 2006, 2007 Tom Hinkle
# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

#import sys
#import signal
#signal.signal(signal.SIGINT, signal.SIG_DFL)
import sys, os, os.path, glob

for desktop_file in glob.glob('lib/plugins/*plugin.in') + glob.glob('lib/plugins/*/*plugin.in'):
    os.system('intltool-merge -d i18n/ %s %s'%(desktop_file,
                                               desktop_file[:-3])
              )

if os.path.exists('foo'):
    os.remove('foo/gourmet')
    os.rmdir('foo')

os.mkdir('foo')
os.symlink(os.path.abspath('lib'),'foo/gourmet')
sys.path = [os.path.abspath('foo')] + sys.path
sys.argv.append('--gourmet-directory=%s'%os.path.abspath('/tmp/asdfqwer122'))
sys.argv.append('--data-directory=%s'%os.path.abspath('../data/'))
sys.argv.append('--glade-directory=%s'%os.path.abspath('../glade/'))
sys.argv.append('--image-directory=%s'%os.path.abspath('../images/'))
import gourmet.gglobals
sys.argv = sys.argv[:-4]
print 'yippee let\'s import...'
import gourmet.backends.db_tests
print 'We imported... let\'s call main'
import unittest
testsuite = unittest.TestSuite()
import gourmet.importers.interactive_importer_tests
import gourmet.importers.importer_tests
import gourmet.convert_tests
for module in [gourmet.importers.interactive_importer_tests,
               gourmet.importers.importer_tests,
               gourmet.convert_tests
               ]:
    testsuite.addTest(
        unittest.defaultTestLoader.loadTestsFromModule(
            module
            )
        )
testsuite.addTest(gourmet.backends.db_tests.suite)
tr = unittest.TestResult()
testsuite.run(tr)
if tr.wasSuccessful():
    print 'All ',tr.testsRun,'tests completed successfully!'
else:
    print 'Uh oh...'
    print 'We had ',len(tr.failures),'failures in ',tr.testsRun,'tests'
    for er,tb in tr.failures:
        print '---'
        print er,':',tb
        print '---'
    if tr.errors:
        print 'We had ',len(tr.errors),' errors in',tr.testsRun,'tests'
        for er,tb in tr.errors:
            print '---'
            print er,':',tb
            print '---'
        
#gourmet.backends.db_tests.main()