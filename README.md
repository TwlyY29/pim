Don't we all like braindumping important stuff with the relaxing certainty of not losing track of it?

Sending yourself an email is a possibility. But your email program doesn't remind you of that approaching deadline, automatically. Also, that email with that brilliant idea for a birthday gift doesn't pop up by itself. And finally, the link to that interesting article you could not finish reading in the subway will most likely get lost in the daily flood tide of mails we all love so much.

But still, the idea of sending a short email is charming. So, why not adding a little intelligence? It would be cool to just send a link and receive a copy of that interesting article via email. Also, a daily summary of all approaching deadlines and ideas for birthday gifts would be really helpful. That is what this collection of scripts is for.

The whole idea is to send an email to this program which then creates a reminder, stores that idea of a birthday gift, or downloads the web-article. 


## Details
Please refer to [my website](http://mircoschoenfeld.de/personal-information-manager.html) to read about the details.


## Requirements
* mailserver accepting mails
* `sendmail`
* [remind](https://linux.die.net/man/1/remind) for `daily`-module


## Installation
Installation is based on autotools, i.e. in the directory where you checked out this git call
```
./configure
make
sudo make install
```

Use the parameters `--prefix=`, `--localstatedir=`, and `--sysconfdir=` to the call to `./configure` to specify the installation directory as well as the location of the configuration file. The installation directory defaults to `/usr/local/`, the local state directory to `[PREFIX]/var/`, and the configuration directory to `[PREFIX]/etc/`. You might want to set `--prefix=/`.

Also make sure to check out `./configure --help` to see what else you can adjust to your needs:
```
Some influential environment variables:
  PYTHON            the Python interpreter
  RCV_BASE_PATH     'set location of log output dir'
  DAILY_BASE_PATH   'set location of reminders file'
  CRONPATTERN       'set cron pattern to configure sending of reminder'
  MAILALIAS         'set mailalias for receiving mails'
  PIM_CONFDIR       'set directory for config file'
  MAIL_USER         'username of mailserver'
```

The installation routine will add an alias to your `[PREFIX]/etc/aliases`:
```
    pim: "| /path/to/mainreceiver"
```
This ensures that mails to `pim@yourdoma.in` will be handled by the `pim` entry point. Of course, `pim` will be set to the value of `MAILALIAS` specified in the call to `configure`.

