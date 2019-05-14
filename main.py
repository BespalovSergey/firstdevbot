import requests
import os
import telegram
import logging
from logging.handlers import RotatingFileHandler
# bot_error token 803220816:AAEExBm2x3rZ5Bit0Gy_nrd_EyT4t5dbd6s

class MyLogsHandler(logging.Handler):
  def emit(self, record):
    log_entry = self.format(record)
    error_bot = telegram.Bot(token= os.environ['bot_error_token'])
    error_bot.send_message(chat_id= 814635828, text = log_entry)

def main( ):

  headers = {
  "Authorization":os.environ['devman_token']
  }
  params = {}
  crach = 'Бот упал с ошибкой'
  url='https://dvmn.org/api/long_polling/'
  logging.basicConfig(level = logging.INFO ,format  = '%(process)d %(levelname)s %(message)s')

  logger = logging.getLogger('first_bot')
  logger.setLevel(logging.INFO)
  handler = MyLogsHandler()
  logger.addHandler(handler)
  logger.info('I am new logger')
 # bot.send_message(chat_id = 814635828 ,text =  'Бот запущен')

  while True:
  
    try:
      response = requests.get(url= url,params = params, headers = headers ,timeout = 5)
    
      if response.ok:
        server_answer = response.json()
      
        if server_answer['status'] == 'timeout':
          params = {'timestamp':server_answer['timestamp_to_request']}
        elif server_answer['status']  == 'found':
          params = {'timestamp':server_answer['last_attempt_timestamp']}
          lesson_title = server_answer['new_attempts'][0]['lesson_title']
          is_negative = server_answer['new_attempts'][0]['is_negative'] 
          test_result=''
          message ='У Вас проверили работу \"{}'.format(lesson_title)
          if is_negative:
            test_result='\"\n\nК сожалению, в работе нашлись ошибки'
          else:
            test_result='\"\n\nПреподавателю всё понравилось, можно приступать к следующему уроку' 
          user_response = '{}{}'.format(message,test_result)   
          bot.send_message(chat_id = 814635828,text  = user_response)
      else:
        try:
          response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
          logger.error( http_err)
          #bot.send_message(chat_id = 814635828 ,text =  crach)
          #bot.send_message(chat_id = 814635828 ,text =  'HTTP response error')
      
      

    except requests.exceptions.ReadTimeout as time_err:
      logger.error( time_err)
      #bot.send_message(chat_id = 814635828 ,text =  crach)
      #bot.send_message(chat_id = 814635828 ,text = 'ReadTimeout error')
    except ConnectionError as con_err:
      logger.error( con_err)
      #bot.send_message(chat_id = 814635828 ,text =  crach)
      #bot.send_message(chat_id = 814635828 ,text =  'Connection error')

    
if __name__ == "__main__":
  bot = telegram.Bot(token= os.environ['telegram_token'])
  main(  )
    
    

