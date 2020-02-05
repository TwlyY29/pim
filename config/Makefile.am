pimconf_DATA=config.ini
pimconfdir=$(PIM_CONFDIR)
EXTRA_DIST = config.ini.in

do_substitution = sed -e 's,[@]STD_REMINDER_FILE[@],$(STD_REMINDER_FILE),g' 

config.ini: config.ini.in Makefile
	$(do_substitution) < $(srcdir)/config.ini.in > config.ini

dist-hook:
	rm -f $(distdir)/config.ini

