import csv
import requests
import json
from openai import OpenAI

# 步骤1: 读取CSV文件并转换为文本
def csv_to_text(csv_path):
    text_lines = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # 用制表符分隔列，保持表格结构
            text_lines.append("\t".join(row))
    return "\n".join(text_lines)


# 步骤2: 构建API请求
def chatgpt_api(csv_text,question):

    client = OpenAI(
        base_url='',
        api_key='',
    )
    prompt = f"""
    Please write Verilog code based on FSM security knowledge and code requirements.FSM security knowledge:
    {csv_text}

    code requirements：{question}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        temperature=0.2,
        model = "deepseek-r1",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

def read_json_files(path) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("Verilog_Engineer : The json data has been read. " )
    return data

# 步骤3: 执行调用
if __name__ == "__main__":
    # 配置参数
    CSV_PATH = ""  # CSV文件路径
    Plan = read_json_files("")
    QUESTION = f"""Instruct:Write correct Verilog code based on the 'query'.Only standard Verilog syntax can be used, not SystemVerilog syntax.
                Task:{Plan}
                """

    # 处理CSV并调用API
    csv_text = csv_to_text(CSV_PATH)
    response = chatgpt_api(csv_text,QUESTION)

