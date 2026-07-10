
import json
import time
from typing import List, Dict, Optional

from openai import api_key
from typing_extensions import Annotated
import sys
import io
import subprocess
from vcdvcd import VCDVCD
from pyverilog.vparser.parser import parse

import requests
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
import os
import openai
from langchain.chains import GraphCypherQAChain
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from py2neo import *


def check_verilog_syntax(path:Annotated[str, "The path of Verilog file."])\
        -> Annotated[str, "A syntax checking tool for Verilog files."]:
    """
    使用iverilog检查Verilog代码语法
    :param file_path: Verilog文件路径
    :return: 编译器输出信息
    """
    try:
        # 调用iverilog进行语法检查
        result = subprocess.run(['iverilog', '-t', 'null', path], capture_output=True, text=True)

        if result.returncode == 0:
            print("Syntax check passed. No errors found.")
            return "Syntax check passed. No errors found."
        else:
            print("Syntax check had been found!!!!.")
            return f"Syntax check failed:\n{result.stderr}"

    except Exception as e:
        return f"Error occurred while checking syntax: {str(e)}"


class Tool:

    @property
    def name(self):
        return self.__class__.__name__

    def __call__(self, **kwargs) -> str:
        raise NotImplementedError


class GoogleSearch(Tool):
    """使用谷歌搜索问题"""

    description = '使用谷歌搜索问题，它的输入是一个问题，参数名为 query，输出是搜索结果。'

    def __init__(self, api_key: Optional[str] = None, topk: int = 5) -> None:
        self.api_key = api_key or os.getenv('SERPER_API_KEY')
        self.base_url = 'https://google.serper.dev/search'
        self.topk = topk

    def __call__(self, query: str) -> str:
        headers = {'x-api-key': self.api_key, 'Content-Type': 'application/json'}
        response = requests.post(self.base_url, params={'q': query}, headers=headers)
        results = self._parse_snippets(response.json())
        return ' '.join(results)

    def _parse_snippets(self, results: dict) -> str:
        # copy from https://github.com/langchain-ai/langchain
        snippets = []

        if results.get('answerBox'):
            answer_box = results.get('answerBox', {})
            if answer_box.get('answer'):
                return [answer_box.get('answer')]
            elif answer_box.get('snippet'):
                return [answer_box.get('snippet').replace('\n', ' ')]
            elif answer_box.get('snippetHighlighted'):
                return answer_box.get('snippetHighlighted')

        if results.get('knowledgeGraph'):
            kg = results.get('knowledgeGraph', {})
            title = kg.get('title')
            entity_type = kg.get('type')
            if entity_type:
                snippets.append(f'{title}: {entity_type}.')
            description = kg.get('description')
            if description:
                snippets.append(description)
            for attribute, value in kg.get('attributes', {}).items():
                snippets.append(f'{title} {attribute}: {value}.')

        for result in results['organic'][:self.topk]:
            if 'snippet' in result:
                snippets.append(result['snippet'])
            for attribute, value in result.get('attributes', {}).items():
                snippets.append(f'{attribute}: {value}.')

        if len(snippets) == 0:
            assert False, 'No snippets found in the search results.'

        return snippets


class CurrentTime(Tool):
    """获取当前时间"""

    description = '获取当前时间的工具，它不接受输入，输出是当前时间。'

    def __call__(self) -> str:
        currtent_time = time.asctime(time.localtime(time.time()))
        return currtent_time



class Iverilog(Tool):
    """"iverilog toll"""
    description = 'Verilog code syntax check, its input is a problem, the parameter name is path, and the output is the check result'

    def __call__(self, path: str) -> str:
        return self.check_verilog_syntax(path)

    def check_verilog_syntax(self, path):
        """
        使用iverilog检查Verilog代码语法
        :param file_path: Verilog文件路径
        :return: 编译器输出信息
        """
        try:
            # 调用iverilog进行语法检查
            result = subprocess.run(['iverilog', '-t', 'null', path], capture_output=True, text=True)

            if result.returncode == 0:
                return "Syntax check passed. No errors found."
            else:
                return f"Syntax check failed:\n{result.stderr}"

        except Exception as e:
            return f"Error occurred while checking syntax: {str(e)}"

