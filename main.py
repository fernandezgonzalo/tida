import os
import json
from Tida import Tida

CONFIG_FILE_NAME = "~/.tida_config.json"
ABS_CONFIG_FILE = os.path.expanduser(CONFIG_FILE_NAME)

def load_config(file_name):
	return json.loads(open(file_name, 'r').read())

def create_config(file_name):
	config = {}
	config['decorated'] = False
	config['skip_taskbar_hint'] = True
	config['keep_above'] = True
	config['skip_pager_hint'] = False
	config['modal'] = False
	config['width'] = 720
	config['heigth'] = 300
	config['key_copy_to_clipboard'] = "<Ctrl><Shift>C"
	config['key_paste_from_clipboard'] = "<Ctrl><Shift>V"
	config['key_toggle_visibility'] = "F12"
	config['shell'] = '/usr/bin/bash'
	config['scrollback_lines'] = -1

	try:
		f = open(file_name, 'w')
		config_dump = json.dumps(config)
		f.write(config_dump)
		f.close()
		return config
	except:
		pass
	return None


if os.path.exists(ABS_CONFIG_FILE):
	config = load_config(ABS_CONFIG_FILE)
else:
	config = create_config(ABS_CONFIG_FILE)

Tida(config=config)

