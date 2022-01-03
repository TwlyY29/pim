pimconf_DATA=config.ini
pimconfdir=$(PIM_CONFDIR)
EXTRA_DIST = config.ini.empty config_daily config_attachments config_getweather config_expenses

do_substitution = sed -e 's,[@]STD_REMINDER_FILE[@],$(STD_REMINDER_FILE),g' -e 's,[@]DAILY_BASE_PATH[@],$(DAILY_BASE_PATH),g' -e 's,[@]EXPENSES_BASE_PATH[@],$(EXPENSES_BASE_PATH),g'

$(srcdir)/config.ini.in:
	cp $(srcdir)/config.ini.empty $(srcdir)/config.ini.in

if INSTALL_DAILY
make_daily: $(srcdir)/config.ini.in
	sed -e '/[@]CONFIG_DAILY[@]/ {' -e 'r $(srcdir)/config_daily' -e 'd' -e '}' -i $(srcdir)/config.ini.in
else !INSTALL_DAILY
make_daily:
	sed -i -e '/[@]CONFIG_DAILY[@]/d' $(srcdir)/config.ini.in
endif

if INSTALL_DAILY_ATTACHMENTS
make_daily_attachments: $(srcdir)/config.ini.in
	sed -e '/[@]CONFIG_DAILY_ATTACHMENTS[@]/ {' -e 'r $(srcdir)/config_attachments' -e 'd' -e '}' -i $(srcdir)/config.ini.in
else !INSTALL_DAILY_ATTACHMENTS
make_daily_attachments:
	sed -i -e '/[@]CONFIG_DAILY_ATTACHMENTS[@]/d' $(srcdir)/config.ini.in
endif

if INSTALL_DAILY_WEATHER
make_daily_weather: $(srcdir)/config.ini.in
	sed -e '/[@]CONFIG_DAILY_WEATHER[@]/ {' -e 'r $(srcdir)/config_getweather' -e 'd' -e '}' -i $(srcdir)/config.ini.in
else !INSTALL_DAILY_WEATHER
make_daily_weather:
	sed -i -e '/[@]CONFIG_DAILY_WEATHER[@]/d' $(srcdir)/config.ini.in
endif

if INSTALL_EXPENSES_CONFIG
make_daily_expenses: $(srcdir)/config.ini.in
	sed -e '/[@]CONFIG_DAILY_EXPENSES[@]/ {' -e 'r $(srcdir)/config_expenses' -e 'd' -e '}' -i $(srcdir)/config.ini.in
else !INSTALL_EXPENSES_CONFIG
make_daily_expenses:
	sed -i -e '/[@]CONFIG_DAILY_EXPENSES[@]/d' $(srcdir)/config.ini.in
endif

$(pimconf_DATA): $(srcdir)/config.ini.in make_daily make_daily_attachments make_daily_expenses make_daily_weather Makefile
	$(do_substitution) < $(srcdir)/config.ini.in > $(pimconf_DATA)

dist-hook:
	rm -f $(distdir)/$(pimconf_DATA) $(distdir)/config.ini.in

