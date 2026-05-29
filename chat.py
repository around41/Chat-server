<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Чат</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: -apple-system, sans-serif; background:#0a0a0f; color:#f0f0f5; height:100vh; display:flex; align-items:center; justify-content:center; overflow:hidden; }
        .screen { width:100%; height:100vh; display:none; flex-direction:column; }
        .screen.active { display:flex; }
        
        .auth { background:#0a0a0f; align-items:center; justify-content:center; padding:24px; gap:12px; }
        .logo { font-size:48px; }
        .title { font-size:24px; font-weight:800; }
        .input { width:100%; max-width:320px; padding:14px; border-radius:12px; border:none; background:#1a1a25; color:#fff; font-size:15px; outline:none; }
        .btn { width:100%; max-width:320px; padding:14px; border-radius:12px; border:none; font-size:16px; font-weight:700; cursor:pointer; }
        .btn-primary { background:#4a7dff; color:#fff; }
        .btn-outline { background:transparent; border:2px solid #333; color:#ccc; }
        .error { color:#ff453a; font-size:12px; text-align:center; }
        
        .app { background:#0a0a0f; }
        .header { padding:14px 18px; background:#12121a; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.06); }
        .header-title { font-weight:800; font-size:20px; }
        .btn-sm { padding:8px 16px; border-radius:10px; border:none; font-size:13px; font-weight:600; cursor:pointer; }
        .btn-red { background:#ff453a; color:#fff; }
        .btn-blue { background:#4a7dff; color:#fff; }
        
        .list { flex:1; overflow-y:auto; }
        .empty { display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; gap:10px; color:#8e8e9a; }
        
        .chat-item { display:flex; align-items:center; gap:12px; padding:14px 18px; cursor:pointer; border-bottom:1px solid rgba(255,255,255,0.06); }
        .chat-item:active { background:rgba(255,255,255,0.03); }
        .avatar { width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:18px; background:#4a7dff; flex-shrink:0; }
        .chat-info { flex:1; }
        .chat-name { font-weight:600; }
        .chat-preview { font-size:13px; color:#5c5c6a; }
        
        .chat-screen { position:absolute; top:0; left:0; width:100%; height:100%; background:#0a0a0f; display:none; flex-direction:column; }
        .chat-screen.active { display:flex; }
        .chat-header { padding:12px 14px; background:#12121a; display:flex; align-items:center; gap:10px; border-bottom:1px solid rgba(255,255,255,0.06); }
        .messages { flex:1; overflow-y:auto; padding:8px 14px; display:flex; flex-direction:column; gap:2px; }
        .msg { display:flex; max-width:82%; margin-bottom:2px; }
        .msg.in { align-self:flex-start; }
        .msg.out { align-self:flex-end; }
        .bubble { padding:10px 14px; border-radius:18px; font-size:15px; }
        .in .bubble { background:#1a1a25; }
        .out .bubble { background:linear-gradient(135deg,#4a7dff,#6c5ce7); color:#fff; }
        .sender { font-size:10px; color:#4a7dff; margin-bottom:2px; padding-left:6px; }
        .time { font-size:9px; color:#5c5c6a; margin-top:2px; text-align:right; }
        
        .input-bar { padding:8px 12px; background:#12121a; display:flex; gap:8px; border-top:1px solid rgba(255,255,255,0.06); }
        .msg-input { flex:1; background:#1a1a25; border:none; border-radius:22px; padding:10px 16px; font-size:15px; color:#fff; outline:none; }
        .send-btn { width:40px; height:40px; border-radius:50%; border:none; font-size:18px; background:#4a7dff; color:#fff; cursor:pointer; }
    </style>
</head>
<body>
<!-- АВТОРИЗАЦИЯ -->
<div class="screen auth active" id="authScreen">
    <div class="logo">💬 </div>
    <div class="title">Чат</div>
    <input type="email" class="input" id="authEmail" placeholder="Email" autocomplete="email" />
    <input type="password" class="input" id="authPassword" placeholder="Пароль" />
    <div class="error" id="authError"></div>
    <button class="btn btn-primary" onclick="login()">Войти</button>
    <button class="btn btn-outline" onclick="register()">Создать аккаунт</button>
</div>

<!-- ПРИЛОЖЕНИЕ -->
<div class="screen app" id="appScreen">
    <div id="mainView" style="display:flex;flex-direction:column;height:100%;">
        <div class="header">
            <span class="header-title">💬  Чаты</span>
            <div style="display:flex;gap:8px;">
                <button class="btn-sm btn-blue" onclick="searchUsers()">🔍</button>
                <button class="btn-sm btn-red" onclick="location.reload()">Выйти</button>
            </div>
        </div>
        <div class="list empty" id="chatList"><div style="font-size:48px;opacity:0.3;">💬 </div><div>Нет чатов</div></div>
        <div style="padding:10px;"><button class="btn btn-primary" style="width:100%;" onclick="createChat()">＋ Новый чат</button></div>
    </div>
    <div id="searchView" style="display:none;flex-direction:column;height:100%;">
        <div class="header"><button class="btn-sm" style="background:#333;color:#fff;" onclick="showMain()">←</button><span class="header-title">🔍 Поиск</span><div></div></div>
        <div style="padding:10px;"><input class="input" id="searchInput" placeholder="Имя или email" style="width:100%;" oninput="doSearch()" /></div>
        <div class="list" id="searchResults"></div>
    </div>
    <div class="chat-screen" id="chatScreen">
        <div class="chat-header"><button class="btn-sm" style="background:#333;color:#fff;" onclick="closeChat()">←</button><div class="avatar" id="chatAv" style="width:36px;height:36px;font-size:14px;">#</div><div style="font-weight:700;" id="chatName">Чат</div></div>
        <div class="messages" id="messagesArea"></div>
        <div class="input-bar"><input class="msg-input" id="msgInput" placeholder="Сообщение..." /><button class="send-btn" onclick="sendMsg()">↑</button></div>
    </div>
</div>

<script>
var ws, currentUser, currentChat, chats=[], cmsgs=[];
var WS_URL = 'ws://' + location.hostname + ':8765';

function connectWS() {
    ws = new WebSocket(WS_URL);
    
    ws.onopen = function() {
        console.log('✅ WebSocket подключен');
        if (currentUser) {
            ws.send(JSON.stringify({ action: 'login', nick: currentUser }));
            loadChats();
        }
    };
    
    ws.onmessage = function(e) {
        var data = JSON.parse(e.data);
        
        if (data.type === 'login_success') {
            currentUser = data.user.nick || data.user;
            document.getElementById('authScreen').classList.remove('active');
            document.getElementById('appScreen').classList.add('active');
            loadChats();
        }
        
        if (data.type === 'register_success') {
            currentUser = data.user.nick;
            document.getElementById('authScreen').classList.remove('active');
            document.getElementById('appScreen').classList.add('active');
            loadChats();
        }
        
        if (data.type === 'error') {
            document.getElementById('authError').textContent = data.message;
        }
        
        if (data.type === 'chats') {
            chats = data.chats;
            renderChats();
        }
        
        if (data.type === 'messages') {
            cmsgs = data.messages;
            renderMsgs();
        }
        
        if (data.type === 'new_message') {
            if (String(data.chatId) === String(currentChat)) {
                cmsgs.push(data.message);
                renderMsgs();
            }
            loadChats();
        }
if (data.type === 'chat_created') {
            loadChats();
            openChat(data.chat.id, data.chat.name, data.chat.av, data.chat.color);
        }
        
        if (data.type === 'search_results') {
            var el = document.getElementById('searchResults');
            if (!data.users.length) {
                el.innerHTML = '<div style="padding:20px;text-align:center;color:#8e8e9a;">Ничего не найдено</div>';
            } else {
                el.innerHTML = data.users.map(u => 
                    '<div class="chat-item" onclick="startPrivateChat(\''+u.email+'\',\''+u.name+'\')"><div class="avatar" style="width:40px;height:40px;font-size:15px;">'+u.name[0].toUpperCase()+'</div><div class="chat-info"><div class="chat-name">'+u.name+'</div><div style="font-size:12px;color:#5c5c6a;">@'+u.nick+'</div></div></div>'
                ).join('');
            }
        }
    };
    
    ws.onclose = function() {
        console.log('🔴  WebSocket отключен');
        setTimeout(connectWS, 3000);
    };
}

function login() {
    var email = document.getElementById('authEmail').value.trim();
    var password = document.getElementById('authPassword').value.trim();
    if (!email || !password) return;
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'login_email', email, password }));
    }
}

function register() {
    var email = document.getElementById('authEmail').value.trim();
    var password = document.getElementById('authPassword').value.trim();
    if (!email || !password) return;
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'register', email, password, name: email.split('@')[0] }));
    }
}

function loadChats() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'get_chats' }));
    }
}

function renderChats() {
    var el = document.getElementById('chatList');
    if (!chats.length) {
        el.className = 'list empty';
        el.innerHTML = '<div style="font-size:48px;opacity:0.3;">💬 </div><div>Нет чатов</div>';
        return;
    }
    el.className = 'list';
    el.innerHTML = chats.map(c =>
        '<div class="chat-item" onclick="openChat(\''+c.id+'\',\''+c.name+'\',\''+c.av+'\',\''+(c.color||'#4a7dff')+'\')"><div class="avatar" style="background:'+(c.color||'#4a7dff')+';">'+c.av+'</div><div class="chat-info"><div class="chat-name">'+c.name+'</div><div class="chat-preview">'+(c.last||'Нет сообщений')+'</div></div></div>'
    ).join('');
}

function openChat(id, name, av, color) {
    currentChat = String(id);
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'get_messages', chatId: currentChat }));
    }
    document.getElementById('chatAv').textContent = av;
    document.getElementById('chatAv').style.background = color;
    document.getElementById('chatName').textContent = name;
    document.getElementById('mainView').style.display = 'none';
    document.getElementById('searchView').style.display = 'none';
    document.getElementById('chatScreen').classList.add('active');
}

function renderMsgs() {
    var el = document.getElementById('messagesArea');
    el.innerHTML = cmsgs.map(m =>
        '<div class="msg '+(m.s===currentUser?'out':'in')+'"><div>'+(m.s!==currentUser?'<div class="sender">'+m.s+'</div>':'')+'<div class="bubble">'+m.t+'</div><div class="time">'+m.tm+'</div></div></div>'
    ).join('');
    el.scrollTop = el.scrollHeight;
}

function sendMsg() {
    var text = document.getElementById('msgInput').value.trim();
    if (!text || !currentChat) return;
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'send_message', chatId: currentChat, message: text }));
    }
    document.getElementById('msgInput').value = '';
}

function createChat() {
    var name = prompt('Название чата:');
    if (!name) return;
    if (ws && ws.readyState === WebSocket.OPEN) {
ws.send(JSON.stringify({ action: 'create_chat', name: name, parts: [currentUser] }));
    }
}

function closeChat() {
    currentChat = null;
    document.getElementById('chatScreen').classList.remove('active');
    document.getElementById('mainView').style.display = 'flex';
    loadChats();
}

function searchUsers() {
    document.getElementById('mainView').style.display = 'none';
    document.getElementById('searchView').style.display = 'flex';
}

function showMain() {
    document.getElementById('searchView').style.display = 'none';
    document.getElementById('mainView').style.display = 'flex';
}

function doSearch() {
    var q = document.getElementById('searchInput').value.trim();
    if (!q) { document.getElementById('searchResults').innerHTML = ''; return; }
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'search', query: q }));
    }
}

function startPrivateChat(email, name) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'create_chat', name: name, parts: [currentUser, email.split('@')[0]] }));
    }
}

// Запуск
connectWS();
</script>
</body>
</html>
