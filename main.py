import requests
import os
import telegram
import logging

def main():
  headers = {
  "Authorization":os.environ['devman_token']
}
params = {}
crach = 'Бот упал с ошибкой'
url='https://dvmn.org/api/long_polling/'
logging.basicConfig(level = logging.DEBUG ,format  = '%(process)d %(levelname)s %(message)s')


logging.debug('First bot is started')
bot.send_message(chat_id = 814635828 ,text =  'Бот запущен')

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
        logging.error( http_err)
        bot.send_message(chat_id = 814635828 ,text =  crach)
        bot.send_message(chat_id = 814635828 ,text =  'HTTP response error') 
      
      

  except requests.exceptions.ReadTimeout as time_err:
    logging.error( time_err) 
    bot.send_message(chat_id = 814635828 ,text =  crach)
    bot.send_message(chat_id = 814635828 ,text = 'ReadTimeout error')
  except ConnectionError as con_err:
    logging.error( con_err)
    bot.send_message(chat_id = 814635828 ,text =  crach)
    bot.send_message(chat_id = 814635828 ,text =  'Connection error')

    
if __name__ == "__main__":
  bot = telegram.Bot(token= os.environ['telegram_token'])
  main()
    
    
