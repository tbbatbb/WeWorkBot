#!python3.9
# -*- encoding: utf-8 -*-

from os import path
import sys, os, datetime, traceback, datetime

class Logger(object):
    '''Logger'''
    
    F_RED     = '\033[;31m'
    B_RED     = '\033[;41m'
    F_GREEN   = '\033[;32m'
    B_GREEN   = '\033[;42m'
    F_YELLOW  = '\033[;33m'
    B_YELLOW  = '\033[;43m'
    F_BLUE    = '\033[;34m'
    B_BLUE    = '\033[;44m'
    C_DEFAULT = '\033[0m |'

    L_INFO:int  = 1
    L_WARN:int  = 2
    L_ERROR:int = 3
    L_DEBUG:int = 4
    L_NONE:int = 5
    CLS_LEVEL:int = L_INFO

    LOG_DIR:str = 'logs'
    TOTAL_LOG_NAME:str = (datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)).strftime('%Y%m%d%H%M%S')

    def __init__(self, name:str, tz:int=8, save:bool=False, level:int=L_INFO, sym_info:str='[√]', sym_warn:str='[!]', sym_err:str='[x]'):
        self.name:str = name
        self.time_delta:datetime.timedelta = datetime.timedelta(hours=tz)
        self.save_to_file:bool = save
        self.sym_info:str = sym_info
        self.sym_warn:str = sym_warn
        self.sym_error:str = sym_err
        self.__level:int = level

    def __now_time(self):
        now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        return (now + self.time_delta)
    
    def __prt(self, color:str, symbol:str, *args, with_stack:bool=False, **kwarg):
        ts = self.__now_time().strftime('%H:%M:%S')
        if with_stack: call_stack:str = '->'.join(map(lambda s: f'{s[2]}:{s[1]}', traceback.extract_stack()[:-2]))
        else:
            line, caller = traceback.extract_stack()[-3][1:3]
            call_stack:str = f'[{caller}:{line}]'
        print(color + symbol, ts, f'[{self.name}]', call_stack + Logger.C_DEFAULT, *args, **kwarg)
        sys.stdout.flush()
        msg = ' '.join([str(a) for a in args])
        self.__save(self.TOTAL_LOG_NAME, f'[{ts}] | {msg}{os.linesep}')
        if self.save_to_file:
            self.__save(self.name, f'{symbol}[{ts}] | {msg}{os.linesep}')

    def __save(self, file_name:str, msg:str):
        if not path.isdir(self.LOG_DIR):
            os.mkdir(self.LOG_DIR)
            self.info(f'Directory {self.LOG_DIR} For Log Files Created.')
        log_file:str = path.join(self.LOG_DIR, f'{file_name}.log')
        with open(log_file, 'a') as outf:
            outf.write(msg)

    def clean(self):
        dirs:list = [path.join(self.LOG_DIR, d) for d in os.listdir(self.LOG_DIR)]
        files:list = [d for d in dirs if path.isfile(d) and d.endswith('.log')]
        for f in files:
            os.remove(f)
        return self

    def info(self, *args, highlight:bool=False, with_stack:bool=False, **kwarg):
        if max(self.__level, Logger.CLS_LEVEL) > Logger.L_INFO:
            return
        color = Logger.F_GREEN if not highlight else Logger.B_GREEN
        self.__prt(color, self.sym_info, *args, with_stack=with_stack, **kwarg)
        return self
    
    def dbg(self, *args, highlight:bool=False, with_stack:bool=False, **kwarg):
        if max(self.__level, Logger.CLS_LEVEL) > Logger.L_DEBUG:
            return
        color = Logger.F_BLUE if not highlight else Logger.B_BLUE
        self.__prt(color, self.sym_info, *args, with_stack=with_stack, **kwarg)
        return self

    def warn(self, *args, highlight:bool=False, with_stack:bool=False, **kwarg):
        if max(self.__level, Logger.CLS_LEVEL) > Logger.L_WARN:
            return
        color = Logger.F_YELLOW if not highlight else Logger.B_YELLOW
        self.__prt(color, self.sym_warn, *args, with_stack=with_stack, **kwarg)
        return self

    def error(self, *args, highlight:bool=False, with_stack:bool=False, **kwarg):
        if max(self.__level, Logger.CLS_LEVEL) > Logger.L_ERROR:
            return
        color = Logger.F_RED if not highlight else Logger.B_RED
        self.__prt(color, self.sym_error, *args, with_stack=with_stack, **kwarg)
        return self

    def set_level(self, v:int=0):
        if v not in range(self.L_NONE + 1):
            self.error(f'Invalid Logging Level {v}')
            return self
        self.__level = v
        return self
    
    @classmethod
    def set_global_level(cls, v:int=0):
        """
        Set Globol Logging Level Which Can Influence All The Logger
        """
        if v not in range(cls.L_NONE + 1):
            raise Exception(f'Invalid Logging Level {v}')
        cls.CLS_LEVEL = v