def save_verilog_files(path:Annotated[str, "A syntax checking tool for Verilog files."],
                       code:Annotated[str, "The verilog target code."]):
    with open(path, 'w') as f:
        f.write(code)
    print("Verilog_Engineer : The Verilog code has been saved. !!")

def save_json_files(path:Annotated[str, "Then save the plan that planner generated"],
                       plan:Annotated[str, "The FSM plan:"]) -> None:
    with open(path, 'w') as f:
        f.write(plan)
    print("Verilog_Engineer : The Verilog plan has been saved. !!")

def read_json_files(path:Annotated[str, "Read the Verilog code generation plan generated in the previous stage."]) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("Verilog_Engineer : The json data has been read. " )
    return data


def ast_generation(path: str) -> str:
    ast, directives = parse([path], debug=False)

    captured_output = io.StringIO()
    sys.stdout = captured_output
    ast.show(buf=captured_output)
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    output = "This is AST of the verilog code:\n" + output + "\n"
    return output


def verilog_checker(verilog_code_path: str, testbench_path: str, wave:bool) -> str:

    syntax_result = subprocess.run(['iverilog', '-o', 'nul', '-Wall', verilog_code_path], capture_output=True, text=True)


    if syntax_result.returncode == 0:
        res = "******- Simulator Output -****** \n"
        print('The code Syntax is correct.')
        subprocess.run(['iverilog', '-o', 'duttable', testbench_path, verilog_code_path], capture_output=True, text=True)
        subprocess.run(['vvp', '-n', 'duttable'], capture_output=True, text=True)

        truetable = VCDVCD("D://pycharm//autogen-0.2.36//V2.0//Input//truetable.vcd")
        duttable = VCDVCD("D://pycharm//autogen-0.2.36//duttable.vcd")
        sig_list = truetable.references_to_ids.keys()
        res += "The verilog code syntax is correct.\n"


        is_wrong = False
        for sig_name in sig_list:
            if str(truetable[sig_name].tv) != str(duttable[sig_name].tv):
                is_wrong = True

        if (is_wrong):
            res += "This verilog code is wrong"
            return res
        else:

            res += "The verilog code function is correct."
            waveform_files = ["D://pycharm//autogen-0.2.36//duttable.vcd",
                              "D://pycharm//autogen-0.2.36//V2.0//Input//truetable.vcd"]
            subprocess.run(["gtkwave"] + waveform_files)
            return res
    else:
        print("The code Syntax is error.\n")
        raise Exception(f"Iverilog syntax check failed: {syntax_result.stderr}")

import os
import json
import re
import ast
from typing import Dict, Any

import os
import re
import json


def extract_confirm_info(intermediate_steps):
    """从中间步骤中提取并结构化confirm信息"""
    confirm_info = []

    # 遍历所有中间步骤元素
    for step in intermediate_steps:
        # 检查当前步骤是否包含context信息
        if isinstance(step, dict) and 'context' in step:
            context_list = step['context']

            # 遍历context列表中的每个条目
            for item in context_list:
                confirm_node = item.get("c")
                if not confirm_node:
                    continue

                # 提取基本信息
                confirm_entry = {
                    "confirm": confirm_node.get("name", "N/A"),
                    "confirm_source": confirm_node.get("source", "知识图谱"),
                    "confirm_positive": [],
                    "confirm_positive_examples": [],
                    "confirm_negative": [],
                    "confirm_negative_examples": []
                }

                # 处理正向信息
                if 'cp' in item:
                    confirm_entry["confirm_positive"].append(item['cp'].get("name", "N/A"))
                if 'cpe' in item:
                    confirm_entry["confirm_positive_examples"].append(item['cpe'].get("name", "N/A"))

                # 处理负向信息
                if 'cn' in item:
                    confirm_entry["confirm_negative"].append(item['cn'].get("name", "N/A"))
                if 'cne' in item:
                    confirm_entry["confirm_negative_examples"].append(item['cne'].get("name", "N/A"))

                confirm_info.append(confirm_entry)

    return confirm_info


