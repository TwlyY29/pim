mailhelper_PYTHON = functions.py __init__.py MIMEUTF8QPText.py
mailhelperdir = $(pythondir)/pim_mailhelper

EXTRA_DIST = functions.py.in __init__.py.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
		-e 's,[@]pimconfdir[@],$(PIM_CONFDIR),g'\
		-e 's,[@]PACKAGE_NAME[@],$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_BUGREPORT[@],$(PACKAGE_BUGREPORT),g' \
		-e 's,[@]VERSION[@],$(VERSION),g'

__init__.py: __init__.py.in Makefile
	$(do_substitution) < $(srcdir)/__init__.py.in > __init__.py

functions.py: functions.py.in Makefile
	$(do_substitution) < $(srcdir)/functions.py.in > functions.py
	
uninstall-hook:
	rm -rf $(mailhelperdir)

dist-hook:
	rm -f $(distdir)/functions.py $(distdir)/__init__.py
