from flask import jsonify

from utils import query, query_noargs


# 获取天气城市数量统计
def get_weathers_total_data():
    xyt_sql = "SELECT COUNT(*) FROM weather WHERE is_old=0 and weather like '%雨%'"
    qt_sql = "SELECT COUNT(*) FROM weather WHERE is_old=0 and weather like '%晴%'"
    dy_sql = "SELECT COUNT(*) FROM weather WHERE is_old=0 and weather like '%多云%' "
    xt_sql = "SELECT COUNT(*) FROM weather WHERE is_old=0 and weather like '%雪%' "
    wt_sql = "SELECT COUNT(*) FROM weather WHERE is_old=0 and weather like '%雾%' "
    cm_sql = "SELECT COUNT(*) FROM weather WHERE is_old=0 and ( weather like '%霾%' OR weather like '%尘%') "
    xyt = query_noargs(xyt_sql)[0][0]
    qt = query_noargs(qt_sql)[0][0]
    dy = query_noargs(dy_sql)[0][0]
    xt = query_noargs(xt_sql)[0][0]
    wt = query_noargs(wt_sql)[0][0]
    cm = query_noargs(cm_sql)[0][0]
    return jsonify({"xyt": xyt, "qt": qt, "dy": dy, "xt": xt, "wt": wt, "cm": cm})


"""
AQI：
0-50良好
51-100:中等
101-150：偏差，对敏感人群不健康
151-200：差，不健康
201-300：极差，非常不健康
300+：有毒
"""


# 获取城市空气质量统计
def get_AQI_total_data():
    lh_sql = "SELECT COUNT(id) FROM weather WHERE aqi<=50 AND is_old=0"
    zd_sql = "SELECT COUNT(id) FROM weather WHERE aqi>50 AND aqi<=100 AND is_old=0"
    pc_sql = "SELECT COUNT(id) FROM weather WHERE aqi>100 AND aqi<=150 AND is_old=0"
    c_sql = "SELECT COUNT(id) FROM weather WHERE aqi>150 AND aqi<=200 AND is_old=0"
    jc_sql = "SELECT COUNT(id) FROM weather WHERE aqi>200 AND aqi<=300 AND is_old=0"
    yd_sql = "SELECT COUNT(id) FROM weather WHERE aqi>300 AND is_old=0"
    lh = query_noargs(lh_sql)[0][0]
    zd = query_noargs(zd_sql)[0][0]
    pc = query_noargs(pc_sql)[0][0]
    c = query_noargs(c_sql)[0][0]
    jc = query_noargs(jc_sql)[0][0]
    yd = query_noargs(yd_sql)[0][0]
    return jsonify([{"time": "良好", "value": lh, "name": "空气质量"},
                    {"time": "中等", "value": zd, "name": "空气质量"},
                    {"time": "偏差", "value": pc, "name": "空气质量"},
                    {"time": "较差", "value": c, "name": "空气质量"},
                    {"time": "极差", "value": jc, "name": "空气质量"},
                    {"time": "有毒", "value": yd, "name": "空气质量"}])


# 获取城市风力质量统计
def get_ws_total_data():
    ws_sql = "SELECT COUNT(id), ws FROM weather WHERE is_old=0 GROUP BY ws"
    ws = query_noargs(ws_sql)
    d = []
    for val, lv in ws:
        lv = str(lv) + "级"
        i = {"name": lv, "value": val}
        d.append(i)
    return jsonify(d)


# 获取城市风向统计
def get_wd_total_data():
    ws_sql = "SELECT COUNT(id), wd FROM weather WHERE is_old=0 GROUP BY wd"
    ws = query_noargs(ws_sql)
    d = []
    for val, lv in ws:
        lv = str(lv)
        i = {"name": lv, "value": val}
        d.append(i)
    return jsonify(d)


# 获取城市空气质量统计
def get_bg_total_data():
    bg_sql = "SELECT record_time,temp, wse FROM weather WHERE cityname='北京' AND  to_days(create_time) = to_days(now());"
    bg = query_noargs(bg_sql)
    d = []
    x = []
    for rt, temp, wse in bg:
        it = {"time": rt, "value": temp, "name": "温度"}
        iw = {"time": rt, "value": wse, "name": "凤速"}
        d.append(it)
        d.append(iw)
        x.append(rt)
    data = {"d": d, "x": x}
    return jsonify(data)


# 获取轮播数据
def get_qg_total_data():
    qg_sql = "SELECT cityname,weather ,temp,ws,wd,aqi FROM weather WHERE is_old=0"
    qg = query_noargs(qg_sql)
    d = []
    for cityname, weather, temp, ws, wd, aqi in qg:
        it = {"城市": cityname, "天气": weather, "温度": temp, "风级": (str(ws) + '级'), "风向": wd, "空气质量": aqi}
        d.append(it)
    return jsonify(d)


# 获取天气分页数据
def get_weathers_list(page_size, page_no, param):
    param = param.replace("\\", "")
    count_sql = "select count(*) from weather where " + param
    count_res = query(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    sql = "select * from weather where " + param + " order by id desc limit " + str(start) + "," + str(page_size)
    res = query(sql)
    data_page = []
    page_list = []
    max_page = 0
    if count_res % page_size == 0:
        max_page = int(count_res / page_size)
    else:
        max_page = int(count_res / page_size) + 1
    if max_page <= 5:
        page_list = [i for i in range(1, max_page + 1, 1)]
    elif page_no + 2 > max_page:
        page_list = [i for i in range(max_page - 5, max_page + 1, 1)]
    elif page_no - 2 < 1:
        page_list = [i for i in range(1, 6, 1)]
    else:
        page_list = [i for i in range(page_no - 2, page_no + 3, 1)]
    for a, b, c, d, e, f, g, h, i, j, k, l, m, n in res:
        item = [a, b, c, d, e, f, g, h, i, j, k, l]
        data_page.append(item)
    return data_page, count_res, page_list, max_page


# 修改天气情况
def edit_weathers(id, temp, wd, ws, wse, sd, weather):
    sql = "update weather set temp=" + temp + ",wd='" + wd + "',ws=" + ws + ",wse=" + wse + ",sd=" + sd + ",weather='" + weather + "' where id =" + id;
    # print(sql)
    res = query(sql)
    return res
