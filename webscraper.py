from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv

my_url = "https://search.studyinaustralia.gov.au/course/search-results.html?qualificationid=12&subjectid=E&locationid=4"

udata = uReq(my_url)
page_html = udata.read()
udata.close()
page_soup = soup(page_html, "html.parser")

contents = page_soup.findAll("div", {"class": "sr_cont"})

data = []

for content in contents:
    college_name = content.find("h2", {"class": "univ_tit"}).text.strip()
    courses = content.findAll("div", {"class": "rs_cnt"})
    for course in courses:
        title = course.find("h3", {"class": "crs_tit univ_tit"})
        if title != None:
            course_title = title.text.strip()
            details = course.findAll("div", {"class": "fl_w100"})
            level_of_study = details[0].find("span").text
            start_date = details[2].find("span").text
            duration = details[3].find("span").text
            tuition_fee = details[4].find("span").text
            data.append((college_name, course_title, level_of_study, start_date, duration, tuition_fee))


with open('course.csv', mode='w') as csv_file:
    fieldnames = ['College Name', 'Course Title', 'Level of Study', 'Intakes', 'Duration', 'Tuition Fee']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for item in data:
        dict = {
            'College Name': item[0],
            'Course Title': item[1],
            'Level of Study': item[2],
            'Intakes': item[3],
            'Duration': item[4],
            'Tuition Fee': item[5]
        }
        writer.writerow(dict)