import argparse
from dotenv import load_dotenv
from bot import Bot

if __name__ == "__main__":
    """ parser = argparse.ArgumentParser()
    parser.add_argument('-u','-username', help='Instagram user login', required=True)
    parser.add_argument('-p', '-password', help='Instagram user password', required=True)
    parser.add_argument('-l', '-promolink', help='Promo Link', required=True, action='append')
    parser.add_argument('-f', '-follow', help='If the bot will follow new users', action='store_true')
    args = parser.parse_args()
    print(args)

    """
    
    #_bot = Bot('repbauduco', 'baubau123')
    _bot = Bot('azz_cs', 'assuncao1')

    
    #_bot = Bot('leououu', '04101997ll')
    
    if _bot.login():
        #_bot.like_and_follow(hashtag='csgo')
        _bot.run('https://www.instagram.com/p/B_5nFMeDd-w/', follow=False, n_comb=2)
        _bot.close()
    else:
        _bot.close()
