#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

class Csvhelper(object):
	"""docstring for Csvhelper"""
	def __init__(self):
		super(Csvhelper, self).__init__()	

	def parse_types(self, line):
		if line[0] == "#":
			line = line[1:]
		return line.split(",")

	def parse_fields(self, line):
		if line[0] == "#":
			line = line[1:]
		return line.split(",")

	def parse_int(self, str):
		if len(str.strip()) == 0:
			return 0
		if "." in str:
			return float(str.strip())
		return int(str.strip())

	def parse_vint(self, str):
		if len(str.strip()) == 0:
			return []

		if len(str) >= 2 and str[0] == '<' and str[-1] == '>':
			str = str[1:-1]

		vi = str.split("|")
		for i in range(0,len(vi)):
			vi[i] = self.parse_int(vi[i])
		return vi

	def parse_vvint(self, str):
		if len(str.strip()) == 0:
			return []
		vvi = str.split("%")
		for i in range(0,len(vvi)):
			vvi[i] = self.parse_vint(vvi[i])
		return vvi

	def parse_vvvint(self, str):
		pass

	def parse_string(self, str):
		return str

	def parse_vstring(self, str):
		if len(str.strip()) == 0:
			return []

		if len(str) >= 2 and str[0] == '<' and str[-1] == '>':
			str = str[1:-1]

		vi = str.split("|")
		for i in range(0,len(vi)):
			vi[i] = self.parse_string(vi[i])
		return vi

	def parse_vvstring(self, str):
		if len(str.strip()) == 0:
			return []
		vvi = str.split("%")
		for i in range(0,len(vvi)):
			vvi[i] = self.parse_vstring(vvi[i])
		return vvi

	def parse_vvvstring(self, str):
		pass

	def parse_line(self, line, types, fields):
		info = []
		values = line.split(",")
		if len(values) != len(fields):
			print("warning invaild line: {0}".format(line))
			return 
		for i in range(0,len(types)):
			t = types[i]
			f = fields[i]
			v = values[i]
			if t == "vector<vector<int>>":
				info.append(self.parse_vvint(v))
			elif t == "vector<vector<string>>":
				info.append(self.parse_vvstring(v))
			elif t == "vector<int>":
				info.append(self.parse_vint(v))
			elif t == "vector<string>":
				info.append(self.parse_vstring(v))
			elif t == "string":
				info.append(self.parse_string(v))
			elif t == "int":
				info.append(self.parse_int(v))
			else:
				print("unsupport type : " + t)

		return info

	def parse(self, path):
		print(path)
		with open (path, 'rb') as file:
			buff = file.read()
			content = buff.decode('utf-8')
			# content = content.encode('utf-8').decode('utf-8')
			lines = content.split("\r\n")
			index = 1
			csvinfo = {}
			csvinfo["content"] = []
			csvinfo["keymap"] = {}
			self.csvinfo = csvinfo
			for line in lines:
				if index == 1:
					pass
				elif index == 2:
					csvinfo['types'] = self.parse_types(line)
				elif index == 3:
					csvinfo['fields'] = self.parse_fields(line)
				elif len(line) > 0 and line[0] == "#":
					pass
				else:
					# print(line)
					item = self.parse_line(line, csvinfo['types'], csvinfo['fields'])
					if item:
						# print(item)
						csvinfo["keymap"][item[0]] = len(csvinfo["content"]) 
						csvinfo["content"].append(item)
				index = index + 1	

			return csvinfo

	def save_to_lua(self, path):
		if os.path.exists(path):
			os.remove(path)

		token = os.path.split(path)[1]
		token = os.path.splitext(token)[0]
		with open (path, 'w', encoding='utf-8') as file:
			file.write("--------------------------------------------------------\n")
			file.write("--------------------自动生成，请勿修改--------------------\n")
			file.write("--------------------------------------------------------\n")

			# fields
			file.write("local fields = {")
			for field in self.csvinfo["fields"]:
				file.write("\"{0}\",".format(field))
			file.write("}\n")

			# fieldmap
			file.write("local fieldmap = {")
			i = 1
			for field in self.csvinfo["fields"]:
				file.write("[\"{0}\"]={1},".format(field, i))
				i = i + 1
			file.write("}\n")

			# keymap
			file.write("local keymap = {")
			for (k,v) in self.csvinfo["keymap"].items():
				file.write("[{0}]={1},".format(k, v))
			file.write("}\n")

			# content
			file.write("local content = {\n")
			for v in self.csvinfo["content"]:
				s = str(v).replace("[", "{").replace("]", "}").replace("\'", "\"").replace(":", "=")
				file.write("\t{0},\n".format(s))
			file.write("}\n")
			
			file.write("\n")
			file.write("return {\n")
			file.write("\tfileds=fields,\n")
			file.write("\tfieldmap=fieldmap,\n")
			file.write("\tkeymap=keymap,\n")
			file.write("\tcontent=content,\n")
			file.write("}")







	

