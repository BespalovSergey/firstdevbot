import requests
import os
import telegram
import logging

#from dotenv import load_dotenv
#load_dotenv()

class MyLogsHandler(logging.Handler):
    def __init__(self ):
      logging.Handler.__init__(self)
      self.error_bot = telegram.Bot(token= os.environ['bot_error_token'])

    def emit(self, record):
      log_entry = self.format(record)
      error_message = '{}{}'.format("Бот проверки заданий упал с ошибкой \n",log_entry)
      self.error_bot.send_message(chat_id = 814635828 ,text =  error_message)

def main( ):
  headers = {
  "Authorization":os.environ['devman_token']
  }
  params = {}

  url='https://dvmn.org/api/long_polling/'
  logging.basicConfig(format  = '%(process)d %(levelname)s %(message)s')
  logger = logging.getLogger('bot_logger')
  logger.setLevel(logging.INFO)
  logger.addHandler(MyLogsHandler())
  logger.info('Бот проверки ошибок запущен')


  while True:
  
    try:
      response = requests.get(url= url,params = params, headers = headers ,timeout = 91)
    
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

        response.raise_for_status()

      
      

    except (requests.exceptions.ReadTimeout ,requests.exceptions.HTTPError ,ConnectionError) as bot_err:
      logger.error( bot_err)


    
if __name__ == "__main__":
  bot = telegram.Bot(token= os.environ['telegram_token'])
  main()
    
    
