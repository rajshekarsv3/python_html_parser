from bs4 import BeautifulSoup
from lxml import etree
from xlrd import open_workbook
import re
import const


class ParserClass:
	file_header = []
	file_content = ''
	work_book = ''
	sheet = ''

	def __init__(self,html_file):
		i=0
		f    = open(html_file,"r")
		data = f.read()
		self.file_content = BeautifulSoup(data, "lxml")

	def get_table(self,table_heading):
		para = self.file_content.find('p',text=re.compile(table_heading))
		required_table = para.find_next_sibling('table');
		return required_table
		#results = {}
		#for row in required_table.findAll('tr'):
		#     aux = row.findAll('td')
		#     print aux.text()

		# print results
		#print(para.find_next_sibling('p').getText())
		#while(para.find_next_sibling('p') not in const.table_name):
			#para = para.find_next_sibling('p')
			#print(para.find_next_sibling('p').getText())
			
			
		# print(self.file_content.body.find_next_siblings('p'))
		# print(self.file_content.body.find_next_siblings('p'))
		#print(self.file_content.contents)

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


	def check_for_month_year_in_html(self,month,year):
		for each_header in self.file_header:
			for each_name in const.month_dict[month]:
				if each_name in each_header:
					if str(year) in each_header:
						print each_header





		# values = []
		# for row in range(s.nrows):
			
		#  	#for col in range(s.ncols):
		#  	if s.cell(row,0).value:
	 # 			values.append(s.cell(row,0).value)
		# print str(values)
			 


		





html_analysis = ParserClass("data.htm")
parsed_table = html_analysis.get_table("Unaudited Condensed Consolidated Interim Statements")
heading_row = html_analysis.get_heading_row(parsed_table.find('tr'))
#html_analysis.get_all_column(parsed_table)
html_analysis.read_excel('Model.xlsx','html')
html_analysis.check_for_month_year_in_html('september',2013)
print html_analysis.file_header
#print parsed_table