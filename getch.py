from readchar import readchar

def getch(valid_options = ['']):
   key_press = None
   while True:
      key_press = readchar()
      if key_press: key_press = key_press.lower()
      if key_press in valid_options:
         break
   
   return key_press