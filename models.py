import openai
import os
import sys
import urllib.request
import re
import ssl
import requests
import json

ssl._create_default_https_context = ssl._create_unverified_context

openai.api_key = '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'

def is_korean(text):
    return bool(re.search('[가-힣]', text))

class AI():
    def chatgpt(text):
        messages = [{
            'role' : 'user',
            'content' : f'{text}'
        }]
        
        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )

        answer = res['choices'][0]['message']['content']

        return answer

    def feedback_chatgpt(text, previous_conversation):
        messages = previous_conversation + [{
            'role' : 'system',
            'content' : "You are the teacher who helps me write better prompts.\
                "
        }, {
            'role' : 'user',
            'content' : f"I'm trying to create results by inserting the above prompt into chatGPT. Please tell me what else I need to add to make a better prompt.\
                my_prompt : {text}\
                Given my_prompt, what else should I modify in this prompt?\
                PLEASE ANSWER IN KOREAN\
                Here are detail examples\
                Example\
                구분 기호를 사용하여 입력 내용을 명확하게 표시하세요\
                구조화된 출력 방식을 요청하세요\
                조건을 충족하는지 확인하세요 \
                원하는 작업의 성공적인 실행 예시를 제공하세요(“Few-shot” prompting)\
                단계를 나눠서 요청해 주세요\
                    \
                After listing all the examples, you can finally modify the prompt and print the modified prompt in the form of 'modified prompt: '.\
                "
        }]

        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )

        answer = res['choices'][0]['message']['content']

        return answer

    def dalle(text):
        if is_korean(text):
            client_id = "alN0gU59jLDRlPMzp1HU" # 개발자센터에서 발급받은 Client ID 값
            client_secret = "b6irWewCtM" # 개발자센터에서 발급받은 Client Secret 값
            url = 'https://openapi.naver.com/v1/papago/n2mt'
            headers = {
                'Content-Type': 'application/json',
                'X-Naver-Client-Id': client_id,
                'X-Naver-Client-Secret': client_secret
            }
            data = {'source': 'ko', 'target': 'en', 'text': text}
            
            response = requests.post(url, json.dumps(data), headers=headers) 

            text = response.json()['message']['result']['translatedText']

        res = openai.Image.create(
            prompt=text,
            n=1,
            size='256x256'
        )

        return text, res['data'][0]['url']

    