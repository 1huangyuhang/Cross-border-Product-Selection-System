"""
工具函数模块
包含通用的工具函数和辅助方法
"""
import os
import json
import time
import random
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """设置日志配置"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('temu_crawler.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)


def ensure_directory(directory: str) -> str:
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_random_user_agent() -> str:
    """获取随机User-Agent"""
    # 定义一个包含多个User-Agent字符串的列表
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 iPad Safari/605.1.15"
    ]
    return random.choice(user_agents)


def random_delay(min_delay: float = 1.0, max_delay: float = 3.0) -> None:
    """随机延迟"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def save_json(data: Any, filepath: str) -> bool:
    """保存数据为JSON格式"""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logging.error(f"保存JSON文件失败: {e}")
        return False


def load_json(filepath: str) -> Optional[Dict]:
    """加载JSON文件"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"加载JSON文件失败: {e}")
    return None


def save_csv(data: List[Dict], filepath: str, headers: List[str]) -> bool:
    """保存数据为CSV格式"""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            # 写入表头
            f.write(','.join(f'"{h}"' for h in headers) + '\n')
            # 写入数据
            for row in data:
                values = [str(row.get(h, '')) for h in headers]
                f.write(','.join(f'"{v}"' for v in values) + '\n')
        return True
    except Exception as e:
        logging.error(f"保存CSV文件失败: {e}")
        return False


def extract_json_from_html(html: str, start_marker: str, end_marker: str) -> Optional[Dict]:
    """从HTML中提取JSON数据"""
    try:
        start_pos = html.find(start_marker)
        if start_pos == -1:
            return None
        start_pos += len(start_marker)
        end_pos = html.find(end_marker, start_pos)
        if end_pos == -1:
            return None
        json_str = html[start_pos:end_pos].strip()
        return json.loads(json_str)
    except Exception:
        return None


def clean_text(text: str) -> str:
    """清理文本，移除多余的空白字符"""
    if not text:
        return ""
    return " ".join(text.strip().split())


def extract_price_number(price_text: str) -> float:
    """从价格文本中提取数字"""
    import re
    if not price_text:
        return 0.0
    # 提取数字和小数点
    numbers = re.findall(r'\d+\.?\d*', price_text.replace(',', ''))
    if numbers:
        return float(numbers[0])
    return 0.0


def format_timestamp() -> str:
    """获取格式化的时间戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def validate_url(url: str) -> bool:
    """验证URL格式"""
    import re
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None
