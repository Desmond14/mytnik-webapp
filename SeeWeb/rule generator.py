
import json

main_dict = {}

############## filters for rule 1 ###################

filter = {}
filter['BillofLading'] = '867034156'
filter['OriginPort'] = 'CNSHA'
filter['DischargePort'] = 'FIKTK'
filter['ArrivalPort'] = 'PLGDN'
filter['PackagesDescType'] = 'CARTONS'


#####################################################

rule_1 = {
	"severity" : 1,
	'filter_type': "AND",
	"filters" : filter
}

############## filters for rule 1 ###################

filter = {}
filter['BillofLading'] = '867034156'
filter['OriginPort'] = 'CNSHA'
filter['DischargePort'] = 'FIKTK'
filter['ArrivalPort'] = 'PLGDN'
filter['PackagesDescType'] = 'CARTONS'


#####################################################


rule_2 = {
	"severity" : 2,
	'filter_type': "OR",
	"filters" : filter
}


main_dict[1] = rule_1
main_dict[2] = rule_2


tmp_file = open('tmp.json', 'w+')
tmp_file.write(json.dumps(main_dict))
