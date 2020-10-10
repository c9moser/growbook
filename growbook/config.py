# growbook/config.py
################################################################################
# Copyright (C) 2020  Christian Moser                                          #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
################################################################################

import gi
from gi.repository import GLib
import os

config={
    'version':(0,0,26),
    'db-version':(0,1),
    'datadir':os.path.join(GLib.get_user_data_dir(),'growbook'),
    'dbfile':os.path.join(GLib.get_user_data_dir(),'growbook','growbook.db'),
    'open-ongoing-growlogs':True
}

def bool_to_db(value):
        if value:
            return "yes"
        return "no"

def bool_from_db(value):
    if value == 'yes':
        return True
    return False

def _check_db_version(db_version):
        dbv=config['db-version']
        if db_version[0] >= dbv[0] and db_version[1] >= dbv[0]:
            return True
        return False
        
def init_config(dbcon):     
    cursor=dbcon.execute("SELECT key,value FROM config WHERE key=?;",('db-version',))
    row=cursor.fetchone()
    if not row:    
        dbcon.executemany("INSERT INTO config (key,value) VALUES (?,?);",
                          [("db-version",'.'.join((str(i) for i in config['db-version']))),
                           ("open-ongoing-growlogs",bool_to_db(config['open-ongoing-growlogs']),)])
        dbcon.commit()
    else:
        db_version=tuple(row[1].split('.'))
        if not _check_db_version(db_version):
            pass

        config['db-version']=db_version
        
        cursor=dbcon.execute('SELECT key,value FROM config WHERE key=?;',('open-ongoing-growlogs',))
        row=cursor.fetchone()
        config[row[0]]=bool_from_db(row[1])

def save_config(dbcon):
    dbcon.executemany("UPDATE config SET value=? WHERE key=?;",
                      [(bool_to_db(config['open-ongoing-growlogs']),'open-ongoing-growlogs')])
    dbcon.commit()


