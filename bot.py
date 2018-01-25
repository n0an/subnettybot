#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import subnet
import secrets


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Usage example:\n'
                                '/subnet 10.1.1.12 255.255.255.248 \n'
                                'or\n'
                                '/subnet 10.1.1.12 /30')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Usage example:\n'
                                '/subnet 10.1.1.12 255.255.255.248 \n'
                                'or\n'
                                '/subnet 10.1.1.12 /30')


def echo(bot, update):
    """Echo the user message."""

    update.message.reply_text('Use /help command to get help')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def parse_ip(bot, update, args, chat_data):

    chat_id = update.message.chat_id
    try:
        # args[0] should contain ip address
        ipaddress = args[0]
        print(ipaddress)
        if subnet.check_ip_address(ipaddress) == False:
            update.message.reply_text('Ip not correct')
            return

        subnetmask = args[1]

        print(subnetmask)
        print('subnetmask[0] = ', subnetmask[0])

        if subnetmask[0] == '/':
            print('---here---')
            if subnet.check_subnet_prefix(subnetmask) == False:
                update.message.reply_text('Prefix not correct')
                return


        else:
            print('---there---')

            if subnet.check_subnet_mask(subnetmask) == False:
                update.message.reply_text('Mask not correct')
                return


        (decimal_mask, mask_octets_decimal) = ('', [])

        if subnetmask[0] == '/':
            numericPrefix = int(subnetmask[1:])
            (decimal_mask, mask_octets_decimal) = subnet.convert_subnet_prefix_to_binarystring(numericPrefix)
        else:
            (decimal_mask, mask_octets_decimal) = subnet.convert_mask_to_binary_string(subnetmask)


        (wildcard_mask, no_of_ones, no_of_zeros, no_of_hosts) = subnet.calculate_wildcard_mask(decimal_mask, mask_octets_decimal)
        print('calculate_wildcard_mask = ', subnet.calculate_wildcard_mask(decimal_mask, mask_octets_decimal))

        result = subnet.convert_ip_to_binary_string(ipaddress, no_of_ones, no_of_zeros, no_of_hosts, wildcard_mask)
        print('result = ', result)
        update.message.reply_text(result)

    except (IndexError, ValueError):
        update.message.reply_text('Usage example:\n'
                                '/subnet 10.1.1.12 255.255.255.248 \n'
                                'or\n'
                                '/subnet 10.1.1.12 /30')



def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(secrets.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("subnet", parse_ip,
                                  pass_args=True,
                                  pass_chat_data=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
