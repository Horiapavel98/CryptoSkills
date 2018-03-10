import requests
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import numpy as np
import sys

def get_coin_prices_dates(symbol):
    url = 'https://cex.io/api/price_stats/' + symbol + '/USD'
    data = {"lastHours": 24, "maxRespArrSize": 119}
    resp = requests.post(url, data).json()
    #(len(resp))
    coin_data = []
    for i in range(len(resp)-96, len(resp)):
        coin_data.append(resp[i])
    round1 = []
    round2 = []
    round3 = []
    ret = []
    #print(len(coin_data))
    for i in range(0, 32):
        round1.append([int(coin_data[i]['tmsp']), float(coin_data[i]['price'])])
        round2.append([int(coin_data[i+32]['tmsp']), float(coin_data[i+32]['price'])])
        round3.append([int(coin_data[i+64]['tmsp']), float(coin_data[i+64]['price'])])
        #print(str(i) + " -- " + str(i+32) +  " -- " + str(i+64))
    ret.append(round1)
    ret.append(round2)
    ret.append(round3)
    return ret

def tmsp_to_str(tmsp):
    return dt.datetime.fromtimestamp(tmsp).strftime('%Y-%m-%d %H:%M:%S')

def get_avg_volat(symbol):
    resp = get_coin_prices_dates(symbol)
    res = []
    for unit in resp:
        for itm in unit:
            res.append(itm[1])
    return np.diff(np.log(res)).std()*np.sqrt(252)*100

def get_lst_volat(lst):
    return np.diff(np.log(lst)).std()*np.sqrt(252)*100

def get_diffs(dates_lst, true_lst, pred_lst):
    dates = np.array(dates_lst)
    true = np.array(true_lst)
    pred = np.array(pred_lst)
    ymax = max(pred_lst)
    ymin = min(pred_lst)
    avg_diff_lst = []
    avg_diff = 0
    max_diff = 0
    min_diff = sys.maxsize

    for i in range(0, len(dates)):
        val = abs(pred_lst[i] - true_lst[i]) * 100 / (ymax - ymin)
        avg_diff_lst.append(val)
        avg_diff += val
        if val >= max_diff:
            max_diff = val

        if val <= min_diff and i > 1:
            min_diff = val

    avg_diff = avg_diff / len(dates)
    res = {}
    res["avg"] = avg_diff
    res["min"] = min_diff
    res["max"] = max_diff
    res["vals"] = avg_diff_lst

    return res

def get_slopes(dates_lst, true_lst, pred_lst):
    dates = np.array(dates_lst)
    true = np.array(true_lst)
    pred = np.array(pred_lst)

    pred_slopes = []
    true_slopes = []
    correct_slopes = []
    slope_change = []
    avg_slope_change = 0
    correct_slopes_nr = 0

    for i in range(0, len(dates)-1):
        true_slopes.append(true[i+1]-true[i])
        pred_slopes.append(pred[i+1]-pred[i])

    for i in range(0, len(dates) - 1):
        if true_slopes[i]*pred_slopes[i] >= 0:
            correct_slopes.append(True)
            if true_slopes[i] != 0:
                slope_change.append(pred_slopes[i]/true_slopes[i])
            else:
                slope_change.append(1)
            avg_slope_change += slope_change[-1]
            correct_slopes_nr += 1
        else:
            correct_slopes.append(False)
            slope_change.append(False)

    if correct_slopes != 0:
        avg_slope_change_pcnt = (avg_slope_change*100)/correct_slopes_nr
        avg_slope_change = avg_slope_change/correct_slopes_nr
    result = {}
    result['avg_change'] = avg_slope_change
    result['avg_change_%'] = avg_slope_change_pcnt
    result['correct_slopes'] = correct_slopes_nr
    result['total_slopes'] = len(dates)-1
    result["slope_change"] = slope_change
    return result

def symbols_to_lists(symbol1, symbol2):
    symbol1 = get_coin_prices_dates(symbol1)
    symbol2 = get_coin_prices_dates(symbol2)

    date = []
    symbol1_val = []
    symbol2_val = []

    for unit in symbol1:
        for itm in unit:
            date.append(itm[0])
            symbol1_val.append(itm[1])

    for unit in symbol2:
        for itm in unit:
            symbol2_val.append((itm[1]))

    result = {}
    result["dates"] = date
    result["symbol1_val"] = symbol1_val
    result["symbol2_val"] = symbol2_val
    return result
