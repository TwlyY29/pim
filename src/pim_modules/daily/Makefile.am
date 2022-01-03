daily_PYTHON = getreminders.py getattachments.py daily_weather.py daily_expenses.py receive.py __init__.py
daily_SCRIPTS = ical2rem.pl
dailydir = $(pythondir)/pim_modules/daily

EXTRA_DIST = __init__.py.in ical2rem.pl

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
		-e 's,[@]DAILY_BASE_PATH[@],$(DAILY_BASE_PATH),g' \
		-e 's,[@]STD_REMINDER_FILE[@],$(STD_REMINDER_FILE),g' \
		-e 's,[@]PYTHON[@],$(PYTHON),g' \
		-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
		-e 's,[@]RCV_BASE_PATH[@],$(RCV_BASE_PATH),g' \
		-e 's,[@]pimconfdir[@],$(PIM_CONFDIR),g' \
		-e 's,[@]PACKAGE_NAME[@],$(PACKAGE_NAME),g' \
		-e 's,[@]PACKAGE_BUGREPORT[@],$(PACKAGE_BUGREPORT),g' \
		-e 's,[@]VERSION[@],$(VERSION),g'


if INSTALL_DAILY_WEATHER
do_substitution += -e 's,[@]DAILY_WEATHER_ACTIVATED[@],True,g'
else
do_substitution += -e 's,[@]DAILY_WEATHER_ACTIVATED[@],False,g'
endif

if INSTALL_DAILY_EXPENSES
do_substitution += -e 's,[@]DAILY_EXPENSES_ACTIVATED[@],True,g'
else
do_substitution += -e 's,[@]DAILY_EXPENSES_ACTIVATED[@],False,g'
endif

__init__.py: __init__.py.in Makefile
	$(do_substitution) < $(srcdir)/__init__.py.in > __init__.py

dist-hook:
	rm -f $(distdir)/__init__.py

install-exec-hook:
	mkdir -p "$(shell dirname $(STD_REMINDER_FILE))"
	touch "$(STD_REMINDER_FILE)"
	chgrp $(MAIL_USER) "$(STD_REMINDER_FILE)"
	chmod g+w "$(STD_REMINDER_FILE)"
