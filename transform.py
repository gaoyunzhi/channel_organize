import yaml
from telegram.ext import Updater

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)
bot = Updater(credential['bot'], use_context=True).bot
debug_group = bot.get_chat(-1001198682178)

with open('category') as f:
	lines = f.readlines()

result = []
count = 0 
for line in lines:
	if not line.strip():
		debug_group.send_message('\n'.join(result), parse_mode='html') 
		result = []
		count = 0
	if 'https' not in line:
		result.append(line)
		continue
	url = line.split()[-1]
	text = line[:-len(url)-2]
	for c in '。【】# ':
		text = text.strip(c)
	count += 1
	result.append('%d. <a href="%s">%s</a>' % (count, url, text))

debug_group.send_message('\n'.join(result), parse_mode='html') 

# with open('result.html', 'w') as f:
# 	f.write('<br/>'.join(result))