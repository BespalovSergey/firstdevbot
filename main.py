import requests
import os
import telegram
import logging
import time

from dotenv import load_dotenv


class MyLogsHandler(logging.Handler):
    def __init__(self ,my_chat_id):
      super().__init__()
      self.error_bot = telegram.Bot(token= os.environ['bot_error_token'])
      self.my_chat_id = my_chat_id

    def emit(self, record):
      log_entry = self.format(record)
      
      bot_down = 'Бот проверки заданий упал с ошибкой \n'
      error_message = '{}{}'.format(bot_down , log_entry)

      if log_entry == 'Бот проверки ошибок запущен':
        error_message = 'Бот проверки ошибок запущен'


      self.error_bot.send_message(chat_id = self.my_chat_id ,text =  error_message)

def main( ):
  headers = {
  "Authorization":os.environ['devman_token']
  }
  params = {}

  url='https://dvmn.org/api/long_polling/'
  logging.basicConfig(format  = '%(process)d %(levelname)s %(message)s')
  logger = logging.getLogger('bot_logger')
  logger.setLevel(logging.INFO)
  logger.addHandler(MyLogsHandler(my_chat_id= my_chat_id))
  logger.info('Бот проверки ошибок запущен')


  while True:
  
    try:
      response = requests.get(url= url,params = params, headers = headers ,timeout = 91)
      response.raise_for_status()
      server_answer = response.json()

      if server_answer['status'] == 'timeout':
        params = {'timestamp': server_answer['timestamp_to_request']}
      elif server_answer['status'] == 'found':
        params = {'timestamp': server_answer['last_attempt_timestamp']}
        lesson_title = server_answer['new_attempts'][0]['lesson_title']
        is_negative = server_answer['new_attempts'][0]['is_negative']
        test_result = ''
        message = 'У Вас проверили работу \"{}'.format(lesson_title)
        if is_negative:
          test_result = '\"\n\nК сожалению, в работе нашлись ошибки'
        else:
          test_result = '\"\n\nПреподавателю всё понравилось, можно приступать к следующему уроку'
        user_response = '{}{}'.format(message, test_result)
        bot.send_message(chat_id=my_chat_id, text=user_response)

      
      

    except requests.exceptions.HTTPError  as bot_err:
      logger.error( bot_err)
    except ConnectionError as bot_err:
      logger.error(bot_err)
      time.sleep(10)


    
if __name__ == "__main__":
  load_dotenv()
  my_chat_id = os.environ['telegram_chat_id']
  bot = telegram.Bot(token= os.environ['telegram_token'])
  main()
    
    
