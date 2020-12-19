pimconf_DATA=config.ini
pimconfdir=$(PIM_CONFDIR)
EXTRA_DIST = config.ini.in

do_substitution = sed -e 's,[@]STD_REMINDER_FILE[@],$(STD_REMINDER_FILE),g' 

$(pimconf_DATA): $(EXTRA_DIST) Makefile
	$(do_substitution) < $(srcdir)/$(EXTRA_DIST) > $(pimconf_DATA)

dist-hook:
	rm -f $(distdir)/$(pimconf_DATA)

