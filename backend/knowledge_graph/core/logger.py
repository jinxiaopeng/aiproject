import logging
import sys

# 创建日志记录器
logger = logging.getLogger("knowledge_graph")
logger.setLevel(logging.INFO)

# 创建控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# 添加处理器到日志记录器
logger.addHandler(console_handler) 