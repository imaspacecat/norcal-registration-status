import requests as req
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}

teams_url = "https://www.norcalftc.org/norcal-ftc-team-list-new/"
team_status_base_url = "https://www.norcalftc.org/ftc-team-status/?ftcteam="  # 524

teams = []
with open("teams.txt", "r") as f:
    teams = f.readlines()
    f.close()


def scrape_team_status(team_number):
    team_status_url = f"{team_status_base_url}{team_number}"
    res = req.get(team_status_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    td = soup.find("table").find_all("td")

    qt_status = []
    for i in range(len(td)):
        if "QT" in td[i].text:
            qt_status.append(td[i + 1].text)

    print([team_number] + qt_status)
    return dict(zip(qt_status[::2], qt_status[1::2]))


csv_filename = "team_status.csv"
with open(csv_filename, mode="w", newline="") as file:
    fieldnames = ["Team Number", "QT #1", "QT #2", "QT #3"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for i, team_number in enumerate(teams):
        result = scrape_team_status(team_number)
        print(type(result))
        writer.writerow({"Team Number": int(team_number)} | result)

    file.close()
