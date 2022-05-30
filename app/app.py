#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install telethon


# In[2]:

import asyncio

async def main():
        # Тут обозначим и запустим наш клиент - при запуске этой ячейки нужно будет ввести номер телефона, 
        # ввести код подтверждения которое прийдет в ваш телеграм канал - с этого момента вы будете авторизованы 
        # и сможете скачивать сообщения из тех каналов, на которые подписаны
        API_ID = 12125354
        API_HASH = '32b18b9170c167da78af810695ad7404'

        from telethon import TelegramClient
        client = TelegramClient('crawler_session', API_ID, API_HASH)

        await client.start()


        # In[3]:


        # Импортируем нужные фунции из файлика db_func.py + создадим экземпляр SQLITE таблички с именем messages.db - в ней и будем хранить всю информацию
        from db_func import conn, store_dialog, create_table, store_message, store_user


        # In[4]:


        # Заполним таблицу со всеми нашими диалогами
        async for dialog in client.iter_dialogs():
                try:
                        store_dialog(dialog.id,dialog.name)
                except:
                        pass


        # Подключиться к файлу с БД SQLITE можно любым доступным средством - включая DBEAVER.
        # 
        # Посмотрим id интересующих нас диалогов в DBEAVER в таблице dialogs и поместим их в список  dialog_list

        # In[5]:


        # Так - список всех диалогов можно вывести на экран


        # In[9]:


        # Например добавим в список канал с id '-1001534342934
        dialog_list = [140687089]


        # In[10]:


        # Наполним табличку с пользователями инфой из интересующих нас диалогов - 
        # Важно -  не из всех диалогов можно получить список пользователей(может быть ограничено админом канала)
        for dialog in dialog_list:
                try:
                        part = await client.get_participants(dialog)
                        print(dialog,'Получен список пользователей')
                except:
                        part = None
                        print(f'Для канала {dialog} нельзя запросить пользователей')
                try:
                        for p in part:
                                try:
                                        store_user(p.id,p.username,p.phone,p.first_name,p.last_name)
                                except:
                                        pass
                except:
                        pass


        # In[12]:


        # Выгрузим все текствые сообщения из интересующих нас каналов 
        # Важно - выгрузка идет с последнего сообщения к первому - по одному (поэтому важно сделать первую выгрузку до конца) - 
        # При повтороном запуске скрипта таблицы с сообщениями будут только дополнены новыми сообщениями начиная с последнего полученного
        # Для каждого канала будет создана своя таблица название_таблицы = id_канала
        for chanel in dialog_list:
                messages = await client.get_messages(chanel)
                print(f'Всего сообщений в канале {chanel} - ',messages.total)
                i = 0
                create_table(chanel)
                c = conn.cursor()
                last_msg = c.execute(f'''SELECT MAX(message_id) FROM "{chanel}"''').fetchone()[0]
                conn.commit()
                async for message in client.iter_messages(chanel):
                        if last_msg == None or message.id > last_msg:
                                if message.from_id:
                                        try:
                                                author = message.from_id.user_id
                                        except:
                                                author = message.from_id.channel_id
                                elif message.peer_id:
                                        try:
                                                author = message.peer_id.channel_id
                                        except:
                                                author = message.peer_id.user_id
                                else:
                                        author = 'unc'
                                store_message(chanel,message.id,author,message.text,message.date,message.views)
                        else:
                                print('Дельта загружена')
                                break
                        i = i+1
                        if i % 1000 == 0:
                                print(f'Загружено {i} сообщений')
                print('Все сообщения загружены')


        # In[ ]:


asyncio.run(main())

