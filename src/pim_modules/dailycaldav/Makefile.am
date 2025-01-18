dailycaldav_PYTHON = getreminders.py __init__.py
dailycaldavdir = $(pythondir)/pim_modules/dailycaldav

EXTRA_DIST = __init__.py.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
		-e 's,[@]pimconfdir[@],$(PIM_CONFDIR),g' \
		-e 's,[@]PACKAGE_NAME[@],$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_BUGREPORT[@],$(PACKAGE_BUGREPORT),g' \
		-e 's,[@]VERSION[@],$(VERSION),g'

__init__.py: __init__.py.in Makefile
	$(do_substitution) < $(srcdir)/__init__.py.in > __init__.py

dist-hook:
	rm -f $(distdir)/__init__.py
