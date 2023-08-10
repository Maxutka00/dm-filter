import sys
import time
from typing import Union, Callable

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.types import InputNotifyPeer, InputPeerNotifySettings
from pyrogram.types import Message
from pyrogram_patch.fsm import State
from pyrogram_patch.fsm import StatesGroup, StateItem
from pyrogram_patch.fsm.filter import StateFilter

from utils import pyro_filters
from config_loader import config


class Question:
    question: str
    answers: list = []
    correct_answer: str = None
    question_branches: list = None
    func: Callable = None

    async def pre_handler(self, message: Message, app: Client):
        pass

    async def after_handler(self, message: Message, app: Client):
        pass

    def __repr__(self):
        return str(self.__class__.__name__) + ":" + self.question


class EmptyQuestion(Question):
    def __init__(self, text: str = ""):
        self.question = text


class QuestionWithTextAnswer(Question):
    def __init__(self, question: str, answers: dict[Callable, list[Question]] = None):
        self.question = question
        if answers:
            self.answers = list(answers.keys())
            self.question_branches = list(answers.values())


class QuestionWithMultipleAnswers(Question):
    def __init__(self, question: str, answers: Union[list[str], dict[str, list[Question]]],
                 text_on_ans: list[str] = None):
        self.question = question
        self.answers = answers
        self.text_on_ans = text_on_ans
        if isinstance(answers, dict):
            self.answers = list(answers.keys())
            self.question_branches = list(answers.values())
        else:
            self.answers = answers


class QuestionWithCorrectAnswer(Question):
    def __init__(self, question: str, correct_answer: str):
        self.question = question
        self.correct_answer = correct_answer


