table_name = ["Unaudited Condensed Consolidated Interim Statements of Comprehensive Income","Unaudited Condensed Consolidated Interim Balance"]


month_dict = {
    '1' : ['jan','january'],
    '2' : ['feb','febraury'],
    '3' : ['mar','march'],
    '4' : ['apr','april'],
    '5' : ['may'],
    '6' : ['jun','june'],
    '7' : ['jul','july'],
    '8' : ['aug','august'],
    '9' : ['sept','September'],
    '10' : ['oct','october'],
    '11' : ['nov','november'],
    '12' : ['dec','december']
    }

common_word = {
	'Revenues' : ['revenue','Revenue','Revenues'],
	'Cost of sales' : ['Cost of sales'],
	'Gross profit' : ['Gross profit'],
	'Operating expenses' : ['Operating expenses:','Operating expenses'],
	'Selling and marketing expenses' : ['Selling and marketing expenses','S&M Expense'],
	'Administrative expenses' : ['Administrative expenses','Administrative exp.'],
	'Total operating expenses' : ['Total operating expenses','Total Opex'],
	'Other Net Income' : ['Other income, net','Other income, net'],
	'Profit before income taxes' : ['Profit before income taxes','PBT'],
	'Income Tax' : ['Income tax expense','Tax'],
	'Net profit' : ['Net profit','PAT'],
	'Basic EPS' : ['Basic EPS','Basic ($)'],
	'Diluted EPS' : ['Diluted EPS','Diluted ($)'],
	'Basic' : ['Basic'],
	'Diluted' : ['Diluted']
}