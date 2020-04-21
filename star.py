# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import json

q_class = {}


def crawl(u):
    browser = webdriver.Chrome()
    browser.get(u)
    con = browser.find_elements_by_css_selector(
        "#root > table:nth-child(5) > tbody > tr > td:nth-child(1) > table:nth-child(2)")
    title_urls = []
    for co in con:
        link = co.find_elements_by_tag_name('a')
        for li in link:
            c = li.get_attribute('href')
            tmp = {"title": li.text, "link": c}
            title_urls.append(tmp)
    nxt = browser.find_element_by_link_text('下一页')
    while nxt:
        time.sleep(1)
        nxt.click()
        content = browser.find_elements_by_css_selector(
            "#root > table:nth-child(5) > tbody > tr > td:nth-child(1) > table:nth-child(2)")
        for co in content:
            link = co.find_elements_by_tag_name('a')
            for li in link:
                c = li.get_attribute('href')
                tmp = {"title": li.text, "link": c}
                title_urls.append(tmp)
        try:
            nxt = browser.find_element_by_link_text('下一页')
        except:
            nxt = None
    path = "./src/" + q_class[u] + ".json"
    with open(path, 'w') as f:
        json.dump(title_urls, f)
    browser.close()


def crawl_init(u):
    # 模拟浏览器
    browser = webdriver.Chrome()
    # 最大化窗口
    # browser.maximize_window()
    browser.get(u)
    con = browser.find_elements_by_css_selector('#nav > tbody > tr')
    for co in con:
        link = co.find_elements_by_tag_name('a')
        i = 0
        for li in link:
            if i > 0:
                c = li.get_attribute('href')
                q_class[c] = li.text
            else:
                i = 1
    browser.close()
    # print(q_class)


if __name__ == '__main__':
    init_url = 'http://news.nankai.edu.cn/'
    crawl_init(init_url)
    for url, text in q_class.items():
        crawl(url)
