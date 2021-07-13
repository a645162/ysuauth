import json
import program_logs

jsonStr = "{\"errcode\":0,\"errmsg\":\"ok\"}"


def isDingTalkOk1(jsonStr):
    program_logs.print1("Parse JSON :" + jsonStr)
    if len(jsonStr) == 0:
        return False
    jsonArray = dict(json.loads(jsonStr))
    program_logs.print1("JSON Array :" + str(jsonArray))
    print(jsonArray)
    if list(jsonArray.keys()).index("errmsg") != -1:
        return jsonArray['errmsg'] == "ok"
    else:
        return False


def isDingTalkOk(jsonStr):
    r = isDingTalkOk1(jsonStr)
    program_logs.print1("isDingTalkOk :" + str(r))
    return r

# print(isDingTalkOk(jsonStr))