def dynamics_security_prompt():
    # 创建阶段映射字典（处理大小写和空格差异）
    data = read_json_files('./Output/retrieved_data.json')
    vul_plan = read_json_files('./Output/Verilog_Plan.json')
    # stage_mapping = {
    #     "statetransition": "State Transition",
    #     "outputlogic": "Output Logic"
    # }

    # 合并Security信息
    # for category in ["Structure", "Potential"]:
    #     for item in data[category]:
    #         # 标准化stage名称
    #         original_stage = item["stage"]
    #         normalized_stage = original_stage.lower().replace(" ", "")
    #
    #         # 查找匹配的subtask
    #         for subtask in vul_plan["subtasks"]:
    #             if stage_mapping.get(normalized_stage, "").lower() == subtask["type"].lower():
    #                 # 构建security信息
    #                 security_info = {
    #                     "description": item["description"],
    #                     "Security information": item["Security information"],
    #                     "position": item["position"]
    #                 }
    #
    #                 # 合并到subtask
    #                 subtask["Security"] = security_info
    #                 break
    vul_plan["Suggestion"] = data

    # 定义输出路径并确保目录存在
    output_dir = "./Output"
    output_path = os.path.join(output_dir, "merged_security_plan.json")
    os.makedirs(output_dir, exist_ok=True)  # 自动创建不存在的目录

    # 写入JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vul_plan, f, indent=2, ensure_ascii=False)  # 禁用ASCII转义以支持中文

    print(f"✅ 安全增强计划已保存至: {os.path.abspath(output_path)}")


import json
from collections import defaultdict

def transform_vulnerability_data(raw_data):
    """
    将原始漏洞数据转换为结构化的JSON格式（移除node_type）

    参数:
        raw_data: 原始漏洞数据列表

    返回:
        结构化后的漏洞数据列表
    """
    # 第一步：按漏洞名称分组
    grouped_data = defaultdict(lambda: {
        "weakness_name": "",
        "description": "",
        "GoodExample": [],
        "BadExample": [],
        "alleviation_suggestions": []
    })

    # 处理每条原始记录
    for record in raw_data:
        weakness_name = record["weakness_name"]
        group = grouped_data[weakness_name]

        # 设置漏洞基本信息（只设置一次）
        if not group["weakness_name"]:
            group["weakness_name"] = weakness_name
            group["description"] = record["description"]

        # 根据关系类型添加到对应类别（只保留content）
        relation_type = record["relation_type"]
        content = record["related_node_name"]

        if relation_type == "GoodExample":
            group["GoodExample"].append(content)
        elif relation_type == "BadExample":
            group["BadExample"].append(content)
        elif relation_type == "alleviation_suggestions":
            group["alleviation_suggestions"].append(content)
        # 可在此处添加其他关系类型的处理

    # 转换为列表并返回
    return list(grouped_data.values())


