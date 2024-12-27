import sys
import json
import logging
from pathlib import Path
from app import app

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    try:
        config_path = Path(__file__).parent.parent / 'config.json'
        logger.info(f"Loading config from {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logger.info(f"Config loaded: {config}")
            return config
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        raise

def main():
    try:
        config = load_config()
        port = int(sys.argv[1]) if len(sys.argv) > 1 else config['port']
        logger.info(f"Starting application on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 