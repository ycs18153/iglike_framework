from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
#

from .models import Model, updateModel

router = APIRouter()


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


@router.get("/autolike/{account}/{password}/{minWaitTime}/{maxWaitTime}/{hashtag}/{maxLike}", response_description="exec auto lilke")
async def auto_like(account: str, password: str, minWaitTime: int, maxWaitTime: int, hashtag: str, maxLike: int):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")  # max. the window size
    # options.add_argument('--headless')

    # Have to edit the path of the chrome driver
    driver = webdriver.Chrome(
        '/Users/twlin/code/iglike_framework/backend/apps/todo/chromedriver', chrome_options=options)
    action = webdriver.ActionChains(driver)

    driver.get("https://www.instagram.com/")

    # 抓取：帳號密碼輸入框
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
    time.sleep(random.randint(minWaitTime, maxWaitTime))
    account_textbox.send_keys(account)
    time.sleep(random.randint(minWaitTime, maxWaitTime))
    password_textbox.send_keys(password)
    print('輸入完帳號密碼，等待：', minWaitTime, '~', maxWaitTime, '秒，就執行登入')
    time.sleep(random.randint(minWaitTime, maxWaitTime))
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
    time.sleep(random.randint(minWaitTime, maxWaitTime))
    driver.get("https://www.instagram.com/explore/tags/" + hashtag)

    time.sleep(random.randint(minWaitTime, maxWaitTime))

    #
    liked = 0
    while liked <= maxLike:
        # 先往下拉，試圖抓到貼文
        print('往下滑')
        for i in range(4):
            time.sleep(random.randint(minWaitTime, maxWaitTime))
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)

        # 抓到目前所能見的貼文們
        post_count = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='_aabd _aa8k _aanf']")), '-1')
        print("目前抓到：", len(post_count), "篇貼文")
        for pc in post_count:
            print('post_count = ', pc.text)

        # 去看抓到的post之href值
        # 這是為了去看：當下一次while時，page會再往下拉，此時去看這次抓到的href跟上次抓到的是否會一樣
        # --- 卡在這，會抓到上一round的post之div，但這些div照理說在頁面已經invisable ---#
        for post in post_count:
            a = post.find_element(By.CSS_SELECTOR, 'a')
            href = a.get_attribute('href')
            print(href)

        # 隨機按 (目前抓到的所有貼文數/2) 篇貼文的讚
        for round in range(int(len(post_count)/2)):
            liked = liked + 1
            time.sleep(random.randint(minWaitTime, maxWaitTime))
            # 點進某篇貼文
            post_count[random.randint(0, len(post_count) - 1)].click()
            time.sleep(random.randint(minWaitTime, maxWaitTime))
            # 按讚
            likeBtn_att = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "section._aamu._ae3_ span._aamw button._abl- svg")), '-1')
            likeBtn = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "section._aamu._ae3_ span._aamw button")), '-1')
            if likeBtn_att.get_attribute('aria-label') == '讚':
                time.sleep(random.randint(minWaitTime, maxWaitTime))
                likeBtn.click()
                print(liked, '. 讚')
                time.sleep(random.randint(minWaitTime, maxWaitTime))
            else:
                print(liked, '. 此篇已按過讚，故略過')
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    time.sleep(20)
    driver.quit()
    #

    # users = []
    # for doc in await request.app.mongodb["auth_user"].find().to_list(length=100):
    #     users.append(doc)
    # return users