def graph_retrieval_tool(description: str) -> dict:
    API_SECRET_KEY = 'sk-NiOdvWU8t9N0qyFXF1811dE3E0B34eF6A99c544b927dDb1f'
    os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
    os.environ["OPENAI_API_BASE"] = "https://api.v3.cm/v1"

    model = ChatOpenAI(temperature=0.0)

    url = "bolt://localhost:7687"
    username = "neo4j"
    password = "huzi1234"
    graph = Neo4jGraph(url=url, username=username, password=password)

    # 使用参数化查询模板
    query_template = """
    MATCH (w:Weakness {name: '%s'})-[:stage|alleviation_suggestions|GoodExample|BadExample|manner]->(n)
    RETURN  n.name AS nodeName, labels(n)[0] AS nodeType
    """
    query = query_template % description

    chain1 = GraphCypherQAChain.from_llm(
        llm=model,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True,
        return_intermediate_steps=True
    )

    # 传递参数执行查询
    response = chain1.invoke({"query": query})

    # 提取并处理中间步骤的数据
    raw_results = response['intermediate_steps'][1]['context']
    security_info = []
    stage_info = []  # 单独存储stage信息

    for record in raw_results:
        node_type = record.get("nodeType", "Unknown")
        node_name = record.get("nodeName", "Unknown")

        if node_type == "stage":
            stage_info.append(node_name)  # 收集所有stage节点名称
        else:
            # 非stage节点保持原有结构
            security_info.append({node_type: node_name})

    # 取第一个stage作为顶层字段值（根据样例数据只有一个stage）
    stage_value = stage_info[0] if stage_info else "No stage information"

    return {
        "weakness_name": description,
        "stage": stage_value,  # 新增平级字段
        "Security information": security_info
    }

def save_json_file(data):
    file_path = './Output/retrieved_data.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"检索结果已保存至: {file_path}")


def graph_retrieval_tool_cwe(cwe_id: str, STG: str) -> dict:
    API_SECRET_KEY = 'sk-NiOdvWU8t9N0qyFXF1811dE3E0B34eF6A99c544b927dDb1f'
    os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
    os.environ["OPENAI_API_BASE"] = "https://api.v3.cm/v1"

    model = ChatOpenAI(temperature=0.0)

    url = "bolt://localhost:7687"
    username = "neo4j"
    password = "huzi1234"
    graph = Neo4jGraph(
        url=url,
        username=username,
        password=password
    )

    chain1 = GraphCypherQAChain.from_llm(llm=model, graph=graph, verbose=True, allow_dangerous_requests=True,
                                         return_intermediate_steps=True)

    # 检索 confirm, confirm_positive, confirm_positive_example, confirm_negative, confirm_negative_example
    query_template = """
    MATCH (w:Weakness {name: '%s'})-[:confirm]->(c:confirm)
    OPTIONAL MATCH (c)-[:confirm_positive]->(cp:confirm_positive)
    OPTIONAL MATCH (cp)-[:confirm_positive_example]->(cpe:confirm_positive_example)
    OPTIONAL MATCH (c)-[:confirm_negative]->(cn:confirm_negative)
    OPTIONAL MATCH (cn)-[:confirm_negative_example]->(cne:confirm_negative_example)
    RETURN c, cp, cpe, cn, cne
    """
    query = query_template % cwe_id
    response = chain1.invoke({"query": query})

    intermediate_steps = response['intermediate_steps']

    # 使用辅助函数提取confirm信息
    confirm_info = extract_confirm_info(intermediate_steps)

    # 单独提取所有confirm字段内容
    confirm_contents = [entry["confirm"] for entry in confirm_info]

    # 将信息整合为字符串
    confirm_info_str = ""
    for entry in confirm_info:
        confirm_info_str += f"确认信息 [{entry['confirm_source']}]：{entry['confirm']}\n"
        confirm_info_str += f"正向类型：{', '.join(entry['confirm_positive'])}\n"
        confirm_info_str += f"正向示例：{', '.join(entry['confirm_positive_examples'])}\n"
        confirm_info_str += f"负向类型：{', '.join(entry['confirm_negative'])}\n"
        confirm_info_str += f"负向示例：{', '.join(entry['confirm_negative_examples'])}\n\n"

    # 构建用于判断的提示词
    model_template = PromptTemplate(
        input_variables=["confirm_info_str", "STG"],
        template="""
        你是一个专业的安全研究员，现在需要判断FSM的STG中是否属于存在特定漏洞。
        漏洞确认信息如下：
        {confirm_info_str}

        FSM的STG信息如下：
        STG：{STG}

        请根据漏洞确认信息中的关于漏洞的正向类型和正向示例和负向类型和负向示例，首先根据示例总结出这类漏洞的表现形式和特点，然后判断该STG中是否存在属于漏洞的表现形式。
        如果属于正向（confirm_positive），请返回 "YES"； 如果属于负向（confirm_negative）示例，请返回 "NO"。
        在判断过程中，请详细说明你的推理过程。
        """
    )

    formatted_prompt = model_template.format(confirm_info_str=confirm_info_str,STG=STG)

    output = model.invoke(formatted_prompt)
    return {
        "cwe_id": cwe_id,
        "state_condition": STG,
        "judgment": output,
        "confirm_info": confirm_info,
        "confirm_contents": confirm_contents
    }


