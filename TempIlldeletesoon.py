import sys
import telepot

# Pass in the token as the first parameter. 
# e.g. python3.4 file.py token
TOKEN = sys.argv[1] 

def handle(msg):
    # Bot fuctionality

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

while 1:
    time.sleep(10)
