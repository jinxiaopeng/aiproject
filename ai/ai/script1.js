document.addEventListener('DOMContentLoaded', function() {
    // 获取聊天窗口元素
    const chatWindow = document.getElementById('chatWindow');
    
    // 设置聊天窗口初始状态为隐藏
    chatWindow.style.display = 'none';

    const aiFloat = document.getElementById('aiFloat');
    const aiAvatar = document.getElementById('aiAvatar');
    const messageInput = document.getElementById('messageInput');
    const sendMessage = document.getElementById('sendMessage');
    const clearChat = document.getElementById('clearChat');
    const closeChat = document.getElementById('closeChat');
    const chatMessages = document.querySelector('.chat-messages');
    const chatHeader = document.querySelector('.chat-header');

    let isDragging = false;
    let isResizing = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;
    let initialWidth;
    let initialHeight;
    let initialMouseX;
    let initialMouseY;
    let chatXOffset = 0;
    let chatYOffset = 0;
    let hasSentWelcomeMessage = false; // 标志变量

    // LM Studio API配置
    const API_URL = 'http://127.0.0.1:1234/v1/chat/completions';  // 使用127.0.0.1替代localhost
    
    // 检查LM Studio服务器状态
    async function checkLMStudioServer() {
        try {
            // 使用 POST 方法发送一个简单的测试请求
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    messages: [
                        {
                            role: 'user',
                            content: 'test'
                        }
                    ],
                    model: 'local-model',
                    max_tokens: 1,
                    stream: false
                })
            });
            
            // 如果能获取到响应，说明服务器正常运行
            const data = await response.json();
            return data && data.choices && data.choices.length > 0;
        } catch (error) {
            console.error('服务器检查失败:', error);
            return false;
        }
    }

    // 开始调整大小
    function startResize(e) {
        const rect = chatWindow.getBoundingClientRect();
        const isInResizeArea = 
            e.clientX > rect.right - 15 && 
            e.clientY > rect.bottom - 15;

        if (isInResizeArea) {
            isResizing = true;
            initialWidth = chatWindow.offsetWidth;
            initialHeight = chatWindow.offsetHeight;
            initialMouseX = e.clientX;
            initialMouseY = e.clientY;
            chatWindow.classList.add('resizing');
            e.preventDefault();
        }
    }

    // 调整大小过程
    function resize(e) {
        if (!isResizing) return;

        e.preventDefault();
        const deltaX = e.clientX - initialMouseX;
        const deltaY = e.clientY - initialMouseY;

        const newWidth = Math.min(Math.max(initialWidth + deltaX, 280), 800);
        const newHeight = Math.min(Math.max(initialHeight + deltaY, 350), 800);

        chatWindow.style.width = newWidth + 'px';
        chatWindow.style.height = newHeight + 'px';
    }

    // 停止调整大小
    function stopResize() {
        isResizing = false;
        chatWindow.classList.remove('resizing');
    }

    // 开始拖动聊天窗口
    function startChatDrag(e) {
        if (e.target === chatHeader || chatHeader.contains(e.target)) {
            isDragging = true;
            initialX = e.clientX - chatXOffset;
            initialY = e.clientY - chatYOffset;
            chatWindow.classList.add('dragging');
        }
    }

    // 拖动聊天窗口程
    function dragChat(e) {
        if (!isDragging) return;

        e.preventDefault();
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;

        chatXOffset = currentX;
        chatYOffset = currentY;

        // 计算新位置，确保窗口不会超出屏幕
        const rect = chatWindow.getBoundingClientRect();
        const maxX = window.innerWidth - rect.width;
        const maxY = window.innerHeight - rect.height;

        const newX = Math.min(Math.max(currentX, 0), maxX);
        const newY = Math.min(Math.max(currentY, 0), maxY);

        chatWindow.style.transform = `translate(${newX}px, ${newY}px)`;
    }

    // 停止拖动聊天窗口
    function stopChatDrag() {
        isDragging = false;
        chatWindow.classList.remove('dragging');
    }

    // AI头像拖拽相关函数
    function dragStart(e) {
        if (isResizing) return;

        if (e.type === "touchstart") {
            initialX = e.touches[0].clientX - xOffset;
            initialY = e.touches[0].clientY - yOffset;
        } else {
            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;
        }

        if (e.target === aiFloat || aiFloat.contains(e.target)) {
            isDragging = true;
            aiFloat.classList.add('dragging');
        }
    }

    function drag(e) {
        if (!isDragging || isResizing) return;

        e.preventDefault();

        if (e.type === "touchmove") {
            currentX = e.touches[0].clientX - initialX;
            currentY = e.touches[0].clientY - initialY;
        } else {
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
        }

        xOffset = currentX;
        yOffset = currentY;

        setTranslate(currentX, currentY, aiFloat);
    }

    function dragEnd() {
        isDragging = false;
        aiFloat.classList.remove('dragging');
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }

    // 添加事件监听器
    // 聊天窗口大小调整
    chatWindow.addEventListener('mousedown', startResize);
    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);

    // 聊天窗口拖动
    chatHeader.addEventListener('mousedown', startChatDrag);
    document.addEventListener('mousemove', dragChat);
    document.addEventListener('mouseup', stopChatDrag);

    // AI头像拖动
    aiFloat.addEventListener('touchstart', dragStart, false);
    aiFloat.addEventListener('touchend', dragEnd, false);
    aiFloat.addEventListener('touchmove', drag, false);
    aiFloat.addEventListener('mousedown', dragStart, false);
    document.addEventListener('mousemove', drag, false);
    document.addEventListener('mouseup', dragEnd, false);

    // 点击AI头像显示/隐藏聊天窗口
    aiAvatar.addEventListener('click', function() {
        if (chatWindow.style.display === 'none' || !chatWindow.style.display) {
            chatWindow.style.display = 'flex';

            // 自动发送欢迎消息
            if (!hasSentWelcomeMessage) {
                setTimeout(() => {
                    const welcomeMessage = "你好，我是信息安全 AI 小助手";
                    const messageElement = document.createElement('div');
                    messageElement.className = 'message ai-message';
                    
                    // 添加AI头像
                    const aiAvatarDiv = document.createElement('div');
                    aiAvatarDiv.className = 'message-avatar';
                    const robotIcon = document.createElement('div');
                    robotIcon.className = 'robot-icon';
                    robotIcon.textContent = 'AI';
                    aiAvatarDiv.appendChild(robotIcon);
                    
                    // 添加AI消息内容
                    const aiContentDiv = document.createElement('div');
                    aiContentDiv.className = 'message-content';
                    aiContentDiv.textContent = welcomeMessage; // 使用欢迎消息
                    
                    // 组装AI消息
                    messageElement.appendChild(aiAvatarDiv);
                    messageElement.appendChild(aiContentDiv);
                    
                    chatMessages.appendChild(messageElement);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 100); // 延迟发送以确保聊天窗口已显示

                hasSentWelcomeMessage = true; // 设置标志为已发送
            }
        } else {
            chatWindow.style.display = 'none';
        }
    });

    // 关闭聊天窗口
    closeChat.addEventListener('click', function() {
        chatWindow.style.display = 'none';
    });

    // 发送消息到LM Studio API
    async function sendToLMStudio(message) {
        // 过滤掉类似 [PAD151645] 的编码
        const filteredMessage = message.replace(/\[PAD\d+\]/g, '').trim();

        // 首先检查服务器状态
        const serverAvailable = await checkLMStudioServer();
        if (!serverAvailable) {
            throw new Error('LM Studio服务器未响应或未正确配置');
        }

        const requestBody = {
            messages: [
                {
                    role: 'user',
                    content: filteredMessage
                }
            ],
            model: 'local-model',
            temperature: 0.7,
            max_tokens: 2000,
            stream: false
        };

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API请求失败: ${response.status} ${response.statusText}\n${errorText}`);
        }

        const data = await response.json();

        if (!data.choices || !data.choices[0] || !data.choices[0].message) {
            throw new Error('API响应格式不正确');
        }

        // 返回纯文本内容并过滤编码
        return data.choices[0].message.content.replace(/\[PAD\d+\]/g, '').trim(); // 确保返回的内容是纯文本
    }

    // 发送消息
    async function sendMessageHandler() {
        const message = messageInput.value.trim();
        if (message) {
            // 创建用户消息
            const messageElement = document.createElement('div');
            messageElement.className = 'message user-message';
            
            // 添加用户头像
            const avatarDiv = document.createElement('div');
            avatarDiv.className = 'message-avatar';
            const userIcon = document.createElement('div');
            userIcon.className = 'user-icon';
            userIcon.textContent = 'U';
            avatarDiv.appendChild(userIcon);
            
            // 添加消息内容
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = message;
            
            // 组装消息
            messageElement.appendChild(avatarDiv);
            messageElement.appendChild(contentDiv);
            
            chatMessages.appendChild(messageElement);
            messageInput.value = '';
            
            // 显示等待状态
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'message ai-message';
            loadingMessage.innerHTML = `
                <div class="message-avatar">
                    <div class="robot-icon">AI</div>
                </div>
                <div class="message-content">思考中...</div>
            `;
            chatMessages.appendChild(loadingMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // 检查用户输入
            if (message === "你是谁") {
                const aiMessageElement = document.createElement('div');
                aiMessageElement.className = 'message ai-message';
                
                // 添加AI头像
                const aiAvatarDiv = document.createElement('div');
                aiAvatarDiv.className = 'message-avatar';
                const robotIcon = document.createElement('div');
                robotIcon.className = 'robot-icon';
                robotIcon.textContent = 'AI';
                aiAvatarDiv.appendChild(robotIcon);
                
                // 添加AI消息内容
                const aiContentDiv = document.createElement('div');
                aiContentDiv.className = 'message-content';
                aiContentDiv.textContent = "我是信息安全 AI 小助手"; // 预设回复
                
                // 组装AI消息
                aiMessageElement.appendChild(aiAvatarDiv);
                aiMessageElement.appendChild(aiContentDiv);
                
                chatMessages.appendChild(aiMessageElement);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } else {
                // 发送到LM Studio API并获取回复
                const aiResponse = await sendToLMStudio(message);
                
                // 移除加载消息
                chatMessages.removeChild(loadingMessage);

                // 创建AI回复消息
                const aiMessageElement = document.createElement('div');
                aiMessageElement.className = 'message ai-message';
                
                // 添加AI头像
                const aiAvatarDiv = document.createElement('div');
                aiAvatarDiv.className = 'message-avatar';
                const robotIcon = document.createElement('div');
                robotIcon.className = 'robot-icon';
                robotIcon.textContent = 'AI';
                aiAvatarDiv.appendChild(robotIcon);
                
                // 添加AI消息内容
                const aiContentDiv = document.createElement('div');
                aiContentDiv.className = 'message-content';
                aiContentDiv.textContent = aiResponse; // 直接使用 AI 的纯文本回复
                
                // 组装AI消息
                aiMessageElement.appendChild(aiAvatarDiv);
                aiMessageElement.appendChild(aiContentDiv);
                
                chatMessages.appendChild(aiMessageElement);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
    }

    // 清空聊天记录
    clearChat.addEventListener('click', function() {
        chatMessages.innerHTML = '';
    });

    // 发送消息事件监听
    sendMessage.addEventListener('click', sendMessageHandler);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessageHandler();
        }
    });
}); 