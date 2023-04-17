import random
import string
import sys
import pandas as pd

sys.path.append("../tools")
from mysqlConnect import mysqlObject
from configReader import configReader
import datetime


activation_code = string.ascii_uppercase + "0123456789"


def generate(num, length):
    result = []
    for i in range(num):
        code = ""
        for j in range(length):
            code += random.choice(activation_code)
        result.append(code)
    df_result = pd.DataFrame(
        {"code": result, "generate_date": [str(datetime.datetime.today().date())] * num}
    )
    return df_result


if __name__ == "__main__":
    environment = sys.argv[1]
    mysqlAnalysisConfig = configReader("../config/config.ini").readDBInfo(
        "-".join(["mysql-analysis", environment])
    )
    mysqlAnalysis = mysqlObject(*mysqlAnalysisConfig)

    df = generate(2, 30)
    mysqlAnalysis.writeData(df, "inviteCode", "aiuser", if_exists="append")
