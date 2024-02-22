"""
Kreirati dekorator koji 'loguje' podatke o radu funkcije u csv fajlu "execution_log.csv" tako što upisuje
sledeće podatke odvojene tačka zarezom:
● trenutak (datum i vreme) poziva funkcije
● pun naziv funkcije (uključujući i njene ulazne argumente)
● vreme izvršavanja funkcije (koju dekoriše) u milisekundama
Potrebno je obezbediti da se sadržaj loga ne prepisuje pri svakom novom pozivu dekorisane funkcije
već da se postojeći sadržaj log fajla samo dopunjuje.
Imati u vidu da dekorisana funkcija može imati nula ili više pozicionih argumenata (args), kao i nula ili
više imenovanih argumenata (kwargs). (20 poena)
Testirati dekorator tako što ćete funkcije iz prethodnog zadatka dekorisati ovim dekoratorom. (5
poena)
Predlog je da se zadatak rešava korišćenjem onih pristupa i Python paketa koji su korišćeni u sličnim
zadacima u toku nastave, ali je dozvoljeno rešiti ga i na drugi način
"""
import functools
from datetime import datetime
from time import perf_counter
from pathlib import Path
import csv
from sys import stderr
def write_to_csv(fpath, data):
    path_exists = fpath.exists()
    try:
        with open(fpath,'w') as fobj:
            if not path_exists:
                csv_writer = csv.writer(fobj)
            csv_writer.writerow(data)
    except OSError as err:
        stderr.write(f"OS error\n{err}\n")

def function_execution_logger(func):

    @functools.wraps(func)
    def wrapper_function_execution_logger(*args,**kwargs):
        start_dt = datetime.now()
        func_name = func.__name__+"("
        if args:
            func_name += ", ".join([str(arg) for arg in args])
        if kwargs:
            func_name += ", ".join([f"{key}={val}" for key, val in kwargs])
        func_name+=" ) "
        start_time = perf_counter()
        value = func(*args, **kwargs)
        exec_time = (perf_counter() - start_time)*1000
        fpath = Path.cwd()/'../data/func_execution_logger.csv'
        write_to_csv(fpath, (start_dt, func_name, exec_time))
