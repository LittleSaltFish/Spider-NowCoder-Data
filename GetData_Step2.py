import re
import requests
from copyheaders import headers_raw_to_dict
import random
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import csv

headers = b"""
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: NOWCODERUID=CC80530AEA0BC80BA485EFEC2C5FEED9; NOWCODERCLINETID=5EBD6241A433575A1B6057A637D47577; SERVERID=f24cbffaf8c883b27da19f52fb8cda88|1616308371|1616308371
DNT: 1
Host: www.nowcoder.com
sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
"""

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
]


def GetMoreMessage(request_url, headers, USER_AGENTS):
    headers = headers_raw_to_dict(headers)
    headers["User-Agent"] = random.choice(USER_AGENTS)

    response = requests.get(url=request_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    JobStyle, TimeRequirement, UpChance, Duty, SkillRequirement = (
        "Null",
        "Null",
        "Null",
        "Null",
        "Null",
    )

    if soup.find_all(text="该职位已下线"):
        return ["Null", "Null", "Null", "Null", "Null"]

    FileName = str(time.strftime("%Y-%H-%M-%S", time.localtime(time.time())))
    with open(f"./HtmlFiles/Step2/{FileName}.html", "w+", encoding="utf-8") as f:
        f.write(response.text)

    try:
        JobStyle = soup.find(name="i", attrs={"class": "job-ico job-ico1"})
        JobStyle = (
            JobStyle.parent.get_text().replace(",", " ").replace("\n", " ")
            if JobStyle
            else "Null"
        )

        Addition = soup.find(text=re.compile(".*转正机会.*"))
        Addition = (
            Addition.replace(",", "").replace("\xa0", "").replace(" ", "")
            if Addition
            else "Null"
        ).split("|")

        TimeRequirement = (
            Addition[1].replace("实习要求：", "")
            if len(Addition) == 3 and Addition[1]
            else "Null"
        )

        UpChance = (
            Addition[2].replace("转正机会：", "")
            if len(Addition) == 3 and Addition[2]
            else "Null"
        )

        Describe = soup.findAll(
            name="div", attrs={"class": "nc-post-content js-duty-content"}
        )

        Duty = (
            Describe[0].get_text().replace(",", " ").replace("\n", " ")
            if len(Describe) > 0
            else "Null"
        )

        SkillRequirement = (
            Describe[1].get_text().replace(",", " ").replace("\n", " ")
            if len(Describe) > 1
            else "Null"
        )

    except Exception as e:
        print(e)

    return [JobStyle, TimeRequirement, UpChance, Duty, SkillRequirement]


if __name__ == "__main__":
    JudgeLength = 2.5
    SleepTime = 0.1
    Filename = time.strftime("%Y-%H-%M-%S", time.localtime(time.time()))
    with open("Data_Step1.csv", "r", encoding="utf-8") as csvFileRead, open(
        f"./Result/Step2/{Filename}.csv", "a+", encoding="utf-8"
    ) as csvFileWrite:
        Reader = csv.reader(csvFileRead)
        for i, j in zip(Reader, tqdm(range(5000))):
            time.sleep(SleepTime)
            Time1 = time.time()
            tmp = GetMoreMessage(i[2], headers, USER_AGENTS)
            Time2 = time.time()
            if Time2 - Time1 >= JudgeLength:
                SleepTime *= 2
            else:
                SleepTime = 0.5
            for j in i:
                csvFileWrite.write(f"{j},")
            for k in tmp:
                csvFileWrite.write(f"{k},")
            csvFileWrite.write("\n")
