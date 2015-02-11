from bs4 import BeautifulSoup
from lxml import etree
import re
import const


class ParserClass:

	file_content = ''

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

	def get_heading_column(self,table_row):
		for cell in table_row.findAll('td'):
			print cell.getText()

		





html_analysis = ParserClass("data.htm")
parsed_table = html_analysis.get_table("Unaudited Condensed Consolidated Interim Statements")
html_analysis.get_heading_column(parsed_table.find('tr'))
#print parsed_table