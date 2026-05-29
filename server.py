import asyncio
import websockets
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Хранилище данных
users = {}
messages = {}
chats = []
connected_clients = {}

# HTTP сервер для раздачи файлов
class ChatHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def run_http_server():
    httpd = HTTPServer(('0.0.0.0', 3000), ChatHTTPHandler)
    print("📱  HTTP сервер: http://localhost:3000")
    httpd.serve_forever()

# WebSocket сервер
async def handle_websocket(websocket, path):
    client_id = str(id(websocket))
    current_user = None
    current_chat = None
    
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get('action')
            
            if action == 'login':
                current_user = data.get('nick', 'User')
                connected_clients[current_user] = websocket
                print(f"👤  {current_user} онлайн")
                
                await websocket.send(json.dumps({
                    'type': 'login_success',
                    'user': current_user
                }))
            
            elif action == 'register':
                email = data.get('email')
                password = data.get('password')
                name = data.get('name', email.split('@')[0])
                
                if email in users:
                    await websocket.send(json.dumps({'type': 'error', 'message': 'Email занят'}))
                else:
                    nick = email.split('@')[0]
                    users[email] = {'nick': nick, 'email': email, 'password': password, 'name': name}
                    await websocket.send(json.dumps({'type': 'register_success', 'user': users[email]}))
            
            elif action == 'login_email':
                email = data.get('email')
                password = data.get('password')
                
                if email not in users:
                    await websocket.send(json.dumps({'type': 'error', 'message': 'Не найден'}))
                elif users[email]['password'] != password:
                    await websocket.send(json.dumps({'type': 'error', 'message': 'Неверный пароль'}))
                else:
                    current_user = users[email]['nick']
                    connected_clients[current_user] = websocket
                    await websocket.send(json.dumps({'type': 'login_success', 'user': users[email]}))
            
            elif action == 'get_chats':
                user_chats = [c for c in chats if current_user in c.get('parts', [])]
                await websocket.send(json.dumps({'type': 'chats', 'chats': user_chats}))
            
            elif action == 'get_messages':
                chat_id = data.get('chatId')
                current_chat = chat_id
                msgs = messages.get(str(chat_id), [])
                await websocket.send(json.dumps({'type': 'messages', 'chatId': chat_id, 'messages': msgs}))
            
            elif action == 'send_message':
                chat_id = str(data.get('chatId'))
                text = data.get('message')
                
                if not chat_id or not text or not current_user:
                    continue
                
                msg = {
                    'id': len(messages.get(chat_id, [])) + 1,
                    's': current_user,
                    't': text,
                    'tm': __import__('datetime').datetime.now().strftime('%H:%M')
                }
                
                if chat_id not in messages:
                    messages[chat_id] = []
                messages[chat_id].append(msg)
                
                # Обновляем чат
                for c in chats:
                    if str(c['id']) == chat_id:
                        c['last'] = text
                        c['time'] = msg['tm']
# Отправляем всем участникам
                chat = next((c for c in chats if str(c['id']) == chat_id), None)
                if chat:
                    for user_nick in chat.get('parts', []):
                        if user_nick in connected_clients:
                            try:
                                await connected_clients[user_nick].send(json.dumps({
                                    'type': 'new_message',
                                    'chatId': chat_id,
                                    'message': msg
                                }))
                            except:
                                pass
            
            elif action == 'create_chat':
                name = data.get('name', 'Чат')
                parts = data.get('parts', [current_user])
                
                chat = {
                    'id': len(chats) + 1,
                    'name': name,
                    'av': name[0].upper(),
                    'color': ['#4a7dff', '#34c759', '#ff9f0a', '#6c5ce7'][len(chats) % 4],
                    'parts': parts,
                    'last': '',
                    'time': ''
                }
                chats.append(chat)
                messages[str(chat['id'])] = []
                
                await websocket.send(json.dumps({'type': 'chat_created', 'chat': chat}))
            
            elif action == 'search':
                query = data.get('query', '').lower()
                results = [u for u in users.values() if query in u['nick'].lower() or query in u['email'].lower()]
                await websocket.send(json.dumps({'type': 'search_results', 'users': results}))
    
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if current_user:
            connected_clients.pop(current_user, None)
        print(f"❌ Отключился: {current_user or client_id}")

async def main():
    # Запускаем HTTP сервер в отдельном потоке
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Запускаем WebSocket сервер
    print("🔌  WebSocket сервер: ws://0.0.0.0:8765")
    async with websockets.serve(handle_websocket, '0.0.0.0', 8765):
        await asyncio.Future()

if __name__ == '__main__':
    print("=" * 50)
    print("🚀  СЕРВЕР ЧАТА НА PYTHON")
    print("=" * 50)
    asyncio.run(main())
