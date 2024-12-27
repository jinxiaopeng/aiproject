from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import logging
import json
import time

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 容器配置
CONTAINER_CONFIG = {
    'sql_injection_basic': {
        'image': 'sql_injection_basic:latest',
        'internal_port': 8081,
        'prefix': 'sql_basic'
    },
    'sql_injection_advanced': {
        'image': 'sql_injection_advanced:latest',
        'internal_port': 8082,
        'prefix': 'sql_adv'
    }
}

def generate_container_name(challenge_type, user_id=None):
    """生成统一的容器名称"""
    prefix = CONTAINER_CONFIG[challenge_type]['prefix']
    timestamp = int(time.time())
    user_suffix = f"_user{user_id}" if user_id else ""
    return f"{prefix}{user_suffix}_{timestamp}"

def get_container_status(container_name):
    """获取容器状态"""
    result = run_command(f'docker ps -a --filter name={container_name} --format "{{{{.Status}}}},{{{{.Ports}}}}"')
    if not result['success']:
        return None
    
    output = result['output'].strip()
    if not output:
        return None
        
    status, ports = output.split(',', 1) if ',' in output else (output, '')
    return {
        'running': 'Up' in status,
        'status': status,
        'ports': ports
    }

def run_command(command):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/api/challenge/start', methods=['POST'])
def start_challenge():
    try:
        data = request.get_json()
        challenge_id = data.get('challengeId')
        challenge_type = data.get('challengeType')  # sql_injection_basic 或 sql_injection_advanced
        user_id = data.get('userId')
        port = data.get('port')

        if not all([challenge_id, challenge_type, port]):
            return jsonify({'success': False, 'message': '参数不完整'}), 400

        if challenge_type not in CONTAINER_CONFIG:
            return jsonify({'success': False, 'message': '未知的挑战类型'}), 400

        # 生成容器名称
        container_name = generate_container_name(challenge_type, user_id)
        
        # 检查容器状态
        status = get_container_status(container_name)
        
        if status and status['running']:
            return jsonify({
                'success': True, 
                'message': '容器已经在运行',
                'container_name': container_name,
                'status': status
            })

        # 如果容器存在但没有运行，先删除它
        if status:
            run_command(f'docker rm {container_name}')

        # 创建新容器
        config = CONTAINER_CONFIG[challenge_type]
        result = run_command(
            f'docker run -d --name {container_name} '
            f'-p {port}:{config["internal_port"]} '
            f'--memory=512m --cpus=0.5 '
            f'--health-cmd="curl -f http://localhost:{config["internal_port"]} || exit 1" '
            f'--health-interval=10s --health-timeout=5s --health-retries=3 '
            f'{config["image"]}'
        )

        if not result['success']:
            return jsonify({'success': False, 'message': f'创建容器失败: {result["error"]}'}), 500

        # 等待容器启动
        time.sleep(2)
        status = get_container_status(container_name)

        logger.info(f'Successfully started container {container_name}')
        return jsonify({
            'success': True, 
            'message': '容器启动成功',
            'container_name': container_name,
            'status': status
        })

    except Exception as e:
        logger.error(f'Error starting container: {str(e)}')
        return jsonify({'success': False, 'message': f'启动容器失败: {str(e)}'}), 500

@app.route('/api/challenge/stop', methods=['POST'])
def stop_challenge():
    try:
        data = request.get_json()
        container_name = data.get('containerName')

        if not container_name:
            return jsonify({'success': False, 'message': '参数不完整'}), 400

        # 检查容器状态
        status = get_container_status(container_name)
        if not status:
            return jsonify({'success': False, 'message': '容器不存在'}), 404

        if not status['running']:
            return jsonify({'success': True, 'message': '容器已经停止'})

        # 停止容器
        stop_result = run_command(f'docker stop -t 10 {container_name}')  # 10秒超时
        if not stop_result['success']:
            return jsonify({'success': False, 'message': f'停止容器失败: {stop_result["error"]}'}), 500

        # 再次检查状态
        status = get_container_status(container_name)
        
        return jsonify({
            'success': True, 
            'message': '容器已停止',
            'container_name': container_name,
            'status': status
        })

    except Exception as e:
        logger.error(f'Error stopping container: {str(e)}')
        return jsonify({'success': False, 'message': f'停止容器失败: {str(e)}'}), 500

@app.route('/api/challenge/status', methods=['GET'])
def get_challenge_status():
    try:
        container_name = request.args.get('containerName')
        if not container_name:
            return jsonify({'success': False, 'message': '参数不完整'}), 400

        status = get_container_status(container_name)
        if not status:
            return jsonify({'success': False, 'message': '容器不存在'}), 404

        return jsonify({
            'success': True,
            'container_name': container_name,
            'status': status
        })

    except Exception as e:
        logger.error(f'Error getting container status: {str(e)}')
        return jsonify({'success': False, 'message': f'获取容器状态失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 