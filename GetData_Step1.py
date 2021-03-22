import requests
from copyheaders import headers_raw_to_dict
import random
import time
from bs4 import BeautifulSoup

request_url = "https://www.nowcoder.com/intern/center?recruitType=1&page="

headers = b"""
Host: www.nowcoder.com
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
DNT: 1
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://www.nowcoder.com/intern/center?recruitType=1&page=2
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cookie: NOWCODERCLINETID=6BA95FFCC77201CABB7BA3862364009B; NOWCODERUID=3BFD362BC6BD0044D7C01AAB17BC1201; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1615960908; gr_user_id=b7308f0f-d1b6-4e13-9526-0a1c86aa7521; dc_pid_set_next_pre=572152_594516_600910_602588_614427_616182_615224_616041_615490_616203_614573_588635_613708_616200_615804_615826_613549_614916_616202_615371_615755_616201_616198_448228_616123_610410_613573_616103_608599_616138_614878_616196_616199; c196c3667d214851b11233f5c17f99d5_gr_session_id=c60f531f-0322-4b75-94aa-d6a90481b6bb; c196c3667d214851b11233f5c17f99d5_gr_session_id_c60f531f-0322-4b75-94aa-d6a90481b6bb=true; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1616120161; SERVERID=20209ceebe066108970cd5046744d133|1616120155|1616120150
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


def GetSinglePage(request_url, headers, USER_AGENTS,PageNu):
    headers = headers_raw_to_dict(headers)
    headers["User-Agent"] = random.choice(USER_AGENTS)

    response = requests.get(url=request_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.find(name="div", attrs={"class": "empty-tip-mod"}):
        return False

    FileName = "Page"+str(PageNu)+" "+str(time.strftime("%D-%H-%M-%S", time.localtime(time.time())))
    with open(
        f"./HtmlFiles/Step1/{FileName}.html",
        "w+",
        encoding="utf-8",
    ) as f:
        f.write(response.text)

    All = soup.findAll(name="li", attrs={"class": "clearfix"})

    SinglePageInfo = []

    for single in All:
        name = single.find(name="a", attrs={"class": "reco-job-title"})
        name = name.get_text().replace(",", " ") if name else "Null"

        company = single.find(name="div", attrs={"class": "reco-job-com"})
        company = company.get_text().replace(",", " ") if company else "Null"

        link = single.find(name="a", attrs={"class": "reco-job-title"})
        link = (
            "https://www.nowcoder.com" + link.get("href").replace(",", " ")
            if link
            else "Null"
        )

        salary = single.find(name="span", attrs={"class": "ico-nb"})
        salary = salary.parent.get_text().replace(",", " ") if salary else "Null"

        add = single.find(
            name="span", attrs={"class": "nk-txt-ellipsis js-nc-title-tips job-address"}
        )
        add = add.get_text().replace(",", " ") if add else "Null"

        Mult = single.find(name="div", attrs={"class": "reco-job-status"})
        SuccessRate = Mult.get_text().replace(",", " ").replace("简历处理率：", "").split()[0]
        AverageTime = Mult.get_text().replace(",", " ").replace("平均处理：", "").split()[1]

        StatueTag = single.find(name="span", attrs={"class": "job-status-tag"})
        StatueTag = StatueTag.get_text().replace(",", " ") if StatueTag else "Null"

        SinglePageInfo.append(
            [name, company, link, salary, add, SuccessRate, AverageTime, StatueTag]
        )

    return SinglePageInfo


if __name__ == "__main__":

    AllInfo = []

    for i in range(500):
        time.sleep(0.5)
        i += 1
        tmp = GetSinglePage(request_url + str(i), headers, USER_AGENTS,i)
        if tmp:
            print(f"Page {i} get successful!")
            AllInfo.extend(tmp)
        else:
            print("Not Found!")
            break

    FileName = time.strftime("%D-%H-%M-%S", time.localtime(time.time()))
    with open(
        f"./Result/Step1/{FileName}.csv",
        "w+",
        encoding="utf-8",
    ) as f:
        for i in AllInfo:
            for j in i:
                f.write(f"{str(j)},")
            f.write("\n")
