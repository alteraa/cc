# from typing import List, Dict
import re
import json
from random import choice
# source: from nltk.chat import util

def get_session_elements(session: dict) -> tuple:
    _pattern = session['pattern']
    _response = session['response']
    return (_pattern, _response)

def get_json(json_filepath: str) -> dict:
    _json = json.load(open(json_filepath, 'r', encoding='utf8'))
    return _json

def get_sessions(json_content: dict) -> list:
    _sessions = json_content['sessions']
    return _sessions

class ChatCompiler:
    def __init__(self, chat_json_path: str, reflections: dict = {}) -> None:
        self.__json = get_json(chat_json_path)
        _sessions = get_sessions(self.__json)
        self.__sessions = self.__compile_sessions(_sessions)
        self.__reflections = reflections
        self.__refl_regex = self.__compile_reflection(reflections)
        
    def __compile_sessions(self, sessions: list) -> list:
        ls = []
        for session in sessions:
            p, r = get_session_elements(session)
            # print(p, r)
            ls.append((re.compile(p, re.IGNORECASE), r))
        return ls
    
    def __compile_reflection(self, reflections: dict) -> re.Pattern:
        sorted_refl = sorted(reflections, key=len, reverse=True)
        return re.compile(
            r"\b({})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )
    
    def __reflect(self, text: str) -> str:
        return self.__refl_regex.sub(
            lambda match: self.__reflections[match.string[match.start() : match.end()]], 
            text.lower()
        )
    
    def __pass_arguments(self, response: str, match: re.Match) -> str:
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self.__reflect(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response
    
    def respond(self, user_input: str):
        # check each pattern
        for (pattern, response) in self.__sessions:
            match = pattern.match(user_input)

            # did the pattern match?
            if match:
                resp = choice(response)  # pick a random response
                resp = self.__pass_arguments(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp        