import itertools
import csv
import requests
import bs4

def getSchools(names):
#get list of school names
	schools = []
	i = 0
	while i < len(names):
		for name in names:
			schoolname = names[i].get_text()
			i += 1
			schools.append(schoolname)
	return schools

def getScores(tableAll):
#get list of program scores
	scores = []
	i = 0
	while i < len(tableAll[0].select('.rankscore-bronze')):
		for score in tableAll[0].select('.rankscore-bronze'):
			number = tableAll[0].select('.rankscore-bronze')[i].get_text()
			i += 1
			scores.append(number)
	return scores


#schools = []
#scores = []
					
nationalUrl = 'http://grad-schools.usnews.rankingsandreviews.com/best-graduate-schools/'

program = [ 'top-engineering-schools/eng-rankings/', 
			'top-science-schools/biological-sciences-rankings', 
			'top-science-schools/chemistry-rankings', 
			'top-science-schools/computer-science-rankings', 
			'top-science-schools/mathematics-rankings', 
			'top-science-schools/physics-rankings'
			]

rankings = {}
i = 0
while i < len(program): 
	results = requests.get(nationalUrl + program[i])
	reqSoup = bs4.BeautifulSoup(results.text, "html.parser")
	tableAll = reqSoup.find_all('tbody') #save entire webpage table as bs object
	names = reqSoup.select('.school-name')  #save school name classes as bs object
	schools = getSchools(names)
	scores = getScores(tableAll)
	for j, school in enumerate(schools):
		if school not in rankings:
			rankings[school] = {'School': school, program[i]: scores[j]}
		else:
			rankings[school].update({program[i]: scores[j]})
	i += 1

			
#print(schools, scores)
print(rankings)

# with open('usnwr_schools.csv', 'w') as f:
# 	writer = csv.writer(f)
# 	for school, score in zip(schools, scores):
# 		writer.writerow([school.encode('utf-8'), score])
with open('usnwr_schools.csv', 'w') as f:
	writer = csv.DictWriter(f, fieldnames=['School'] + program)
	writer.writeheader()
	for row in rankings:
		writer.writerow(rankings[row])