class Dialog:
    class States(StatesGroup):
        pass

    def __init__(self, questions: list[Question], no_questions_in_result: bool = False):
        self.questions = questions
        self.q_list = []
        self.question_handlers = {}
        self.no_questions_in_result = no_questions_in_result
        self.get_all_q()
        print(self.question_handlers)
        # sys.exit()

        self.pyro_handlers = []
        for i in self.question_handlers.items():
            state_item = StateItem()
            setattr(self.States, i[0], state_item)
            f = filters.private & filters.incoming & StateFilter(getattr(self.States, i[0]))
            self.pyro_handlers.append(MessageHandler(self.message_handler, f))

    def get_all_q(self):
        def find_coordinates_with_values(data, coordinates=None):
            if coordinates is None:
                coordinates = []
            if isinstance(data, dict):
                for i, (key, value) in enumerate(data.items()):
                    coordinates.append(str(i))
                    find_coordinates_with_values(value, coordinates)
                    coordinates.pop()
            elif (isinstance(data, QuestionWithMultipleAnswers) or isinstance(data, QuestionWithTextAnswer)) and data.question_branches:
                self.question_handlers.update({f"{':'.join(coordinates)}": data})
                for i, item in enumerate(data.question_branches):
                    coordinates.append(str(i))
                    find_coordinates_with_values(item, coordinates)
                    coordinates.pop()

            elif isinstance(data, list):
                for i, item in enumerate(data):
                    coordinates.append(str(i))
                    find_coordinates_with_values(item, coordinates)
                    coordinates.pop()
            else:
                self.question_handlers.update({f"{':'.join(coordinates)}": data})

        find_coordinates_with_values(self.questions)

    async def message_handler(self, app: Client, message: Message, state: State):
        real_state = state_str(state.state)
        print(real_state)
        next_state = self.get_next_state(real_state)
        this_question = self.question_handlers.get(real_state)
        if isinstance(this_question, QuestionWithCorrectAnswer):
            if message.text != this_question.correct_answer:
                return await message.reply("Incorrect answer")
        elif isinstance(this_question, QuestionWithMultipleAnswers):
            if not message.text.isdigit() or len(this_question.answers) < int(message.text) or 0 > int(message.text):
                return await message.reply("Enter only the number of the selected answer")
            if this_question.question_branches:
                next_state = get_key_by_value(self.question_handlers,
                                              this_question.question_branches[int(message.text) - 1][0])
            if this_question.text_on_ans:
                await message.reply(this_question.text_on_ans[int(message.text) - 1])
        elif isinstance(this_question, QuestionWithTextAnswer) and this_question.question_branches:
            for n, func in enumerate(this_question.answers):
                if func(message.text):
                    next_state = get_key_by_value(self.question_handlers,
                                                  this_question.question_branches[n][0])
                    break
            else:
                return await message.reply("I dont understand you")
        next_q = self.question_handlers.get(next_state)
        if isinstance(next_q, EmptyQuestion):
            if next_q.question:
                await message.reply(next_q.question)
            next_state = self.get_next_state(next_state)
        await state.set_data({state_str(state.state): message.text})
        await this_question.after_handler(message, app)
        if not next_state:
            text = await self.get_text_data(state, message)
            #await message.reply(text)
            await app.send_message(config.receiver_user, text)
            await state.finish()
            await enable_notifications(app, message.chat.id)
            await app.unarchive_chats(message.chat.id)
            return
        else:
            next_q = self.question_handlers.get(next_state)
            if next_q:
                await next_q.pre_handler(message, app)
            await state.set_state(getattr(self.States, next_state))
            await message.reply(self.generate_question(next_state))

    async def get_text_data(self, state: State, message: Message):
        form = []
        for key, data in (await state.get_data()).items():
            question: Question = self.question_handlers.get(key)
            if isinstance(question, QuestionWithMultipleAnswers):
                if self.no_questions_in_result:
                    form.append(f"{question.answers[int(data) - 1]}\n")
                else:
                    form.append(f"{question.question}\n— {question.answers[int(data) - 1]}\n")
            else:
                if self.no_questions_in_result:
                    form.append(f"{data}\n")
                else:
                    form.append(f"{question.question}\n— {data}\n")

        return f"{message.from_user.mention} {'@'+message.from_user.username if message.from_user.username else ''}\n\n" + "\n".join(
                                   form)

    async def enter_dialog_handler(self, app: Client, message: Message, state: State):
        await app.read_chat_history(message.chat.id)
        await disable_notifications(app, message.chat.id)
        await app.archive_chats(message.chat.id)
        text = self.generate_question("0")
        await message.reply(text)
        await state.set_state(getattr(self.States, "0"))

    def generate_question(self, for_state: str):
        message_text = []
        question: Question = self.question_handlers.get(for_state)
        message_text.append(question.question + "\n")
        if isinstance(question, QuestionWithMultipleAnswers):
            for n, answer in enumerate(question.answers):
                message_text.append(f"{n + 1}. {answer}")

        return "\n".join(message_text)

    def get_next_state(self, state):
        state = list(map(int, state.split(":")))
        state.reverse()
        state_copy = state.copy()
        for n, s in enumerate(state_copy):
            this_level = list(filter(lambda x: len(x.split(":")) == len(state_copy) - n, self.question_handlers))
            if this_level and list(filter(lambda x: int(x.split(":")[len(state_copy) - n - 1]) > s, this_level)):
                state[0] += 1
                state.reverse()

                r = ":".join(map(str, state))
                if r not in self.question_handlers:
                    state.reverse()
                    state[0] -= 1
                    state.pop(0)
                else:
                    return r
            else:
                state.pop(0)

    def register_dialog(self, app: Client):
        for i in self.pyro_handlers:
            app.add_handler(i)
        app.add_handler(MessageHandler(self.enter_dialog_handler, filters.private & StateFilter(
            "*") & filters.incoming & pyro_filters.empty_chat_filter))


def state_str(state):
    return state.split("_")[-1]


async def disable_notifications(app, chat_id):
    notify_settings = UpdateNotifySettings(
        peer=InputNotifyPeer(peer=await app.resolve_peer(chat_id)),
        settings=InputPeerNotifySettings(
            show_previews=False,
            mute_until=int(time.time() + 99999999)
        )
    )
    return await app.invoke(notify_settings)


async def enable_notifications(app, chat_id):
    notify_settings = UpdateNotifySettings(
        peer=InputNotifyPeer(peer=await app.resolve_peer(chat_id)),
        settings=InputPeerNotifySettings()
    )
    return await app.invoke(notify_settings)


def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


if __name__ == "__main__":
    dm_filter_dialog = Dialog([QuestionWithTextAnswer("Как дела?"),
                               QuestionWithMultipleAnswers("Зачем?", {"за печкой": [QuestionWithTextAnswer("pechka"),
                                                                                    QuestionWithTextAnswer(
                                                                                        "pochemu pechka")],
                                                                      "так надо": [QuestionWithTextAnswer("nado"),
                                                                                   QuestionWithTextAnswer(
                                                                                       "pochemu nado")]}),
                               QuestionWithTextAnswer("Money?")])