from py2neo import Graph, Node, Relationship, NodeMatcher

def FSMCR():
    try:
        with open("D://pycharm//autogen-0.2.36//V2.0//Output//FSMCR.json", "r") as file:
            data = json.load(file)
        print(data["states"])
    except FileNotFoundError:
        print("文件未找到，请检查路径！")
    except json.JSONDecodeError:
        print("JSON 文件格式错误！")

    graph = Graph('bolt://localhost:7687', auth=('neo4j', 'huzi1234'), name='neo4j')

    #graph.delete_all()
    graph.begin()

    for k in range(len(data["states"])):
            cql = '''
                                     MERGE (a:State{name:\'%s\', output:"\'%s\'", condition:"\'%s\'",protected:"\'%s\'",init_state:False})
                                   ''' % (data["states"][k]["name"],
                                          data["states"][k]["output"],
                                          data["states"][k]["condition"],
                                          data["states"][k]["protected"]
                                          )
            graph.run(cql)
    for i in range(len(data["init_state"])):
        cql = '''
                                             MERGE (a:State{name:\'%s\'})
                                             ON MATCH SET a.init_state = true
                                           ''' % (data["states"][i]["name"],
                                                  )
        graph.run(cql)
    for j in range(len(data["transitions"])):
            cql = '''
                                     MERGE (a:State{name:\'%s\'})
                                     MERGE (b:State{name:\'%s\'})
                                     MERGE (a)-[:TRANSITION{condition:\'%s\'}]-> (b)
                                   ''' % (data["transitions"][j]["from"],
                                          data["transitions"][j]["to"],
                                          data["transitions"][j]["condition"],
                                          )
            graph.run(cql)

    return None

from neo4j import GraphDatabase

def Dead_State(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            f"MATCH (n:{label}) "
            f"WHERE (n)-[:{rel_type}]->(n)"
            "AND NOT EXISTS {"
            f"MATCH (n)-[:{rel_type}]->(m)"
            "WHERE m <> n"
            "}"
            "AND NOT EXISTS {"
            f"MATCH (m)-[:{rel_type}]->(n)"
            "WHERE m <> n"
            "}"
            "RETURN n"
        )
        result = tx.run(query)
        return [record["n"] for record in result]

    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("1.Dead State")
            if not nodes:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                graph = Graph('bolt://localhost:7687', auth=('neo4j', 'huzi1234'), name='neo4j')
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str = str + f"  - State_ID: {node.id}, Name: {dict(node)}"
                    # draw = """
                    #                     MERGE (a:State{name:\'%s\'})
                    #                     MERGE (a)-[:DEAD_STATE]-> (a)
                    #                 """ % (dict(node)['name'])
                    # graph.run(draw)
                data["Structure"]["Dead State"] = str

    finally:
        driver.close()

