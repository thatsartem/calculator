import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from models import Directions
from database import SessionLocal
from sqlalchemy import insert


di = {
    'Математика(профиль)' : 1,
    'Русский язык': 2,
    'Информатика': 3,
    'Физика': 4,
    'Литература': 5,
    'География': 6,
    'Химия': 7,
    'История': 8,
    'Биология': 9,
    'Обществознание': 10,
    'Иностранный язык': 11
}

link1 = "https://abitur.mtuci.ru/admission/firstcourse_budget/detail.php?ide=4099&ids=356"
link2 = "https://abitur.mtuci.ru/admission/firstcourse_budget/detail.php?ide=5663&ids=356"
link3 = "https://abitur.mtuci.ru/admission/firstcourse_budget/detail.php?ide=4027&ids=356"
links = [
    (link1,'Очная'),
    (link2,'Очно-заочная'),
    (link3,'Заочная')
]

data = []

for link, form in links:
    s = HTMLSession()
    r = s.get(link)
    r.html.render(timeout=20,wait=1,sleep=4)
    html_code = r.html.raw_html

    soup = BeautifulSoup(html_code, 'lxml')

    table = soup.find('table', id='learning_areas')

    table_rows = table.find_all('tr', class_='tr')

    for row in table_rows:
        name = row.find('a', id='name_wrk1', class_='show_bio')
        for i in name.find_all('i'):
            i.extract()
        code = name.get_text().split('-')[0].strip()
        name = name.get_text().split('-')[1].strip()
        t = row.find('table')
        sec = t.find_all('tr')[1]
        columns = sec.find_all('td')

        subjects = columns[0].get_text(strip=True)
        matches = re.findall(r'\d+\.(.*?)(?=\d+\.|$)', subjects)
        combined_lists = [[]]        
        new_lists = []
        for element in matches:
            if "/" in element:
                split_elements = element.split("/")
                new_lists.append(split_elements)
            else:
                new_lists.append([element])

        for sublist in new_lists:
            new_combined_lists = []
            for element in sublist:
                for combined_list in combined_lists:
                    new_combined_lists.append(combined_list + [di[element]])
            combined_lists = new_combined_lists
            
        budget_seats = int(columns[1].get_text(strip=True))
        passing_score = columns[2].get_text(strip=True)
        paid_seats = int(columns[3].get_text(strip=True))
        tuition_fee = int(columns[4].get_text(strip=True).replace(" ",""))
        for subjects in combined_lists:
            data.append({
                'university': 'Московский Технический Университет Связи и Информатики',
                'code': code,
                'name': name,
                'form': form,
                'subjects': subjects,
                'budget_seats': budget_seats,
                'passing_score': None if passing_score=='-' else int(passing_score),
                'paid_seats': paid_seats,
                'tuition_fee': tuition_fee,
                'link': link
            })


with SessionLocal() as session:
    session.execute(
        insert(Directions),data
    )
    session.commit()



print('insertion completed')
