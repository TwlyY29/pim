from __future__ import print_function

import os.path
import configparser
from datetime import datetime
from calendar import monthrange
from collections import defaultdict

SEP='\t'

def diff_month(d1, d2):
  return (d1.year - d2.year) * 12 + d1.month - d2.month

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]

def rest_days_in_month():
  _now = datetime.now()
  days = number_of_days_in_month(_now.year, _now.month)
  return days - _now.day

def compile_output(CONF_SEC, CONF_FILE):
  out = ''
  title = None
  config = configparser.ConfigParser()
  config.read(CONF_FILE)
  if config.has_section(CONF_SEC):
    title = config[CONF_SEC]['title']
    report_database = config[CONF_SEC]['report_pocket_money_database']
    report_database = f"database_{report_database}"
    if report_database in config[CONF_SEC]:
      DATABASE = config[CONF_SEC][report_database]
      DATEPATT = config[CONF_SEC]['date_pattern']
      MONTHLY_PLUS = float(config[CONF_SEC]['report_pocket_money_monthly_amount'])
      STATS_PER_CATEGORY = config[CONF_SEC]['report_pocket_money_stats_per_category']
      STATS_PER_CATEGORY_TOP_N = int(config[CONF_SEC]['report_pocket_money_stats_per_category_top_n'])
      
      if os.path.isfile(DATABASE):
        
        month = datetime.now().month
        month_amount = 0
        
        stats = defaultdict(float)
        
        with open(DATABASE, 'r') as _database:
          header = _database.readline()
          header = header.strip().split(SEP)
          ind_date = header.index('date')
          ind_plusminus = header.index('pm')
          ind_amount = header.index('amount')
          ind_category = header.index('category')
          
          last_monthly_plus = None
          
          for line in _database:
            line = line.strip().split(SEP)
            date = datetime.strptime(line[ind_date], DATEPATT)
            amount = float(line[ind_amount])
            is_expense = (line[ind_plusminus] == '-')
            
            if last_monthly_plus is None:
              last_monthly_plus = datetime(date.year, date.month, 1)
              month_amount += MONTHLY_PLUS
            elif date.year != last_monthly_plus.year or date.month != last_monthly_plus.month:
              months = diff_month(date, last_monthly_plus)
              month_amount += MONTHLY_PLUS * months
              last_monthly_plus = datetime(date.year, date.month, 1)
            
            month_amount += amount * -1 if is_expense else float(line[ind_amount])
            
            if STATS_PER_CATEGORY and is_expense:
              stats[line[ind_category]] += amount
          
          months = diff_month(datetime.now(), last_monthly_plus)
          if months > 0:
            month_amount += MONTHLY_PLUS * months
          
          month_amount = round(month_amount, 2)
          rest_of_month = rest_days_in_month()
          if rest_of_month > 0:
            daily_avg = round(month_amount / rest_of_month, 2)
            out = f"For this month, you have {month_amount}€ left,\nthat's {daily_avg}€ for all of the {rest_of_month} days left of {datetime.strftime(datetime.now(), '%B')}.\n"
          else:
            out = f"For this month, you have {month_amount}€ left.\nHang in there. Today's last day of {datetime.strftime(datetime.now(), '%B')}!\n"
            
          
          if STATS_PER_CATEGORY:
            stats_sorted = sorted(stats.items(),key=lambda k_v: k_v[1],reverse=True)
            out += "\n" + f"Your top {STATS_PER_CATEGORY_TOP_N} categories:\n"
            for cat,amount in stats_sorted[0:STATS_PER_CATEGORY_TOP_N]:
              amount = round(amount, 2)
              out += f"   {cat}:\t{amount:8.2f}€\n"
        
        if out != '':
          return title,out
    return title,False
    
if __name__ == '__main__':
  title, reminder = compile_output('daily_expenses','../../../config/config.ini.testing')
  print(reminder)