def Static_Lock(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            f"MATCH (n:{label})<-[:{rel_type}]-(m)"
            "WHERE m <> n "
            "AND NOT EXISTS {"
            f"MATCH (n)-[:{rel_type}]->(j)"
            "WHERE j <> n"
            "}"
            "RETURN DISTINCT n"
        )
        result = tx.run(query)
        re = [record["n"] for record in result]
        return re

    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("2.Static Lock")
            if not nodes:

                print(f"ALL '{label}' Nodes Are Safe")
            else:
                graph = Graph('bolt://localhost:7687', auth=('neo4j', 'huzi1234'), name='neo4j')
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str = str + f"  - State_ID: {node.id}, Name: {dict(node)}"
                    # draw = """
                    #     MERGE (a:State{name:\'%s\'})
                    #     MERGE (a)-[:STATIC_LOCK]-> (a)
                    # """%(dict(node)['name'])
                    # graph.run(draw)
                data["Structure"]["Static Deadlock"] = str
    finally:
        driver.close()


def Dynamic_Lock(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            f"MATCH path = (start:State)-[:TRANSITION*3..10]->(start)"
            f"WHERE ALL(n IN nodes(path)[1..-1] WHERE n <> start)"
            "WITH [n IN nodes(path)[0..-1] | n.name] AS cycle "
            "RETURN DISTINCT apoc.coll.sort(cycle) AS DeadlockCycle"
        )
        result = tx.run(query)
        return result

    try:
        with driver.session() as session:
            result = query_executor(session, label, rel_type)
            print("3.Dynamic Lock")
            deadlock = [record["DeadlockCycle"] for record in result]
            print(deadlock)
            data["Structure"]["Dynamic Deadlock"] = deadlock
    finally:
        driver.close()

def Unreachable_State(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            f"MATCH (n:{label})-[:{rel_type}]->(m)"
            "WHERE m <> n AND n.init_state = false "
            "AND NOT EXISTS {"
            f"MATCH (j)-[:{rel_type}]->(n)"
            "WHERE j <> n"
            "}"
            "RETURN DISTINCT n"
        )
        result = tx.run(query)
        return [record["n"] for record in result]

    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("4.Unreachable_State")
            if not nodes:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str += f"  - State_ID: {node.id}, Name: {dict(node)}"
                data["Structure"]["Unreachable State"] = str
    finally:
        driver.close()

def Live_Lock(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            f"MATCH (n:{label})-[:{rel_type}]->(m)"
            "WHERE m <> n AND n.init_state = true "
            "AND NOT EXISTS {"
            f"MATCH (j)-[:{rel_type}]->(n)"
            "WHERE j <> n"
            "}"
            "RETURN DISTINCT n"
        )
        result = tx.run(query)
        return [record["n"] for record in result]

    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("5.Live_Lock")
            if not nodes:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str = str + f"  - State_ID: {node.id}, Name: {dict(node)}"
                data["Structure"]["Live lock"] = str
    finally:
        driver.close()



def CWE_825(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))

    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            f"MATCH (n:{label})<-[:{rel_type}]-(m)"
            "WHERE m <> n "
            "AND NOT EXISTS {"
            f"MATCH (n)-[:{rel_type}]->(j)"
            "WHERE j <> n"
            "}"
            "RETURN DISTINCT n"
        )
        result = tx.run(query)
        re = [record["n"] for record in result]
        return re

    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("6.CWE-825")
            if not nodes:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str = str + f"  - State_ID: {node.id}, Name: {dict(node)}"
                data["Structure"]["CWE-825"] = str
    finally:
        driver.close()


def CWE_190(label, rel_type, data):
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        query = (
            """MATCH (n:State) WHERE n.condition <> "'None'" RETURN n"""
        )
        result = tx.run(query)
        return [record["n"] for record in result]
    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("7.CWE-190")
            if not nodes:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str += f"  - State_ID: {node.id}, Name: {dict(node)}"
                data["Potential"]["CWE-190"] = str
    finally:
        driver.close()

def CWE_367(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            """MATCH (n:State) WHERE n.protected <> "'NULL'" RETURN n"""
        )
        result = tx.run(query)
        return [record["n"] for record in result]
    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("8.CWE-367")
            if not nodes:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str += f"  - State_ID: {node.id}, Name: {dict(node)}"
                data["Potential"]["CWE-367"] = str
    finally:
        driver.close()


