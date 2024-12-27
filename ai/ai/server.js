const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();

// 启用CORS，允许所有来源
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

// 日志中间件
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
    next();
});

// 静态文件服务
app.use(express.static(path.join(__dirname, './')));

// 主页路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'ai.html'));
});

// 代理设置
app.use('/api', createProxyMiddleware({
    target: 'http://localhost:1234',
    changeOrigin: true,
    pathRewrite: {
        '^/api': ''
    },
    onProxyReq: (proxyReq, req, res) => {
        // 添加必要的头部
        proxyReq.setHeader('Origin', 'http://localhost:3000');
    },
    onProxyRes: (proxyRes, req, res) => {
        // 添加CORS头部
        proxyRes.headers['Access-Control-Allow-Origin'] = '*';
        proxyRes.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS';
        proxyRes.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization';
    },
    onError: (err, req, res) => {
        console.error('代理错误:', err);
        res.status(500).send('代理服务器错误');
    }
}));

const PORT = 3000;

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error('服务器错误:', err);
    res.status(500).send('服务器内部错误');
});

// 启动服务器
const server = app.listen(PORT, () => {
    console.log(`服务器正在运行: http://localhost:${PORT}`);
}).on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`错误: 端口 ${PORT} 已被占用`);
    } else {
        console.error('服务器启动错误:', err);
    }
}); 