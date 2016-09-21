import csv
import string
import requests
import bs4

results = requests.get('http://grad-schools.usnews.rankingsandreviews.com/best-graduate-schools/top-engineering-schools/eng-rankings?int=a74509')

reqSoup = bs4.BeautifulSoup(results.text, "html.parser")
i = 0
schools = []


whitelist = string.printable + string.whitespace

def clean(s):
	return "".join(c for c in s if c in whitelist)

for school in reqSoup:
	x = reqSoup.find_all("a", {"class" : "school-name"})
	while i < len(x):
		for name in x:
			y = x[i].get_text()
			i += 1
			schools.append(y)
			
with open('usnwr_schools.csv', 'w', '') as f:
	writer = csv.writer(f)
	for y in schools:
		clean(y)
		writer.writerow([y.encode('utf-8')])