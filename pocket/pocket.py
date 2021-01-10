#!/usr/bin/env python
from os import environ as env
import requests
import webbrowser

env["POCKET_CONSUMER_KEY"] = "your key here"
env["POCKET_APP_NAME"] = "miniflux"


def authorize_pocket_app():
    data = {
        # "consumer_key": env['POCKET_CONSUMER_KEY'],
        # "redirect_uri": env['POCKET_APP_NAME'],
    }
    resp = requests.post(url="https://getpocket.com/v3/oauth/request", data=data)
    code = resp.text.split("=")[1]
    webbrowser.open(f"https://getpocket.com/auth/authorize?request_token={code}"
                    "&redirect_uri=https://duckduckgo.com")
    input("Authorize %s app in the browser, then click enter" % env['POCKET_APP_NAME'])
    get_token(code)


def get_token(code):
    resp = requests.post(
        url="https://getpocket.com/v3/oauth/authorize",
        data={
            "consumer_key": env["POCKET_CONSUMER_KEY"],
            "code": code,
        })

    token = resp.text.split("&")[0].split("=")[1]
    print("Secret token:", token)


if __name__ == "__main__":
    authorize_pocket_app()