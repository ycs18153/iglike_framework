from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import json
import asyncio
from fastapi import FastAPI, BackgroundTasks
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import pymongo
from pymongo import MongoClient
import certifi
from datetime import datetime
#

from .models import Model, updateModel

router = APIRouter()

#
mongoClient = pymongo.MongoClient(
    "mongodb+srv://andy:acdwsx321@groupmagt.cgjzv3a.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())  # 要連結到的 connect string
iglike_auth = mongoClient["iglike_auth"]  # 指定資料庫
autoLikeResult_table = iglike_auth["autoLikeResult"]  # 指定資料表
#


@router.post("/", response_description="Add new user")
async def create_user(request: Request, user: Model = Body(...)):
    user = jsonable_encoder(user)
    new_user = await request.app.mongodb["auth_user"].insert_one(user)
    created_user = await request.app.mongodb["auth_user"].find_one(
        {"_id": new_user.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get("/", response_description="List all users")
async def list_users(request: Request):
    users = []
    for doc in await request.app.mongodb["auth_user"].find().to_list(length=100):
        users.append(doc)
    return users


@router.get("/{id}", response_description="Get a user")
async def show_user(id: str, request: Request):
    if (user := await request.app.mongodb["auth_user"].find_one({"uid": id})) is not None:
        return user
    else:
        return '-1'

    raise HTTPException(status_code=404, detail=f"user {id} not found")


@router.get("/autolike_res/{id}", response_description="Get a user who had exec auto like function and display result")
async def show_autolike_res(id: str, request: Request):
    collections = []
    records = autoLikeResult_table.find({"uid": id}, {'_id': 0})
    for record in records:
        collections.append(record)
    return collections
    raise HTTPException(status_code=404, detail=f"user {id} not found")

# @router.put("/{id}", response_description="Update a task")
# async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
#     task = {k: v for k, v in task.dict().items() if v is not None}

#     if len(task) >= 1:
#         update_result = await request.app.mongodb["tasks"].update_one(
#             {"_id": id}, {"$set": task}
#         )

#         if update_result.modified_count == 1:
#             if (
#                 updated_task := await request.app.mongodb["tasks"].find_one({"_id": id})
#             ) is not None:
#                 return updated_task

#     if (
#         existing_task := await request.app.mongodb["tasks"].find_one({"_id": id})
#     ) is not None:
#         return existing_task

#     raise HTTPException(status_code=404, detail=f"Task {id} not found")


# @router.delete("/{id}", response_description="Delete Task")
# async def delete_task(id: str, request: Request):
#     delete_result = await request.app.mongodb["tasks"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Task {id} not found")


async def auto_like_implem(uid, account, password, minWaitTime, maxWaitTime, hashtag, maxLike):
    # structure for result writing
    line_uid = uid
    ig_account = account
    now = datetime.now()
    start_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # end_time = ''
    # num_of_liked = 0
    author_of_liked_author = []

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")  # max. the window size
    # options.add_argument('--headless')

    # Have to edit the path of the chrome driver
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(), chrome_options=options)
    # driver = webdriver.Chrome(
    #     '/Users/twlin/code/iglike_framework/backend/apps/todo/chromedriver', chrome_options=options)
    action = webdriver.ActionChains(driver)

    # load cookie -> for testing
    # with open('/Users/twlin/code/iglike_framework/backend/apps/todo/cookie_jar.json') as f:
    #     cookies = json.load(f)

    driver.get("https://www.instagram.com/")

    await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
    # time.sleep(random.randint(minWaitTime, maxWaitTime))

    # load cookie -> for testing
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # driver.refresh()

    # # 抓取：帳號密碼輸入框
    try:
        account_textbox = WebDriverWait(driver, 10, 0.2).until(
            EC.presence_of_element_located((By.NAME, "username")), '-1')
        password_textbox = WebDriverWait(driver, 10, 0.2).until(
            EC.presence_of_element_located((By.NAME, "password")), '-1')
    except:
        print('帳號或密碼的 By.NAME 改變')
        driver.quit()
        return '-1'

    # 抓取：登入按鈕
    try:
        loginBtn = WebDriverWait(driver, 10, 0.2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _abak _abb8 _abbq _abb- _abcm']")), '-1')
    except:
        print('登入按鈕的 By.XPATH 改變')
        driver.quit()
        return '-2'

    # 輸入：帳號密碼
    # 執行：登入
    await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
    # time.sleep(random.randint(minWaitTime, maxWaitTime))
    account_textbox.send_keys(account)
    await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
    # time.sleep(random.randint(minWaitTime, maxWaitTime))
    password_textbox.send_keys(password)
    print('輸入完帳號密碼，等待：', minWaitTime, '~', maxWaitTime, '秒，就執行登入')
    await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
    # time.sleep(random.randint(minWaitTime, maxWaitTime))
    loginBtn.click()
    print('已按下登入')

    '''
        按下登入按鈕後，若:
        1. 帳號密碼錯誤
        2. 密碼 < 6個字元
        則10秒後才 return 400
    '''

    try:
        # 抓取：稍後再說按鈕
        # 沒抓到代表沒登入成功
        later = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='_ac8f']//button")), '-1')
        print('已找到`稍後再說`按鈕，等待：', minWaitTime, '~', maxWaitTime, '秒，就按稍後再說')
    except:
        print("帳號或密碼不正確")
        driver.quit()
        return '400'

    # 執行：按下稍後再說
    time.sleep(random.randint(minWaitTime, maxWaitTime))
    later.click()
    print('已按下`稍後再說`，等待：', minWaitTime, '~', maxWaitTime, '秒，就找hashtag')

    # 找 hashtag
    await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
    # time.sleep(random.randint(minWaitTime, maxWaitTime))
    driver.get("https://www.instagram.com/explore/tags/" + hashtag)

    await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
    # time.sleep(random.randint(minWaitTime, maxWaitTime))
    webBody = WebDriverWait(driver, 10, 0.2).until(
        EC.presence_of_element_located((By.TAG_NAME, "body")), '-1')
    webBody.send_keys(Keys.SPACE)
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)

    round = 1
    liked = 1
    while liked <= maxLike:
        print('==============')
        print('Round: ', round)
        await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
        # time.sleep(random.randint(minWaitTime, maxWaitTime))
        try:
            posts = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='_aabd _aa8k _aanf']")), '-1')
            # posts = driver.find_elements(
            #     By.XPATH, "//div[@class='_aabd _aa8k _aanf']")
            print("抓到： ", len(posts), " 篇")
        except Exception as e:
            print(e)
            print("抓到 invisible element 之貼文")
            pass
        # 點進某篇貼文
        time.sleep(random.randint(minWaitTime, maxWaitTime))
        try:
            #
            r_num = random.randint(0, len(posts) - 1)
            print("亂數： ", r_num)
            posts[r_num].click()
            #
            # posts[random.randint(0, len(posts) - 1)].click()
        except Exception as e:
            print(e)
            print("1. 被限制 or 2. 點選到 invisible element 之貼文")
            return '666 Auto Like has been Limited'
            driver.quit()
            break
        await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
        # time.sleep(random.randint(minWaitTime, maxWaitTime))
        # 按讚
        try:
            likeBtn_att = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "section._aamu._ae3_ span._aamw button._abl- svg")), '-1')
        except Exception as e:
            print(e)
            print('標籤改變或抓不到: likeBtn_att')
            break
        try:
            likeBtn = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "section._aamu._ae3_ span._aamw button")), '-1')
        except Exception as e:
            print(e)
            print('標籤改變或抓不到: likeBtn')
            break
        if likeBtn_att.get_attribute('aria-label') == '讚':
            try:
                print("按了第 ", liked, " 篇讚")
                try:
                    author = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div._aacl._aaco._aacw._aacx._aad6._aade div.xt0psk2 div.xt0psk2 a")), '-1')
                    # author = driver.find_element(
                    #     By.XPATH, "//div[@class='_aacl _aaco _aacw _aacx _aad6 _aade']//div[@class='xt0psk2']//span[@class='_aap6 _aap7 _aap8']//a[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _acan _acao _acat _acaw _aj1- _a6hd']").text
                    #
                    author_of_liked_author.append(author.text)
                    #
                    print("Po文作者: ", author.text)
                except Exception as e:
                    print(e)
                    print("Po文作者標籤改變")
                    pass
                await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
                # time.sleep(random.randint(minWaitTime, maxWaitTime))
                likeBtn.click()
                liked = liked + 1
                await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
                # time.sleep(random.randint(minWaitTime, maxWaitTime))
            except Exception as e:
                print(e)
                print("按讚發生問題")
                # time.sleep(150)
                pass
        else:
            try:
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
                # time.sleep(random.randint(minWaitTime, maxWaitTime))
                print(liked, '. 此篇已按過讚，故略過並往下滑')
                for i in range(3):
                    print("下滑 ", i, " 次")
                    # Scroll down to bottom
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    await asyncio.sleep(random.randint(minWaitTime, maxWaitTime))
                    # time.sleep(random.randint(minWaitTime, maxWaitTime))
                round = round + 1
                print("========")
                continue
            except Exception as e:
                print(e)
                print("下拉發生問題")
                pass
        round = round + 1
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        print("========")

    print("執行完成並結束")
    print(author_of_liked_author)
    driver.quit()
    now = datetime.now()
    end_time = now.strftime("%Y-%m-%d %H:%M:%S")
    res_dict = {
        "uid": line_uid,
        "ig_account": account,
        "start_time": start_time,
        "end_time": end_time,
        "num_of_liked": liked - 1,
        "authors_of_liked": author_of_liked_author
    }
    autoLikeResult_table.insert_one(res_dict)


@router.get("/autolike/{uid}/{account}/{password}/{minWaitTime}/{maxWaitTime}/{hashtag}/{maxLike}", response_description="exec auto lilke")
async def auto_like(uid: str, account: str, password: str, minWaitTime: int, maxWaitTime: int, hashtag: str, maxLike: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        auto_like_implem, uid, account, password, minWaitTime, maxWaitTime, hashtag, maxLike)
    return 'op'
