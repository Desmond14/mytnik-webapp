
import json
main_dict = {}
filter = {}                # operator #value
#filter['Filter_Column_1'] = ['>','xxxx'] #### Numbered value
#filter['Filter_Column_2'] = ['<','xxxx'] #### Numbered value
#filter['Filter_Column_3'] = ['>=','xxx'] #### Numbered value
#filter['Filter_Column_4'] = ['<=','xxx'] #### Numbered value
#filter['Filter_Column_n'] = ['like','xxx'] ### SQL rexp

alert_1 = {
	"severity" : 5,       ### Possible choice 1,2,3,4 .. n
	'filter_type': "AND", ### Possible choice AND OR
	"filters" : filter    ### DO NOT CHANGE
}
main_dict[1] = alert_1
tmp_file = open('alert.json', 'w+')
tmp_file.write(json.dumps(main_dict))