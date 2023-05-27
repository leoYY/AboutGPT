# -*- coding: UTF-8 -*-
"""
    @author     : leoyy
    @date       : 六  5/27 22:41:50 2023
    @last update: 六  5/27 22:41:50 2023
    @summary    : 
    @version    : 1.0.0.0
"""

import sys,os,getopt,logging,traceback
# import search path
# sys.path.append() 
import gflags
import importlib
import openai

from py_dotenv import read_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
_ = read_dotenv(dotenv_path)


openai.api_key = os.getenv('OPENAI_API_KEY')

# ================ log ===============
LOGFILE="./prompts_examples.log"

LOGLEVEL="NOTICE"
FORMAT="[%(levelname)s] %(asctime)s : %(pathname)s %(module)s:%(funcName)s[%(lineno)d] %(message)s"
LEVEL = {}
LEVEL['NOTICE'] = logging.NOTSET
LEVEL['DEBUG'] = logging.DEBUG
LEVEL['INFO'] = logging.INFO
LEVEL['WARNING'] = logging.WARNING
LEVEL['ERROR'] = logging.ERROR
LEVEL['CRITICAL'] = logging.CRITICAL

# ============== gflags ==============
# gflags.DEFINE_string("arg1", \"\", \"argument example\")
# usage like FLAGS.arg1
FLAGS = gflags.FLAGS

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    resp = openai.ChatCompletion.create(
            model = model,
            messages = messages,
            temperature = 0
    )
    return resp['choices'][0]["message"]["content"]

def InitLog():
    logger = logging.getLogger()
    hdlr = logging.FileHandler(LOGFILE)
    formatter = logging.Formatter(FORMAT)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(LEVEL[str(LOGLEVEL)])
    return logger
LOG=InitLog()

def action_lists():
    # example content
    text = """Long long ago, there was a king. He was very rich and kind. He had a daughter. She was very beautiful. \
            One day, the king said to his daughter, “I want to find a good husband for you. I will hold a party.  \
            You can choose one of them.” The princess was very happy. She said, “Thank you, father.” \ 
            On the day of the party, many princes came to the palace. They were very handsome. \
            The princess liked them very much. But she didn’t know who was the best. \
            At last, she chose the one who was the kindest. They got married and lived happily."""
    prompt = f"""
    Perform the following actions:
    1 - translate the following text delimited by triple backticks into Chinese .
    2 - Summarize the chinese result from action 1.
    3 - List each name in the summary.
    
    Answer in following format:

    Text : <chinese text>
    Summary : <summary>
    Roles: <list of names in summary>

    ```{text}```
    """
    res = get_completion(prompt)
    print(res)

def main(argv):
    importlib.reload(sys)
    try:
        argv = gflags.FLAGS(argv)
    except gflags.UnrecognizedFlagError as e:
        print("%s"%(e))
    except gflags.FlagsError as e:
        print("%s \\n Usage: %s ARGS\\n %s"%(e, sys.argv[0], FLAGS))
        sys.exit(1)

    action_lists()

if __name__ == "__main__":
    main(sys.argv)

