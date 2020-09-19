#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
# import chardet

from csv import CSVHelper

if __name__ == '__main__':
	csv = CSVHelper()
	path = sys.argv[1]
	output = path.replace(".csv", ".lua")
	path = os.path.abspath(sys.argv[1]) 
	info = csv.parse(path) 
	csv.save_to_lua(output)




	

