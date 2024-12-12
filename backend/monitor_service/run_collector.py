import argparse
from collector.system_metrics import start_collector

def main():
    parser = argparse.ArgumentParser(description='系统资源监控数据采集器')
    parser.add_argument('--user-id', type=int, required=True, help='用户ID')
    parser.add_argument('--interval', type=int, default=30, help='采集间隔(秒)')
    
    args = parser.parse_args()
    
    print(f"Starting system metrics collector for user {args.user_id}")
    print(f"Collection interval: {args.interval} seconds")
    
    try:
        start_collector(args.user_id, args.interval)
    except KeyboardInterrupt:
        print("\nCollector stopped by user")
    except Exception as e:
        print(f"\nCollector stopped due to error: {str(e)}")

if __name__ == "__main__":
    main() 