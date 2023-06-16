from .chat_preload import *
from .cerate_tags import *

FILE_PATH = 'test.txt'
def tag(news_txt_path):
    tag = news_tag()
    return tag.create_tag(news_txt_path)


def news_answer(question, news_txt):
    with open(FILE_PATH, 'w') as f:
        f.write(news_txt)
    chatbot_ans = chatbot(FILE_PATH)
    return chatbot_ans.news_chat(question)


def topic_answer(question, news_txt):
    with open(FILE_PATH, 'w') as f:
        f.write(news_txt)
    chatbot_ans_topic = chatbot(FILE_PATH)
    return chatbot_ans_topic.topic_chat(question)

if __name__ == "__main__":
    print(tag("test.txt"))
    # print(news_answer("what is the company", "test.txt"))
    print(topic_answer("what is digital marketing", "test.txt"))
