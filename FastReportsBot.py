from __future__ import print_function
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import fastreport_cloud_sdk
from fastreport_cloud_sdk.rest import ApiException
from pprint import pprint
import json, string, os
from aiogram.utils.markdown import text
import urllib.request
from convert import *



configuration = fastreport_cloud_sdk.Configuration(
    host = "https://fastreport.cloud",
    username = 'apikey',
    password = 'nkaom4tjfw9xyopt1r9e17hodwr4f69bryabkkbk71cy9q5wbf8o')

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

storage = MemoryStorage()
global filetype
filetype=""
b1 = KeyboardButton('/Конвертировать')
b2 = KeyboardButton('/Word')
b3 = KeyboardButton('/Excel')
b4 = KeyboardButton('/PDF')
b5 = KeyboardButton('/Информация')
b6 = KeyboardButton('/PowerPoint')
b7 = KeyboardButton('/XML')
b8 = KeyboardButton('/HTML')
b9 = KeyboardButton('/FPX')
b10 = KeyboardButton('/SVG')
b11 = KeyboardButton('/Тайна')
kb_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b1, b5)
kb1_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b2, b3, b4, b6).row(b7, b8, b9, b10)
kb2_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b11)


async def on_startup(_):
    print('Бот запущен и вышел в онлайн')


@dp.message_handler(commands=['start', 'Начать'])
async def commands_start(message: types.message):
    try:
        await bot.send_message(message.from_user.id,
                               'Добро пожаловать в FastReports! \nДля начала работы выберите команду..',
                               reply_markup=kb_user)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/FastReports_Bot')


@dp.message_handler(commands=['info', 'Информация'])
async def command_info(message: types.message):
    if message.text == 'Информация':
        try:
            help_message = text('FastReportsBot - бот, предназначенный для работы с файлами.',
                                'Во многом упрощает работу с файлами разных типов.',
                                'Ссылка на репозиторий с исходным кодом: ',
                                sep='\n')
            await bot.send_message(message.chat.id, help_message, reply_markup=kb2_user)
            await command_photo()
        except:
            await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/FastReports_Bot')


@dp.message_handler(commands=['Тайна'])
async def command_photo(message: types.message):
    ph = InputFile('img.png', 'rb')
    await bot.send_message(message.from_user.id, 'А вот и тайна!')
    await bot.send_photo(message.from_user.id, photo=ph)


@dp.message_handler(commands=['convert', 'Конвертировать'])
async def convert(message: types.Message):
    await message.reply('Выберите расширение файла для конвертации:', reply_markup=kb1_user)


@dp.message_handler(commands=['Word'])
async def choose_word(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте файл формата .frx')
    with open('type.txt',"w") as f:
        f.write("docx")


@dp.message_handler(commands=['Excel'])
async def choose_excel(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте свой файл')
    with open('type.txt',"w") as f:
        f.write("xlsx")


@dp.message_handler(commands=['PDF'])
async def choose_pdf(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте свой файл')
    with open('type.txt',"w") as f:
        f.write("pdf")


@dp.message_handler(commands=['PowerPoint'])
async def choose_power(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте свой файл')
    with open('type.txt',"w") as f:
        f.write("pptx")


@dp.message_handler(commands=['XML'])
async def choose_xml(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте свой файл')
    with open('type.txt',"w") as f:
        f.write("xml")


@dp.message_handler(commands=['HTML'])
async def choose_html(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте свой файл')
    with open('type.txt',"w") as f:
        f.write("html")


@dp.message_handler(commands=['FPX'])
async def choose_fpx(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте свой файл')
    with open('type.txt',"w") as f:
        f.write("fpx")


@dp.message_handler(commands=['SVG'])
async def choose_svg(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте свой файл')
    with open('type.txt',"w") as f:
        f.write("svg")


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def scan_handler(msg: types.Message):
    await msg.reply(text='Файл получен...')
    document_id = msg.document.file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    name = msg.document.file_name
    token1='5609948735:AAF0VPybW--FBeVNhbuBtNeZ4U0LWxfHBsw'
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{token1}/{fi}', f'importFiles/{name}')
    await bot.send_message(msg.chat.id, 'Файл успешно сохранён, идёт конвертация...')
    print(name)
    strtype=""
    with open('type.txt',"r") as f:
        strtype=f.read()
    print(strtype)
    filepath = export_frx(strtype,name)
    await bot.send_message(msg.chat.id, 'Файл успешно конвертирован.\nГена на...\nНет, Гена возьми')
    await msg.answer_document(InputFile(filepath))
    await bot.send_message(msg.chat.id, 'Спасибо за пользование ботом. C уважением команда NextGen', reply_markup=kb_user)
    

    

@dp.message_handler()
async def echo_send(message: types.message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('Cenzura.json')))) != set():
        await message.answer("Маты запрещены!")
        await message.delete()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
