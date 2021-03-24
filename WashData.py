import jieba
import csv
from tqdm import tqdm

jieba.load_userdict("./Dictionary/IT_Dict.txt")

with open("./Result/Data_Step2.csv", "r", encoding="utf-8") as csvFileRead, open(
    f"./Result/Date_Wash.csv", "w+", encoding="utf-8"
) as csvFileWrite, open(
    f"./Result/RequireList.txt", "w+", encoding="utf-8"
) as csvFileWrite2:
    
    csvFileWrite.write(
            "JobName,Company,Url,Address,AddInfo,WorkStyle,UpgradeChance,MinSalary,MaxSalary,AveSalary,DayNeed,WeekNeed,SumNeed,ViewRate,AveSpeed,CutRequest\n"
            )
    
    Reader = csv.reader(csvFileRead)
    for line, i in zip(Reader, tqdm(range(5000))):

        MinSalary, MaxSalary, AveSalary = "Null", "Null", "Null"
        DayNeed, WeekNeed, SumNeed = "Null", "Null", "Null"
        CutRequest,ViewRate,AveSpeed = "Null", "Null", "Null"

        tmp = line[3].replace("¥", "").replace("元/天", "").split("-")
        if len(tmp) == 2:
            MinSalary, MaxSalary = tmp[0], tmp[1]
            AveSalary = (float(MinSalary) + float(MaxSalary)) / 2

        ViewRate = line[5].replace("简历处理率：", "").replace("-", "")
        ViewRate = ViewRate if ViewRate else "Null"

        AveSpeed = line[6].replace("平均处理：", "").replace("天", "").replace("-", "")
        AveSpeed = AveSpeed if AveSpeed else "Null"

        TimeNeed = line[9].replace("个月以上", "").split("天/周，")
        if len(TimeNeed) == 2:
            DayNeed, WeekNeed = TimeNeed[0], TimeNeed[1]
            SumNeed = int(DayNeed) * int(WeekNeed)

        if line[12] != "Null":
            Tmp = jieba.cut(line[12], cut_all="False")
            CutRequest = " ".join(jieba.cut(line[12], cut_all=False))

        for i in line[:3]+[line[4]]+line[7:9]+[line[10]]:
            csvFileWrite.write(f"{i},")
        csvFileWrite.write(
            f"{MinSalary},{MaxSalary},{AveSalary},{DayNeed},{WeekNeed},{SumNeed},{ViewRate},{AveSpeed},{CutRequest}"
            )
        csvFileWrite.write("\n")

        csvFileWrite2.write(CutRequest + " ")
