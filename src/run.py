from bot import Bot
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','-username', help='Instagram user login', required=True)
    parser.add_argument('-p', '-password', help='Instagram user password', required=True)
    parser.add_argument('-ht', '-hashtags', help='Desired hashtags to run the bot on', required=True, action='append')
    parser.add_argument('-f', '-follow', help='If the bot will follow new users', action='store_true')
    
    args = parser.parse_args()
    print(args)

    _bot = Bot(args.u, args.p)
    if _bot.login():
        for hashtag in args.ht:
            _bot.run(hashtag, follow=args.f)

        _bot.close()
    else:
        _bot.close()
