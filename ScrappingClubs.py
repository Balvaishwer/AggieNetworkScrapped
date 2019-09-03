from bs4 import BeautifulSoup
import requests
import re



def getLinks():

    html_page = requests.get("https://www.aggienetwork.com/clubs/findmyclub.aspx")
    soup = BeautifulSoup(html_page.text, 'html.parser')
    n = 0
    for link in soup.findAll('a', attrs={'href': re.compile("^/club-page")}):
        print(link.get('href'))
        getData(link.get('href'))
        n  += 1
        if n == 1000:
            break


def getData(link):
    append = "https://www.aggienetwork.com"
    url = append + link
    print(url)
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.text, 'html.parser')
    clubInfo = soup.findAll("ul", {"class": "cleanLi"})[0]
    if clubInfo.a == None:
        Name = "Not Available"
    else:
        Name = str(clubInfo.a.contents[0])
        print("Name =", Name)
    if clubInfo.li.find_next_siblings('li')[2].a == None:
        Email = "Not Available"
    else:
        Email = clubInfo.li.find_next_siblings('li')[2].a.text
        print("Email =", Email)
    ClubTitle = soup.findAll("div", {"class": "cmsTitleWrap"})[0].h1.text
    ClubTitle = ClubTitle.lstrip()
    print("Title =", ClubTitle)
    writeFile(str(ClubTitle), str(Name), str(Email))

def writeFile(ClubTitle, Name, Email):
    file = open('AggieClubs.txt','a')
    file.write("%s, %s, %s\n" % (ClubTitle, Name, Email))
    file.close()





getLinks()

