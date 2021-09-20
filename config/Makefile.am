pimconf_DATA=config.ini
pimconfdir=$(PIM_CONFDIR)
EXTRA_DIST = config.ini.in config_getweather

do_substitution = sed -e 's,[@]STD_REMINDER_FILE[@],$(STD_REMINDER_FILE),g' 

if INSTALL_DAILY_WEATHER

$(pimconf_DATA): $(srcdir)/config.ini.in Makefile
	$(do_substitution) < $(srcdir)/config.ini.in > $(pimconf_DATA)
	$(do_substitution) < $(srcdir)/config_getweather >> $(pimconf_DATA)

else

$(pimconf_DATA): Makefile
	$(do_substitution) < $(srcdir)/config.ini.in > $(pimconf_DATA)
endif

dist-hook:
	rm -f $(distdir)/$(pimconf_DATA)

