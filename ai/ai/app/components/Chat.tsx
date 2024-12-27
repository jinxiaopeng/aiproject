import React, { useState } from 'react';
import './Chat.css'; // 导入 CSS 文件

// 定义消息类型
type Message = {
    text: string;
    sender: 'user' | 'ai';
};

function Chat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isDragging, setIsDragging] = useState(false);
    const [offset, setOffset] = useState({ x: 0, y: 0 });
    const [position, setPosition] = useState({ x: 100, y: 100 }); // 设置初始位置

    const handleSend = async () => {
        const response = await sendToAI(input);
        setMessages([...messages, { text: input, sender: 'user' }, { text: response, sender: 'ai' }]);
        setInput('');
    };

    const handleMouseDown = (e: React.MouseEvent) => {
        setIsDragging(true);
        setOffset({ x: e.clientX - position.x, y: e.clientY - position.y });
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        if (isDragging) {
            const newX = e.clientX - offset.x;
            const newY = e.clientY - offset.y;
            setPosition({ x: newX, y: newY }); // 更新位置
        }
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    return (
        <div id="chat-container">
            <div
                id="chat-window"
                className={`chat-draggable ${isDragging ? 'dragging' : ''}`}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                style={{ transform: `translate(${position.x}px, ${position.y}px)` }} // 应用位置
            >
                <div className="chat-window">
                    {messages.map((msg, index) => (
                        <div key={index} className={msg.sender}>
                            {msg.text}
                        </div>
                    ))}
                </div>
                <label htmlFor="chat-input" className="hidden-label">输入消息</label>
                <input
                    id="chat-input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="输入消息..."
                />
                <button onClick={handleSend}>发送</button>
            </div>
            <div className="ai-component">
                {/* 这里是 AI 组件的内容 */}
                <div>AI 组件</div>
            </div>
        </div>
    );
}

// 发送消息到 AI 组件的函数
async function sendToAI(message: string) {
    return "AI 的响应"; // 示例响应
}

export default Chat; 