from bardapi import Bard
import os
import requests
os.environ['_BARD_API_KEY'] = 'XwjLV4fakAyJs9eXmVCmjQZGaiV_yDfPj3CiO5lNIXGCvQ-YDi5lkQazCY8ayciCVWo0eg.'
token='XwjLV4fakAyJs9eXmVCmjQZGaiV_yDfPj3CiO5lNIXGCvQ-YDi5lkQazCY8ayciCVWo0eg.'

session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
# session.cookies.set("__Secure-1PSID", token) 

bard = Bard(token=token, session=session, timeout=30)
ans = bard.get_answer("How are you?")['content']

print(ans)
# Continued conversation without set new session
ans_prev = bard.get_answer("What is my last prompt??")['content']
print(ans_prev)