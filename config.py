config = {
'teamid'        :'TheMulti-ArmedBandits',
'teampw'        :'bb3d9c0ea5aaab61db6f035e7de4870c',
'contexturl'    :'http://krabspin.uci.ru.nl/getcontext.json/',
'proposeurl'    :'http://krabspin.uci.ru.nl/proposePage.json/',
'saveinterval'  : 1000,
'updateinterval': 1,
'max_its'       :1000,
'metamodel': {
		'run_id_min'    : 0,
		'run_id_max'    : 10000,
		'trainits'      : 100,
		'testits'       : 10,
		'conv_threshold': 1.1#,
	},
'variables': [
		'header',
		'adtype',
		'color',
		'productid',
		'price',
		'ID',
		'Agent',
		'Language',
		'Referer',
		'Age'#,
	]#,
}

