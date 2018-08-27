import constants
import requests
import json
import flask
from flask import request
from flask import jsonify
from time import localtime, time
from timedate import Period, in_minutes, in_minutes_t, in_h_m, add_utc

application = flask.Flask(__name__)

url = "https://api.telegram.org/bot" + constants.token + '/'


def take_data():
    """

                Creating list of lessons

    """

    lessons = []
    for i in constants.lessons:
        x = Period(i[0], i[1], i[2], i[3], i[4], i[5])
        lessons.append(x)
    '''
    
                Takes present time
    
    '''
    time_now = [localtime(time())[3], localtime(time())[4]]
    time_now_day = localtime(time())[6]
    print(time_now, time_now_day)
    time_now[0], time_now[1], time_now_day = add_utc(3, time_now[0], time_now[1], time_now_day)[0], \
                                             add_utc(3, time_now[0], time_now[1], time_now_day)[1], \
                                             add_utc(3, time_now[0], time_now[1], time_now_day)[2]
    print(time_now, time_now_day)
    '''
    
                Search for the next lesson
    
    '''

    today_lessons = [i for i in lessons if i.day == constants.days[time_now_day]]

    lessons_now = "Nothing on today"

    trigger = True
    for i in today_lessons:
        if in_minutes_t(i.time_start) <= in_minutes(time_now[0], time_now[1]) < in_minutes_t(i.time_end):
            lessons_now = i.subject, i.kind, i.room, \
                          (in_minutes_t(i.time_end) - in_minutes(time_now[0], time_now[1])), False, i.time_start
            trigger = False

    if trigger:
        delta_time = 1440
        for i in today_lessons:
            if 0 < in_minutes_t(i.time_start) - in_minutes(time_now[0], time_now[1]) < delta_time:
                delta_time = in_minutes_t(i.time_start) - in_minutes(time_now[0], time_now[1])
                lessons_now = i.subject, i.kind, i.room, \
                              (in_minutes_t(i.time_start) - in_minutes(time_now[0], time_now[1])), True, i.time_end

    result = "Lesson: {},\nCategory: {},\nRoom: {},\n".format(lessons_now[0], lessons_now[1], lessons_now[2])
    hours_left, minutes_left = str(in_h_m(lessons_now[3])[0]), str(in_h_m(lessons_now[3])[1])
    if lessons_now[4]:
        result += "Lesson starts in {}:{},\n".format(lessons_now[5].hour, lessons_now[5].minute)
        result += "Before the beginning of the lesson " + hours_left + ":" + minutes_left + " left."
    else:
        result += "Lesson ends in {}:{},\n".format(lessons_now[5].hour, lessons_now[5].minute)
        result += "Until the end of the lesson " + hours_left + ":" + minutes_left + " left."
        return result


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_update():
    urls = url + "getUpdates"
    r = requests.get(urls)
    return r.json()


def send_message(chat_id, text="bla-bla-bla"):
    urls = url + "sendMessage"
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(urls, json=answer)
    return r.json()


@application.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        send_message(chat_id, take_data())

        # write_json(r)
        return jsonify(r)
    return 'Testing!'


def main():
    # r = get_update()
    # chat_id = r['result'][-1]['message']['chat']['id']
    # print(chat_id)
    # send_message(chat_id)
    pass


if __name__ == "__main__":
    application.run()
