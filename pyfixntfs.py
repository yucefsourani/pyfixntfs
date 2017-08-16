#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  pyfixntfs.py
#  
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os
import subprocess
import string
import dbus
from os.path import basename,join


pkexec = "pkexec"

class Dives(object):
    def __init__(self,bus,block_device,number=10):
        self.__bus           = bus
        self.__block_device  = block_device
        self.__number        = number
        self.__proxy         = self.__bus.get_object("org.freedesktop.UDisks2",self.__block_device)
        self.__interface     = dbus.Interface(self.__proxy,"org.freedesktop.DBus.Properties")
        self.__driveo        = self.__interface.Get("org.freedesktop.UDisks2.Block","Drive")
        self.BLOCKDO         = self.__block_device
        self.DRIVE           = "/dev/"+basename(self.__block_device)
        self.DRIVEC          = basename(self.__block_device)
        self.DRIVEO          = self.__driveo
        self.NAME            = basename(self.__driveo)

        self.__drive_proxy     = self.__bus.get_object("org.freedesktop.UDisks2",self.__driveo)
        self.__drive_interface = dbus.Interface(self.__drive_proxy,"org.freedesktop.DBus.Properties")
        self.REMOVABLE         = self.__drive_interface.Get("org.freedesktop.UDisks2.Drive","Removable")
        self.SIZE              = self.__drive_interface.Get("org.freedesktop.UDisks2.Drive","Size")
        self.CONNECTIONB       = self.__drive_interface.Get("org.freedesktop.UDisks2.Drive","ConnectionBus")
        self.ALLPATTIONS       = self.__all_parttions()
        self.ALL               = [self.BLOCKDO,self.DRIVE,self.DRIVEC,self.DRIVEO,self.REMOVABLE,self.SIZE,self.CONNECTIONB,\
        self.ALLPATTIONS]

        
        
    def __all_parttions(self):
        result = []
        for i in range(1,self.__number+1):
            try:
                proxy = self.__bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2/block_devices/{}{}".format(self.DRIVEC,str(i)))
                interface = dbus.Interface(proxy,"org.freedesktop.DBus.Properties")
                fstype = interface.Get("org.freedesktop.UDisks2.Block","IdType")
                result.append(["/org/freedesktop/UDisks2/block_devices/{}{}".format(self.DRIVEC,str(i)),self.DRIVE+str(i),self.DRIVEC+str(i),str(fstype)])
            except:
                pass
        return result

    def umount_(self,obj,force=False):
        try:
            proxy = self.__bus.get_object("org.freedesktop.UDisks2",obj)
            interface = dbus.Interface(proxy,"org.freedesktop.UDisks2.Filesystem")
            umount = interface.get_dbus_method("Unmount")
            umount({"force" : force})
        except Exception as e :
            return e

        return True
        
    def umount_drive(self):
        for p in self.ALLPATTIONS:
            self.umount_(p[0])
        

def INIT():
    bus = dbus.SystemBus()
    result  = []
    for char in string.ascii_lowercase :
        try:
            bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2/block_devices/sd{}".format(char))
            result.append(Dives(bus,"/org/freedesktop/UDisks2/block_devices/sd{}".format(char)))
        except :
            pass
    return result
    
    

all_object_parttions = INIT()

def lsof_(location):
	check = subprocess.check_output("lsof {}".format(location).split(),encoding="utf-8")
	return check
	
def get_ntfs_parttions():
	result = dict()
	count  = 1
	for d in all_object_parttions:
		for i in d.ALLPATTIONS:
			if i[-1] == "ntfs":
				result.setdefault(str(count),[i[1],d,i[0]])
				count += 1
	if len(result)!=0:
		result.setdefault(str(count),["All","All","All"])
	return result
	
def fix_parttions(l):
	to_write = ""
	for i in l:
		to_write += "ntfsfix "+i[0]+"\n"
		
	with open("/tmp/asgh7421dfsaq3zxgopbfryjjd.sh","w") as myfile:
		myfile.write(to_write)
	check = subprocess.call("chmod 755 /tmp/asgh7421dfsaq3zxgopbfryjjd.sh".split())
	if check != 0:
		return False
	check = subprocess.call("{} bash /tmp/asgh7421dfsaq3zxgopbfryjjd.sh".format(pkexec).split())
	if check != 0:
		return False
	return True
	
def umount(l,force=False):
	for d in l:
		check = d[1].umount_(d[-1],force)
		if  check!=True:
			check = str(check)
			if check.startswith("org.freedesktop.UDisks2.Error.DeviceBusy"):
				check = check.split()
				print ("\nDevice {} Is Busy Please Close This And Try Again :\n".format(check[3][:-1]))
				print(lsof_(check[-4][:-1]))
				while True:
					print ("\nF To Force Umount || R To Return : \n")
					answer = input("\n- ")
					if answer == "f" or answer == "F":
						return  umount(l,force=True)
					elif answer == "r" or answer == "R":
						return False
		
	if not fix_parttions(l):
		return False
	return True
		
def main(msg=""):
	ntfs_parttions = get_ntfs_parttions()
	if len(ntfs_parttions)!=0:
		while True:
			os.system("clear")
			if  len(msg)!=0:
				print (msg)
			print ("Choice Parttions || Q To Quit:\n")
			for k,v in ntfs_parttions.items():
				print (k+"- "+v[0]+".\n")
			answer = input("\n- ").strip()
			if answer == "q" or answer == "Q":
				exit("\nbye...")
			elif answer in ntfs_parttions.keys():
				if ntfs_parttions[answer][0] == "All":
					t = [ntfs_parttions[k] for k,v in ntfs_parttions.items() if ntfs_parttions[k][0]!="All" ]
					check = umount(t)
					if not check:
						return main("Fix Fail.\n")
					else:
						return main ("Success.\n")
				else:
					check = umount([ntfs_parttions[answer]])
					if not  check:
						return main("Fix Fail.\n")
					else:
						return main ("Success.\n")
	else:
		exit ("\nNothing To Do.")

main()
