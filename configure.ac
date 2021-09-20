AC_INIT([Personal Information Manager],
        0.1.2,
        TWlyY29@gmail.com,
        pim,
        http://www.mircoschoenfeld.de)
AM_INIT_AUTOMAKE([foreign])
AM_PATH_PYTHON([3.5])

AC_CONFIG_FILES([Makefile src/Makefile src/pim_mailhelper/Makefile src/pim_modules/Makefile config/Makefile cron/Makefile])
AC_CONFIG_FILES([src/pim_modules/daily/Makefile])

AC_SUBST(RCV_BASE_PATH,"$localstatedir/log/")
AC_ARG_VAR(RCV_BASE_PATH, 'set location of log output dir')
AC_SUBST(DAILY_BASE_PATH,"$localstatedir/mail/")
AC_ARG_VAR(DAILY_BASE_PATH, 'set location of reminders file')
AC_SUBST(STD_REMINDER_FILE,"$DAILY_BASE_PATH/pim_daily_reminder")
AC_SUBST(CRONPATTERN,'0 5 * * *')
AC_ARG_VAR(CRONPATTERN, 'set cron pattern to configure sending of reminder')
AC_SUBST(MAILALIAS,'reminder')
AC_ARG_VAR(MAILALIAS, 'set mailalias for receiving mails')
AC_SUBST(PIM_CONFDIR,"$sysconfdir/pim")
AC_ARG_VAR(PIM_CONFDIR, 'set directory for config file')
AC_SUBST(MAIL_USER,"mail")
AC_ARG_VAR(MAIL_USER, 'username of mailserver')

AX_PYTHON_MODULE(dateparser, "", python3)
AX_PYTHON_MODULE([requests], "", python3)
AX_PYTHON_MODULE(configparser, "", python3)

AC_ARG_ENABLE([daily],
[AS_HELP_STRING([--disable-daily],[Turn off daily])],
[case "${enableval}" in
  no) daily="check" ;;
  yes)  daily="no" ;;
  *) AC_MSG_ERROR([bad value ${enableval} for --disable-daily]) ;;
esac],[daily="yes"])

AC_ARG_ENABLE([daily_weather],
[AS_HELP_STRING([--enable-daily_weather],[Turn on daily weather report])],
[case "${enableval}" in
  no) daily_weather="no" ;;
  yes)  daily_weather="check" ;;
  *) AC_MSG_ERROR([bad value ${enableval} for --enable-daily_weather]) ;;
esac],[daily_weather=false])

AS_IF([test "x$daily_weather" = xcheck],
  [AS_IF([test "x$HAVE_PYMOD_REQUESTS" = x"no"],
      [AC_MSG_ERROR([missing python module: requests])],
      [daily_weather=true])])
AM_CONDITIONAL([INSTALL_DAILY_WEATHER], [test "x$daily_weather" = xtrue])

AS_IF([test "x$daily" != xno],
  [AX_PROG_PERL_MODULES( iCal::Parser,
    [daily=check],
    [AS_IF([test "x$daily" = xyes],
      [AC_MSG_ERROR([perl module iCal::Parser required, but not found.])],
      [daily=false])])])
AS_IF([test "x$daily" = xcheck],
      [AC_CHECK_PROG(sendmail_exists,sendmail,true,false)])
AS_IF([test "x$sendmail_exists" = xtrue],
      [daily=true],
      [AC_MSG_ERROR([sendmail required, but not found.])])
AM_CONDITIONAL([INSTALL_DAILY], [test "x$daily" = xtrue])

AC_SUBST(VERSION)
AC_SUBST(PACKAGE_NAME)
AC_SUBST(PACKAGE_BUGREPORT)

AC_OUTPUT
