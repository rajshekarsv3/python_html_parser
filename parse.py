from bs4 import BeautifulSoup
from lxml import etree
import xlrd
from xlrd import open_workbook
from datetime import datetime
import re
import const


class ParserClass:
	file_header = []
	file_content = ''
	work_book = ''
	sheet = ''
	dict_from_html = {}
	dict_from_workbook = {}
	index_of_current_year_in_html = ''
	index_of_previous_year_in_html = ''
	index_of_previous_year_in_html = ''

	def __init__(self,html_file):
		i=0
		f    = open(html_file,"r")
		data = f.read()
		self.file_content = BeautifulSoup(data, "lxml")

	def get_table(self,table_heading):
		para = self.file_content.find('p',text=re.compile(table_heading))
		required_table = para.find_next_sibling('table');
		return required_table


	def get_heading_row(self,table_row):
		for cell in table_row.findAll('td'):
			if cell.getText():
				self.file_header.append(cell.getText().replace('\n', '').replace('\r', '').replace('       ',' '))
		


	def get_all_column(self,table_content):
		for row in table_content.findAll('tr'):
			for cell in row.findAll('td'):
				print cell.getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ')


	def read_excel(self,excel_name,sheet_name):
		self.work_book = open_workbook(excel_name)
		self.sheet = self.work_book.sheet_by_name(sheet_name);
		print 'Sheet Added:',self.sheet.name
		#print xlrd.xldate_as_tuple(self.sheet.cell(0,1).value,self.work_book.datemode)
		#print self.sheet.cell(0,1).value
		for row in range(self.sheet.nrows):
			temp_list = []
		 	for col in range(1,self.sheet.ncols):
			 	if self.sheet.cell(row,col).value:
		 			temp_list.append(self.sheet.cell(row,col).value)
		 	temp_list.insert(0,str(self.sheet.cell(row,0).value.strip()))
		 	self.dict_from_workbook[self.sheet.cell(row,0).value.strip()] = temp_list
		print self.dict_from_workbook



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
			self.index_of_current_year_in_html = temp_list_to_store_month_and_year_index[1]
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
			self.index_of_previous_year_in_html = temp_list_to_store_month_and_year_index[1]
		print self.index_of_previous_year_in_html
		print self.index_of_current_year_in_html
		





	def form_dict_from_html(self,table_content):
		for row in table_content.findAll('tr'):
			row_cells = row.findAll('td');
			temp_list = []
			length = len(row_cells)
			for i in range(1,length):
				temp_list.append(row_cells[i].getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ').strip())
			temp_list.insert(0,str(self.get_common_word_matching_key(row_cells[0].getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ').strip())))

			self.dict_from_html[row_cells[0].getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ').strip()] = temp_list
			#self.dict_from_html.setdefault(row_cells[0].getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' '), temp_list)
		print self.dict_from_html
			# for cell in row.findAll('td'):
			# 	print cell.getText().replace('\n', '').replace('\r', '').replace('       ',' ').replace('     ',' ')

	def get_common_word_matching_key(self,word):
		common_word = ''
		for key,each_word in const.common_word.iteritems():
			if word in each_word:
				common_word = key

		return common_word



		





html_analysis = ParserClass("data.htm")
parsed_table = html_analysis.get_table("Unaudited Condensed Consolidated Interim Statements")
heading_row = html_analysis.get_heading_row(parsed_table.find('tr'))
html_analysis.form_dict_from_html(parsed_table)
html_analysis.read_excel('Model.xlsx','html')
html_analysis.month_year_in_html('9',14)
#print html_analysis.file_header
#print parsed_table