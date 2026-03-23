# -*- coding: utf-8 -*-
"""
DeepSeek API 持续对话终端
支持在终端中与DeepSeek AI进行持续对话
"""

import os
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    api_key='sk-2365a09c63c1482b8bf66f2f817f5070',
    base_url="https://api.deepseek.com"
)

def chat_with_deepseek(messages):
    """
    与DeepSeek进行对话
    
    Args:
        messages (list): 对话消息列表
    
    Returns:
        str: AI回复内容
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 对话失败: {str(e)}"

def main():
    """
    主对话循环
    """
    print("🤖 DeepSeek AI 对话终端")
    print("=" * 50)
    print("💡 输入 'quit' 或 'exit' 退出对话")
    print("💡 输入 'clear' 清空对话历史")
    print("=" * 50)
    
    # 初始化对话历史
    messages = [
        {"role": "system", "content": "你是一个有用的AI助手，请用中文回答用户的问题。"}
    ]
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n👤 您: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！感谢使用DeepSeek AI对话终端！")
                break
            
            # 检查清空命令
            if user_input.lower() in ['clear', '清空']:
                messages = [
                    {"role": "system", "content": "你是一个有用的AI助手，请用中文回答用户的问题。"}
                ]
                print("🧹 对话历史已清空")
                continue
            
            # 检查空输入
            if not user_input:
                print("⚠️  请输入有效内容")
                continue
            
            # 添加用户消息到对话历史
            messages.append({"role": "user", "content": user_input})
            
            # 显示AI正在思考
            print("🤔 AI正在思考...")
            
            # 获取AI回复
            ai_response = chat_with_deepseek(messages)
            
            # 显示AI回复
            print(f"🤖 AI: {ai_response}")
            
            # 添加AI回复到对话历史
            messages.append({"role": "assistant", "content": ai_response})
            
        except KeyboardInterrupt:
            print("\n\n👋 检测到Ctrl+C，正在退出...")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")
            continue

if __name__ == "__main__":
    main()