def CWE_561(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            """MATCH (n:State) RETURN COUNT(n) AS state_count """
        )
        result = tx.run(query)
        record = result.single()
        return record["state_count"] if record else 0
    try:
            with driver.session() as session:
                state_count  = session.execute_read(query_executor, label, rel_type)
                print("8.CWE-561")
                print(f"State节点数量: {state_count}")
    finally:
            driver.close()

def CWE_570(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))

    def query_executor(tx, label, rel_type):
        # 动态构造查询，确保label和rel_type已做安全校验
        query = (
            f"MATCH (a:{label})-[r:{rel_type}]->(b:{label}) "
            "WHERE r.condition <> 'None' "
            "RETURN r"
        )
        result = tx.run(query)
        return [record["r"] for record in result]  # 返回关系对象列表

    try:
        with driver.session() as session:
            relationships = session.execute_read(query_executor, label, rel_type)
            print("11.CWE-570")
            if not relationships:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for rel in relationships:
                    # 获取关系属性
                    condition = rel.get('condition')
                    new_st = f"  - transitions:[    from: state_name,    to: state_name,    condition: '{condition}']\n"
                    str += new_st
                data["Potential"]["CWE-570"] = str
    finally:
        driver.close()

def CWE_571(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))

    def query_executor(tx, label, rel_type):
        # 动态构造查询，确保label和rel_type已做安全校验
        query = (
            f"MATCH (a:{label})-[r:{rel_type}]->(b:{label}) "
            "WHERE r.condition <> 'None' "
            "RETURN r"
        )
        result = tx.run(query)
        return [record["r"] for record in result]  # 返回关系对象列表

    try:
        with driver.session() as session:
            relationships = session.execute_read(query_executor, label, rel_type)
            print("12.CWE-571")
            if not relationships:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for rel in relationships:
                    # 获取关系属性
                    condition = rel.get('condition')
                    new_st = f"  - transitions:[    from: state_name,    to: state_name,    condition: '{condition}']\n"
                    str += new_st
                data["Potential"]["CWE-571"] = str
    finally:
        driver.close()

def FIF(label, rel_type, data):
    # 替换为你的Neo4j连接信息
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "huzi1234"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    def query_executor(tx, label, rel_type):
        # 注意：动态构造Cypher时需确保输入安全（避免注入攻击）
        query = (
            """MATCH (n:State) WHERE n.protected <> "'None'" RETURN n"""
        )
        result = tx.run(query)
        return [record["n"] for record in result]
    try:
        with driver.session() as session:
            nodes = session.execute_read(query_executor, label, rel_type)
            print("16.FIF")
            if not nodes:
                print(f"ALL '{label}' Nodes Are Safe")
            else:
                str = ""
                for node in nodes:
                    print(f"  - State_ID: {node.id}, Name: {dict(node)}")
                    str += f"  - State_ID: {node.id}, Name: {dict(node)}"
                data["Structure"]["FIF-metric"] = str
    finally:
        driver.close()

def SG_Check():
    data = {"Structure":{}, "Potential":{}}
    Dead_State("State", "TRANSITION", data)
    Static_Lock("State", "TRANSITION", data)
    Dynamic_Lock("State", "TRANSITION", data)
    Unreachable_State("State", "TRANSITION", data)
    Live_Lock("State", "TRANSITION", data)
    #CWE_825("State", "TRANSITION", data)

    #CWE_190("State", "TRANSITION", data)
    #CWE_367("State", "TRANSITION", data)
    #
    #CWE_570("State", "TRANSITION", data)
    #CWE_571("State", "TRANSITION", data)
    # CWE_561("State", "TRANSITION", data)
    #FIF("State", "TRANSITION", data)

    print(data)
    with open("./Output/vul.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # indent 让格式更美观






    



