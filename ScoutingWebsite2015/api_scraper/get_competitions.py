'''
Created on Mar 11, 2016

@author: preiniger
'''


def get_week1_competitions(sql_basepath, json_basepath):

    sql_path = sql_basepath + "/week1"
    json_path = json_basepath + "/week1"

    event_codes = []
    event_codes.append((json_path, sql_path, "ONTO2"))
    event_codes.append((json_path, sql_path, "ISTA"))
    event_codes.append((json_path, sql_path, "MNDU"))
    event_codes.append((json_path, sql_path, "MNDU2"))
    event_codes.append((json_path, sql_path, "SCMB"))
    event_codes.append((json_path, sql_path, "CASD"))
    event_codes.append((json_path, sql_path, "VAHAY"))
    event_codes.append((json_path, sql_path, "MIKET"))
    event_codes.append((json_path, sql_path, "MISOU"))
    event_codes.append((json_path, sql_path, "MISTA"))
    event_codes.append((json_path, sql_path, "MIWAT"))
    event_codes.append((json_path, sql_path, "PAHAT"))
    event_codes.append((json_path, sql_path, "NJFLA"))
    event_codes.append((json_path, sql_path, "NCMCL"))
    event_codes.append((json_path, sql_path, "NHGRS"))
    event_codes.append((json_path, sql_path, "CTWAT"))
    event_codes.append((json_path, sql_path, "WAAMV"))
    event_codes.append((json_path, sql_path, "WASPO"))

    return event_codes


def get_week2_competitions(sql_basepath, json_basepath):

    sql_path = sql_basepath + "/week2"
    json_path = json_basepath + "/week2"

    event_codes = []
    event_codes.append((json_path, sql_path, "TXSA"))
    event_codes.append((json_path, sql_path, "AZFL"))
    event_codes.append((json_path, sql_path, "ARLR"))
    event_codes.append((json_path, sql_path, "CAMA"))
    event_codes.append((json_path, sql_path, "MOKC"))
    event_codes.append((json_path, sql_path, "PACA"))
    event_codes.append((json_path, sql_path, "ONTO"))
    event_codes.append((json_path, sql_path, "MXMC"))
    event_codes.append((json_path, sql_path, "NYNY"))
    event_codes.append((json_path, sql_path, "FLOR"))
    event_codes.append((json_path, sql_path, "MOSL"))
    event_codes.append((json_path, sql_path, "MDBET"))
    event_codes.append((json_path, sql_path, "VABLA"))
    event_codes.append((json_path, sql_path, "MIKE2"))
    event_codes.append((json_path, sql_path, "MILAK"))
    event_codes.append((json_path, sql_path, "MISJO"))
    event_codes.append((json_path, sql_path, "INWLA"))
    event_codes.append((json_path, sql_path, "NCRAL"))
    event_codes.append((json_path, sql_path, "MAREA"))
    event_codes.append((json_path, sql_path, "MAWOR"))
    event_codes.append((json_path, sql_path, "GACOL"))
    event_codes.append((json_path, sql_path, "WASNO"))
    event_codes.append((json_path, sql_path, "ORWIL"))

    return event_codes


def get_competitions_to_scrape():

    sql_path = "__api_scraping_results/database"
    json_path = "../__api_scraping_results/json"

    events = []
#     events.extend(get_week1_competitions(sql_path, json_path))
    events.extend(get_week2_competitions(sql_path, json_path))

    return events
