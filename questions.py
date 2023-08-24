import copy

from utils import funcs
from utils.dialog import Dialog, QuestionWithTextAnswer, QuestionWithMultipleAnswers, QuestionWithCorrectAnswer, \
    EmptyQuestion

payment = QuestionWithMultipleAnswers("Payment method?", ["PayPal", "USDT"], [
    "Payment details:\n<code>symbolstone@gmail.com</code>\nSend me a transaction ID when paid.",
    "Payment details:USDT - TRC20\n<code>TBdgATDewH1CmWLeuT6EhTkW5QAKCSGRHn</code>\nSend me a transaction ID when paid."])
copy.deepcopy(payment)

send_messages_groups = [QuestionWithTextAnswer("What groups is about?"),
                        QuestionWithTextAnswer("What is group language?"),
                        QuestionWithTextAnswer(
                            "The price is $50 to send messages to 1000 groups.\nHow many messages do you want to send?"),
                        copy.deepcopy(payment)]
send_messages_users = [QuestionWithTextAnswer("What your target audience is about?"),
                       QuestionWithTextAnswer("What language?"),
                       QuestionWithTextAnswer("The price is $50 per 1000 DMs. How many messages do you want to send?"),
                       copy.deepcopy(payment)]
invite_users = [QuestionWithTextAnswer("What your target audience is about?"),
                QuestionWithTextAnswer("What language?"),
                QuestionWithTextAnswer("Your group/channel link?"),
                QuestionWithTextAnswer(
                    "The price is $50 per 1000 invited. All members will be real and active.\nHow many members do you want to invite?"),
                copy.deepcopy(payment)]
market = QuestionWithMultipleAnswers("Choose type:", {"Send messages into the groups.": send_messages_groups,
                                                      "Send direct messages to user.": send_messages_users,
                                                      "Invite members/subscriber to your group/channel.": invite_users})

find_list_groups = [
    QuestionWithTextAnswer("All groups will be legit and active, type your requirements:\n\nWhat groups is about?"),
    QuestionWithTextAnswer("Groups language?"),
    QuestionWithTextAnswer("The price is $10 per 100 groups.\nHow many groups do you want?",
                           {funcs.less_than_100: [QuestionWithTextAnswer("Free search available on Teleteg.com and @TeletegBot")],
                            funcs.bigger_than_100: [copy.deepcopy(payment)]})]

find_list_channels = [
    QuestionWithTextAnswer("All channels will be legit and active, type your requirements:\n\nWhat channels is about?"),
    QuestionWithTextAnswer("Channels language?"),
    QuestionWithTextAnswer("The price is $10 per 100 channels.\nHow many channels do you want?",
                           {funcs.less_than_100: [QuestionWithTextAnswer("Free search available on Teleteg.com and @TeletegBot")],
                            funcs.bigger_than_100: [copy.deepcopy(payment)]})]

find_list_members = [QuestionWithMultipleAnswers("Choose quantity:", {
    "Members from one group": [QuestionWithTextAnswer("Free feature available on Teleteg.com")],
    "Members from many groups": [QuestionWithTextAnswer("What groups is about?"),
                                                           QuestionWithTextAnswer("Groups language?"),
                                                           QuestionWithTextAnswer(
                                                               "The price is $10 per 1000 admins.\nHow many admins do you want?",
                                                               {funcs.less_than_1000: [QuestionWithTextAnswer("link to the website and bot.")],
                                                                funcs.bigger_than_1000: [copy.deepcopy(payment)]})]})]

find_list_admins = [
    QuestionWithMultipleAnswers("From where?", {"From groups": [QuestionWithTextAnswer("What groups is about?"),
                                                           QuestionWithTextAnswer("Groups language?"),
                                                           QuestionWithTextAnswer(
                                                               "The price is $10 per 1000 admins.\nHow many admins do you want?",
                                                               {funcs.less_than_1000: [QuestionWithTextAnswer("link to the website and bot.")],
                                                                funcs.bigger_than_1000: [copy.deepcopy(payment)]})],
                                           "From channels": [QuestionWithTextAnswer("What channels is about?"),
                                                             QuestionWithTextAnswer("Channels language?"),
                                                             QuestionWithTextAnswer("The price is $10 per 1000 admins.\nHow many admins do you want?",
                                                                 {funcs.less_than_1000: [QuestionWithTextAnswer("link to the website and bot.")],
                                                                  funcs.bigger_than_1000: [copy.deepcopy(payment)]})]})]
find_list = QuestionWithMultipleAnswers("What do you want to find?", {"Groups": find_list_groups,
                                                                      "Channels": find_list_channels,
                                                                      "Members": find_list_members,
                                                                      "Admins": find_list_admins})

find_user_groups = [QuestionWithTextAnswer("Search User at Teleteg.com"),
                    QuestionWithMultipleAnswers("The price for custom research is $50", {
                        "Agree": [QuestionWithTextAnswer("Write username"), copy.deepcopy(payment)],
                        "Not agree": [EmptyQuestion()]})]
find_user_messages = [QuestionWithTextAnswer("Request beta test at @Teleteg_Support"),
                      QuestionWithMultipleAnswers("Custom research price is $50+", {
                          "Agree": [QuestionWithTextAnswer("Write the username that you want to check."),
                                    copy.deepcopy(payment)],
                          "Not agree": [EmptyQuestion()]})]
find_mentions = [QuestionWithTextAnswer("Request beta test at @Teleteg_Support"),
                 QuestionWithMultipleAnswers("Custom research price is $50+", {
                     "Agree": [QuestionWithTextAnswer("Write the username that you want to check."),
                               copy.deepcopy(payment)],
                     "Not agree": [EmptyQuestion()]})]

telegram_search = QuestionWithMultipleAnswers("What kind of search do you need?",
                                              {"Find list of target groups/channels, members/admins.": [find_list],
                                               "Find out what groups the user in": find_user_groups,
                                               "Find messages that user wrote in Telegram groups": find_user_messages,
                                               "Find messages in groups where your keyword was mentioned.": find_mentions})

advertise = [QuestionWithMultipleAnswers("Advertise on our website or in a bot?", ["Website", "Bot"]),
             QuestionWithTextAnswer("Type your website or channel link?"),
             QuestionWithMultipleAnswers("What kind of placement?", ["link", "banner"]),
             QuestionWithMultipleAnswers("Prices starting from $50 a month.",
                                         {"Agree": [copy.deepcopy(payment)], "Not agree": [EmptyQuestion()]})]
partnering = [QuestionWithTextAnswer("Your name, company name or a link to your website."),
              QuestionWithTextAnswer("Describe your offer in a few words.")]
other = [QuestionWithTextAnswer("Send a short description of what you are looking for.")]

main = [QuestionWithMultipleAnswers("Please choose from below:", {"Market in Telegram": [market],
                                              "Telegram Search": [telegram_search],
                                              "Advertise on our website or in a bot": advertise,
                                              "Partnering": partnering,
                                              "Other": other})]

test = find_list_channels
