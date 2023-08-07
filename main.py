import asyncio
import logging

import pyrogram
from pyrogram import Client
from pyrogram_patch import patch
from pyrogram_patch.fsm.storages import MemoryStorage

import questions
from config_loader import config
from utils.dialog import Dialog, QuestionWithTextAnswer, QuestionWithMultipleAnswers, QuestionWithCorrectAnswer
from utils.funcs import math_question_gen


async def main():
    logging.basicConfig(level=logging.INFO)
    app = Client("acc", api_id=config.ub.api_id, api_hash=config.ub.api_hash, app_version="0.21.7.1154-arm64-v8a",
                 device_model="OnePlus 7 Pro", system_version="SDK 31")

    patch_manager = patch(app)

    patch_manager.set_storage(MemoryStorage())
    dm_filter_dialog = Dialog(questions.main, no_questions_in_result=True)
    dm_filter_dialog.register_dialog(app)
    await app.start()
    await pyrogram.idle()
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
