modules_PYTHON = __init__.py
modulesdir = $(pythondir)/pim_modules

if INSTALL_DAILY
  MAYBE_DAILY = daily
endif

if INSTALL_EXPENSES
  MAYBE_EXPENSES = expenses
endif

if INSTALL_DAILYCALDAV
  MAYBE_DAILYCALDAV = dailycaldav
endif

EXTRA_DIST = __init__.py.in

SUBDIRS = $(MAYBE_DAILY) $(MAYBE_EXPENSES) $(MAYBE_DAILYCALDAV)

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
		-e 's,[@]pimconfdir[@],$(PIM_CONFDIR),g'\
		-e 's,[@]PACKAGE_NAME[@],$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_BUGREPORT[@],$(PACKAGE_BUGREPORT),g' \
		-e 's,[@]VERSION[@],$(VERSION),g'

__init__.py: __init__.py.in Makefile
	$(do_substitution) < $(srcdir)/__init__.py.in > __init__.py

uninstall-hook:
	-rm -rf $(modulesdir)

dist-hook:
	rm -f $(distdir)/__init__.py
