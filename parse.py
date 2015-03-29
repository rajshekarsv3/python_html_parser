from bs4 import BeautifulSoup
from lxml import etree
import xlrd
from xlrd import open_workbook
from xlwt import easyxf
from datetime import datetime
import re
import const
import xlutils
from xlutils.copy import copy


class ParserClass:
	file_header = []
	keys_in_html = []
	file_content = ''
	work_book = ''
	sheet = ''
	dict_from_html = {}
	dict_from_workbook = {}
	index_of_current_year_in_html = ''
	index_of_previous_year_in_html = ''
	index_of_previous_year_in_xls = ''
	index_of_current_year_in_xls = ''
	keys_in_excel = []
	sheet_index = ''

	def __init__(self,html_file):
		i=0
		f    = open(html_file,"r")
		data = f.read()
		self.file_content = BeautifulSoup(data, "lxml")

	def get_table(self,table_heading):
		para = self.file_content.find('div',text=re.compile(table_heading))
		print para;
		if(para):
			required_table = para.find_next_sibling('table');
			if(not required_table):
				next_sibling = para.parent.find_next_sibling('div');
				required_table = next_sibling.find('table')
				print required_table
		else:
			print 'No table with Given name'
			return 0
		return required_table


	def get_heading_row(self,table_row):
		table_row = table_row.find_next_sibling('tr').find_next_sibling('tr').find_next_sibling('tr')
		for cell in table_row.findAll('td'):
			if cell.getText():
				self.file_header.append(cell.getText().replace('\n', '').replace('\r', '').replace('       ',' '))
		print self.file_header
		


	def get_all_column(self,table_content):
		for row in table_content.findAll('tr'):
			for cell in row.findAll('td'):
				print cell.getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ')


	def read_excel(self,excel_name,sheet_index):
		self.sheet_index = sheet_index
		self.work_book = open_workbook(excel_name, formatting_info=True)
		self.sheet = self.work_book.sheet_by_index(sheet_index);
		print 'Sheet Added:',self.sheet.name
	
		#print xlrd.xldate_as_tuple(self.sheet.cell(0,1).value,self.work_book.datemode)
		#print self.sheet.cell(0,1).value
		for row in range(self.sheet.nrows):
			temp_list = []
		 	for col in range(1,self.sheet.ncols):
			 	if self.sheet.cell(row,col).value:
		 			temp_list.append(self.sheet.cell(row,col).value)
		 	common_word = str(self.get_common_word_matching_key(self.sheet.cell(row,0).value.strip()))
		 	temp_list.insert(0,common_word)
		 	self.keys_in_excel.append(common_word)
		 	self.dict_from_workbook[self.sheet.cell(row,0).value.strip()] = temp_list
		print self.keys_in_excel



	#month and year for which the value should be generated is passed here
	def month_year_in_html(self,month,year):
		temp_list_to_store_month_and_year_index = []
		for each_header in self.file_header:
			for each_name in const.month_dict[month]:
				if each_name in each_header:
					if (str(year) in each_header or str(year+2000) in each_header):
						temp_list_to_store_month_and_year_index.append(self.file_header.index(each_header))
		if len(temp_list_to_store_month_and_year_index) == 0:
			print "no data matching the given input year"
		elif len(temp_list_to_store_month_and_year_index) > 1:
			for val in temp_list_to_store_month_and_year_index:
				if str('Three') in self.file_header[val]:
					self.index_of_current_year_in_html = val
		else:
			print temp_list_to_store_month_and_year_index
			self.index_of_current_year_in_html = temp_list_to_store_month_and_year_index[0]
		temp_list_to_store_month_and_year_index = []
		for each_header in self.file_header:
			for each_name in const.month_dict[month]:
				if each_name in each_header:
					if (str(year-1) in each_header or str(year+2000-1) in each_header):
						temp_list_to_store_month_and_year_index.append(self.file_header.index(each_header))
		if len(temp_list_to_store_month_and_year_index) == 0:
			print "no data matching the given input year"
		elif len(temp_list_to_store_month_and_year_index) > 1:
			for val in temp_list_to_store_month_and_year_index:
				if str('Three') in self.file_header[val]:
					self.index_of_previous_year_in_html = val
		else:
			self.index_of_previous_year_in_html = temp_list_to_store_month_and_year_index[0]
		print self.index_of_previous_year_in_html
		print self.index_of_current_year_in_html

		
	def form_dict_from_html(self,table_content):
		for row in table_content.findAll('tr'):
			row_cells = row.findAll('td');
			temp_list = []
			length = len(row_cells)
			for i in range(1,length):
				temp_list.append(row_cells[i].getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ').strip())
			common_word = str(self.get_common_word_matching_key(row_cells[0].getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ').strip()))
			temp_list.insert(0,common_word)
			self.keys_in_html.append(common_word)
			self.dict_from_html[row_cells[0].getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ').strip()] = temp_list
		#print self.keys_in_html
			

	def get_common_word_matching_key(self,word):
		common_word = ''
		for key,each_word in const.common_word.iteritems():
			if word in each_word:
				common_word = key

		return common_word

	def month_year_in_excel(self,month,year):
		temp_list = []
		index = 0
		previous_year = year-1
		
		for cell in self.sheet.row(2):
			
			if cell.value and cell.ctype==3:
				temp_list = xlrd.xldate_as_tuple(cell.value,self.work_book.datemode)
				if(temp_list[0]==previous_year and temp_list[1]==month):
					self.index_of_previous_year_in_xls = index
				if(temp_list[0]==year and temp_list[1]==month):
					self.index_of_current_year_in_xls = index
			index += 1
		print self.index_of_previous_year_in_xls
		if(not self.index_of_current_year_in_xls):
			self.index_of_current_year_in_xls=index+1;
		print self.index_of_current_year_in_xls
	
	def display_difference(self):
		print "Elements present in html but not in excel########"
		print list(set(self.keys_in_html)-set(self.keys_in_excel))
		print "Elements present in Excel but not in html########"		
		print list(set(self.keys_in_excel)-set(self.keys_in_html))

	def write_sheet(self):
		copy_work_book = copy(self.work_book);
		write_sheet = copy_work_book.get_sheet(self.sheet_index)
		
		for row in range(self.sheet.nrows):
			if self.sheet.cell(row,0).value:
				common_word=str(self.get_common_word_matching_key(self.sheet.cell(row,0).value.strip()))
				index = self.get_index_from_html_dict(common_word)
				if common_word:
					write_sheet.write(row,self.index_of_current_year_in_xls,self.dict_from_html[index][self.index_of_current_year_in_html])
				print self.dict_from_html[index][self.index_of_current_year_in_html]
			index = None
		copy_work_book.save('output.xls')
		#  	common_word = str(self.get_common_word_matching_key(self.sheet.cell(row,0).value.strip()))
		#  	temp_list.insert(0,common_word)
		#  	self.keys_in_excel.append(common_word)
		#  	self.dict_from_workbook[self.sheet.cell(row,0).value.strip()] = temp_list

	def get_index_from_html_dict(self,common_word):
		result = ''
		for key,each_word in self.dict_from_html.iteritems():
			if common_word in each_word:
				result = key

		return result

		





html_analysis = ParserClass("new.html")
parsed_table = html_analysis.get_table("Condensed Consolidated Statements of Operations")
if(parsed_table!=0):
	heading_row = html_analysis.get_heading_row(parsed_table.find('tr'))
	html_analysis.form_dict_from_html(parsed_table)
	html_analysis.read_excel('ELX.xls',0)
	html_analysis.month_year_in_html('9',14)
	html_analysis.month_year_in_excel(9,2014)
	html_analysis.display_difference()
	html_analysis.write_sheet()
	print html_analysis.file_header
print html_analysis.dict_from_html


