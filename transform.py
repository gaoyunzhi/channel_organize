with open('category') as f:
	lines = f.readlines()

result = []
for line in lines:
	if 'https' not in line:
		result.append(line)
		continue
	url = line.split()[-1]
	text = line[:-len(url)-2]
	for c in '。【】# ':
		text = text.strip(c)
	result.append('<a href="%s">%s</a>' % (url, text))

with open('result.html', 'w') as f:
	f.write('<br/>'.join(result))