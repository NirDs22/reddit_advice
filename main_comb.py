# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:07:43 2023

@author: Nir Daos
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

import praw
import g4f
import reddir_handler
import random
from time import sleep

def problem_analysis(pro):
    pro_size = len(pro.split(" "))
    if pro_size <= 3:
        return False
    return True

def answer_analysis(ans):
    ans_size = len(ans.split(" "))
    if ans_size <= 20:
        return False   # short answer means the AI won't reply.
    time_per_word_sec = random.triangular(0.5, 1, 1.5) * ans_size  # The average typing speed
    time_scrolling = random.triangular(3, 13, 10)  # Time it takes to scroll and click post
    sleep(time_per_word_sec + time_scrolling)
    return True

reddit = praw.Reddit(
    user_agent="botbot:1:<1.0> (by u/ApiHelp1)",
    client_id="jlOawY9W20bS6H3XPTdw2g",
    client_secret="3lJlaVnA8W1vQTMgVHqub0HRZVnbaA",
    username="ApiHelp1",
    password="68096809Ab",
)

def compose_guide():
    g_ask_reply = ["Please advice on this matter, ", "Please help me with this problem, "]
    g_human_qualities = ["be kind and deep, ", "", "be kind, deep and helpful, ", "be helpful and practical, "]
    g_direct = ["", "answer directly to the problem without much debate, "]
    g_reply_len = ["Answer in one short paragraph up to 40 words, ", "keep the answer between 21-28 words, "]
    g_gram_style = ["", "write with the same style as the problem text, ", "write with a one minor typo, ", "write without using Uppercase at the beginning of one of your sentences, "]

    guide = ""
    guide += random.choice(g_ask_reply)
    guide += random.choice(g_human_qualities)
    guide += random.choice(g_direct)
    guide += random.choice(g_reply_len)
    guide += random.choice(g_gram_style)
    guide += "be serious, no humor."  # random.choice(g_humor)
    guide += ". The answer cannot look like it was made by AI, but like a human comment from an actual user! Do not repeat to describe the problem. Do not start the answer with 'Hey, Hello' etc."

    return guide

def get_advice(problem, guidance=compose_guide()):
    if len(problem) < 10:
        return "Fail"
    # Automatic selection of provider
    for trial in range(4):
        try:
            # Normal response
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": problem + guidance}],
            )  # Alternative model setting

            # print(response)
            if "Chatbase" in response:
                continue

            return response
        except BaseException as ex:
            print(f"\n #{trial + 1}/4 Error while trying to fetch ans. {ex}")
    print("Fail")
    return "Fail"

def start():
    forums = ["adviceforteens", "relationship_advice", "helpme", "advice"]
    # Fetch posts from r/advicen
    for f in forums:
        subreddit = reddit.subreddit(f)
        for submission in subreddit.new(limit=10):  # Adjust the limit as needed
            if (not submission.over_18) and (submission.num_comments <= 0):
                print(f"Title: {submission.title}\n")
                problem = submission.selftext
                print("Text: ", problem, "\n")

                if problem_analysis(problem):
                    ans = get_advice(problem)
                    ans = ans.replace('*', '')

                if answer_analysis(ans):
                    print(f"####\nABOUT TO REPLY: \n\n {ans} \n\nEND OF REPLY\n####")
                    a = "y"  # input("ok? (y/n) ")
                    if a == "y":
                        submission.reply(ans)

                print("\n---\n")
            else:
                print("\nnsfw/commented\n")
            sleep(6)
            print("!end of post!")

if __name__ == '__main__':
    while True:
        for trial in range(1, 6):
            try:
                start()
                sleep(60 * 60 * 2)

            except BaseException as ex:
                print(f"\n #{trial}/5 Error while trying to start. {ex}")
            sleep(60 * 30)

        break
