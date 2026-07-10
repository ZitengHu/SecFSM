import autogen
import argparse
import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher
from config import Agents_config
from utils import get_prompts
from tool import *
from tool import graph_retrieval_tool
import json
import re
from autogen import ConversableAgent


def create_security():
    import pandas as pd
    from py2neo import Graph
    import numpy as np

    df = pd.read_csv('', engine='python')

    # 替换所有NaN值为空字符串
    df = df.replace({np.nan: ''})

    graph = Graph('bolt://localhost:7687', auth=('neo4j', 'huzi1234'), name='neo4j')
    graph.delete_all()

    for i, line in df.iterrows():
        # 跳过所有属性都为空的节点
        if all(value == '' for value in line[['Weakness', 'ID', 'Description']]):
            continue

        # 构建参数字典，处理可能的NaN值
        parameters = {
            'weakness': line['Weakness'] if pd.notna(line['Weakness']) else '',
            'id': line['ID'] if pd.notna(line['ID']) else '',
            'description': line['Description'] if pd.notna(line['Description']) else '',
            'stage': line['stage'] if pd.notna(line['stage']) else '',
            'type': line['type'] if pd.notna(line['type']) else '',
            'fc1': line['FidelityChecking1'] if pd.notna(line['FidelityChecking1']) else '',
            'fc2': line['FidelityChecking2'] if pd.notna(line['FidelityChecking2']) else '',
            'cons': line['Consequence'] if pd.notna(line['Consequence']) else '',
            'cons1': line['Consequence1'] if pd.notna(line['Consequence1']) else '',
            'cons2': line['Consequence2'] if pd.notna(line['Consequence2']) else '',
            'good_ex': line['Good Example'] if pd.notna(line['Good Example']) else '',
            'good_ex1': line['Good Example1'] if pd.notna(line['Good Example1']) else '',
            'bad_ex': line['Bad Example'] if pd.notna(line['Bad Example']) else '',
            'bad_ex1': line['Bad Example1'] if pd.notna(line['Bad Example1']) else '',
            'suggestion': line['alleviation suggestions'] if pd.notna(line['alleviation suggestions']) else '',
            'manner': line['manner'] if pd.notna(line['manner']) else '',
            'confirm': line['confirm'] if pd.notna(line['confirm']) else '',
            'cp1': line['confirm_p1'] if pd.notna(line['confirm_p1']) else '',
            'cp1_e1': line['confirm_p1_e1'] if pd.notna(line['confirm_p1_e1']) else '',
            'cp1_e2': line['confirm_p1_e2'] if pd.notna(line['confirm_p1_e2']) else '',
            'cp2': line['confirm_p2'] if pd.notna(line['confirm_p2']) else '',
            'cp2_e1': line['confirm_p2_e1'] if pd.notna(line['confirm_p2_e1']) else '',
            'cp2_e2': line['confirm_p2_e2'] if pd.notna(line['confirm_p2_e2']) else '',
            'cn1': line['confirm_n1'] if pd.notna(line['confirm_n1']) else '',
            'cn1_e1': line['confirm_n1_e1'] if pd.notna(line['confirm_n1_e1']) else '',
            'cn1_e2': line['confirm_n1_e2'] if pd.notna(line['confirm_n1_e2']) else '',
            'cn2': line['confirm_n2'] if pd.notna(line['confirm_n2']) else '',
            'cn2_e1': line['confirm_n2_e1'] if pd.notna(line['confirm_n2_e1']) else '',
            'cn2_e2': line['confirm_n2_e2'] if pd.notna(line['confirm_n2_e2']) else ''
        }

        # 构建Cypher查询
        cql = """
            MERGE (a:Weakness{name: $weakness, id: $id, description: $description})

            // 只创建非空stage节点
            FOREACH (_ IN CASE WHEN $stage <> '' THEN [1] ELSE [] END |
                MERGE (b:stage{name: $stage})
                MERGE (a)-[:stage]-> (b)
            )
            FOREACH (_ IN CASE WHEN $type <> '' THEN [1] ELSE [] END |
                MERGE (a1:type{name: $type})
                MERGE (a)-[:type]-> (a1)
            )
            

            // 只创建非空FidelityChecking节点
            FOREACH (_ IN CASE WHEN $fc1 <> '' THEN [1] ELSE [] END |
                MERGE (c:FidelityChecking{name: $fc1})
                MERGE (a)-[:FidelityChecking]-> (c)
            )
            FOREACH (_ IN CASE WHEN $fc2 <> '' THEN [1] ELSE [] END |
                MERGE (d:FidelityChecking{name: $fc2})
                MERGE (a)-[:FidelityChecking]-> (d)
            )

            // 只创建非空Consequence节点
            FOREACH (_ IN CASE WHEN $cons <> '' THEN [1] ELSE [] END |
                MERGE (e:Consequence{name: $cons})
                MERGE (a)-[:Consequence]-> (e)
            )
            FOREACH (_ IN CASE WHEN $cons1 <> '' THEN [1] ELSE [] END |
                MERGE (f:Consequence{name: $cons1})
                MERGE (a)-[:Consequence]-> (f)
            )
            FOREACH (_ IN CASE WHEN $cons2 <> '' THEN [1] ELSE [] END |
                MERGE (g:Consequence{name: $cons2})
                MERGE (a)-[:Consequence]-> (g)
            )

            // 只创建非空GoodExample节点
            FOREACH (_ IN CASE WHEN $good_ex <> '' THEN [1] ELSE [] END |
                MERGE (h:GoodExample{name: $good_ex})
                MERGE (a)-[:GoodExample]-> (h)
            )
            FOREACH (_ IN CASE WHEN $good_ex1 <> '' THEN [1] ELSE [] END |
                MERGE (i:GoodExample{name: $good_ex1})
                MERGE (a)-[:GoodExample]-> (i)
            )

            // 只创建非空BadExample节点
            FOREACH (_ IN CASE WHEN $bad_ex <> '' THEN [1] ELSE [] END |
                MERGE (j:BadExample{name: $bad_ex})
                MERGE (a)-[:BadExample]-> (j)
            )
            FOREACH (_ IN CASE WHEN $bad_ex1 <> '' THEN [1] ELSE [] END |
                MERGE (k:BadExample{name: $bad_ex1})
                MERGE (a)-[:BadExample]-> (k)
            )

            // 只创建非空alleviation_suggestions节点
            FOREACH (_ IN CASE WHEN $suggestion <> '' THEN [1] ELSE [] END |
                MERGE (l:alleviation_suggestions{name: $suggestion})
                MERGE (a)-[:alleviation_suggestions]-> (l)

                // 只创建非空manner节点
            FOREACH (_ IN CASE WHEN $manner <> '' THEN [1] ELSE [] END |
                    MERGE (m:manner{name: $manner})
                    MERGE (l)-[:alleviation_suggestions]-> (m)
                )
            )

            // 只创建非空confirm节点
            FOREACH (_ IN CASE WHEN $confirm <> '' THEN [1] ELSE [] END |
                MERGE (n:confirm{name: $confirm})
                MERGE (a)-[:confirm]-> (n)

                // confirm_positive部分
                FOREACH (_ IN CASE WHEN $cp1 <> '' THEN [1] ELSE [] END |
                    MERGE (o:confirm_positive{name: $cp1})
                    MERGE (n)-[:confirm_positive]-> (o)

                    FOREACH (_ IN CASE WHEN $cp1_e1 <> '' THEN [1] ELSE [] END |
                        MERGE (p:confirm_positive_example{name: $cp1_e1})
                        MERGE (o)-[:confirm_positive_example]-> (p)
                    )
                    FOREACH (_ IN CASE WHEN $cp1_e2 <> '' THEN [1] ELSE [] END |
                        MERGE (q:confirm_positive_example{name: $cp1_e2})
                        MERGE (o)-[:confirm_positive_example]-> (q)
                    )
                )

                FOREACH (_ IN CASE WHEN $cp2 <> '' THEN [1] ELSE [] END |
                    MERGE (r:confirm_positive{name: $cp2})
                    MERGE (n)-[:confirm_positive]-> (r)

                    FOREACH (_ IN CASE WHEN $cp2_e1 <> '' THEN [1] ELSE [] END |
                        MERGE (s:confirm_p_example{name: $cp2_e1})
                        MERGE (r)-[:confirm_positive_example]-> (s)
                    )
                    FOREACH (_ IN CASE WHEN $cp2_e2 <> '' THEN [1] ELSE [] END |
                        MERGE (t:confirm_positive_example{name: $cp2_e2})
                        MERGE (r)-[:confirm_positive_example]-> (t)
                    )
                )

                // confirm_negative部分
                FOREACH (_ IN CASE WHEN $cn1 <> '' THEN [1] ELSE [] END |
                    MERGE (u:confirm_negative{name: $cn1})
                    MERGE (n)-[:confirm_negative]-> (u)

                    FOREACH (_ IN CASE WHEN $cn1_e1 <> '' THEN [1] ELSE [] END |
                        MERGE (v:confirm_negative_example{name: $cn1_e1})
                        MERGE (u)-[:confirm_negative_e]-> (v)
                    )
                    FOREACH (_ IN CASE WHEN $cn1_e2 <> '' THEN [1] ELSE [] END |
                        MERGE (w:confirm_negative_example{name: $cn1_e2})
                        MERGE (u)-[:confirm_negative_example]-> (w)
                    )
                )

                FOREACH (_ IN CASE WHEN $cn2 <> '' THEN [1] ELSE [] END |
                    MERGE (x:confirm_negative{name: $cn2})
                    MERGE (n)-[:confirm_negative]-> (x)

                    FOREACH (_ IN CASE WHEN $cn2_e1 <> '' THEN [1] ELSE [] END |
                        MERGE (y:confirm_negative_example{name: $cn2_e1})
                        MERGE (x)-[:confirm_negative_example]-> (y)
                    )
                    FOREACH (_ IN CASE WHEN $cn2_e2 <> '' THEN [1] ELSE [] END |
                        MERGE (z:confirm_negative_example{name: $cn2_e2})
                        MERGE (x)-[:confirm_negative_example]-> (z)
                    )
                )
            )
        """

        try:
            graph.run(cql, parameters)
        except Exception as e:
            print(f"Error on row {i}: {e}")
            print(f"Parameters: {parameters}")
            # 可以选择跳过错误继续执行，或者中断
            # raise  # 取消注释以中断执行


from llama_cpp import Llama
def RTL_Coder(prompt:str):


    llm = Llama.from_pretrained(
        repo_id="ishorn5/RTLCoder-v1.1-gguf-4bit",
        filename="ggml-model-q4_0.gguf",
        cache_dir="E:/data/hub/"
    )
    output = llm(
        prompt,
        max_tokens=512,
        echo=True
    )
    generated_text = output['choices'][0]['text']
    return generated_text

#gpt-4o
#claude-3-5-haiku-20241022
#deepseek-r1

def High_level_Plan_gent(args):
    config_list = [
        {
            "model": "gpt-4o",
            'api_key': '',
            'base_url': '',
            "temperature": 0.1,
        }
    ]
    llm_config = {"config_list": config_list, "cache_seed": 42}

    #Agent_state LLM role's prompts
    Agent_state = 'Plan'
    Planner_message = get_prompts(Agent_state, 'Planner',
                                  Agents_config=Agents_config, module_des=args.Modlue_Des)
    Verify_Assistant_message = get_prompts(Agent_state, 'Plan_Verify_Assistant',
                                           Agents_config=Agents_config, module_des=args.Modlue_Des)

    # LLM Role: Planner
    Planner = autogen.ConversableAgent(
        name="Planner",
        system_message = Planner_message,
        code_execution_config=False,
        llm_config=llm_config,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    )

    # LLM Role: Plan Verify Assistant
    Plan_Verify_Assistant = autogen.ConversableAgent(
        name="Plan_Verify_Assistant",
        system_message=Verify_Assistant_message,
        llm_config=llm_config,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode = "NEVER",
    )

    Plan_Verify_Assistant.register_for_llm(name="save_json_files", description="save_json_files")(save_json_files)
    Plan_Verify_Assistant.register_for_execution(name="save_json_files")(save_json_files)
    # chat group
    Plann_Agent = autogen.GroupChat(agents=[Planner, Plan_Verify_Assistant],messages=[], max_round=12)
    # group manager
    Plan_manager = autogen.GroupChatManager(groupchat=Plann_Agent, llm_config=llm_config)

    Planner.initiate_chat(
        Plan_manager,
        message=str(args.Modlue_Des)
    )

#claude-3-5-haiku-20241022
#deepseek-r1
def CSTEE_Agent(args):
    config_list = [
        {
            "model": "gpt-4o",
            'api_key': '',
            'base_url': '',
            "temperature": 0.1,
        }
    ]
    llm_config = {"config_list": config_list, "cache_seed": 42}

    Verilog_Engineer = autogen.ConversableAgent(
        name="Verilog_Engineer",
        system_message=str(Agents_config['state']['CSTEE']['Verilog_Engineer']['Task']),
        llm_config=llm_config,
    )

    user_proxy = autogen.ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    Agent_state = 'CSTEE'
    Verilog_Engineer_message = get_prompts(Agent_state, 'Verilog_Engineer',
                                  Agents_config=Agents_config, module_des=args.Modlue_Des)
    # Register the tool signature with the assistant agent.
    Verilog_Engineer.register_for_llm(name="save_verilog_files", description="save_verilog_files")(save_verilog_files)
    user_proxy.register_for_execution(name="save_verilog_files")(save_verilog_files)
    chat_result = user_proxy.initiate_chat(Verilog_Engineer, message=Verilog_Engineer_message)

def FSRG():
    config_list = [
        {
            "model": "gpt-4o",
            'api_key': '',
            'base_url': '',
            "temperature": 0.1
            ,
        }
    ]
    llm_config = {"config_list": config_list, "cache_seed": 42}
    with open('./V2.0/Output/Verilog_Plan.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    assistant = autogen.ConversableAgent(
        name="Assistant",
        system_message="You are a top-tier Verilog expert with experience in retrieving required information for the following task using graph_retrieval_tool. "
                       "You can help with Retrieving required information "
                       "Return 'TERMINATE' when the task is done.",
        llm_config=llm_config,
    )

    user_proxy = autogen.ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    # Register the tool signature with the assistant agent.
    assistant.register_for_llm(name="graph_retrieval_tool",
                               description="input task_description,return information for task")(
        graph_retrieval_tool)

    # Register the tool function with the user proxy agent.
    user_proxy.register_for_execution(name="graph_retrieval_tool")(graph_retrieval_tool)
    message = """
             ``` JSON:{json}
                 Let's think step by step.Based on the JSON file structure mentioned earlier, I need you to complete the following tasks:
                 1.Use the graph retrieval tool to search based on the following content:{CurrentTask1}
                 2.{Save1}
                 3.{CurrentTask2}
                 4.{Save2}
                 5.{CurrentTask3}
                 6.{Save3}
                 ``` 
    """
    message = message.format(
        json=json_data,
        CurrentTask1="Traverse all nodes and filter out nodes that match 'init_state=True'.",
        Save1="Locate the item with 'id':'3' in the 'subtasks' array of the JSON and fill the organized node information into its' Evidence' field.Do not change other contents of the JSON.",
        CurrentTask2="Extract the State field of each subtask in the 'id':'5' in the 'subtasks' of dynamic_subtasks array from the provided JSON data. Output a list containing only these State values, arranged in order, without any additional information."
                     "According to this list, sequentially call the graph retrieval tool to retrieve only the output_value and output_key of the current state, regardless of other states.",
        Save2="Locate the item with 'id':'5' in the 'subtasks' array of the JSON and fill the output_value and output_key of the state into its' Evidence' field.Do not change other contents of the JSON.",
        CurrentTask3="Extract the State field of each subtask in the 'id':'5' in the 'subtasks' of dynamic_subtasks array from the provided JSON data. Output a list containing only these State values, arranged in order, without any additional information."
                     "According to this list, call the graph retrieval tool sequentially to retrieve which states have a 'TRANSITION' relationship with the current state, the direction of the 'TRANSITION' relationship is from other states to the current state..",
        Save3="Locate the item with 'id':'4' in the 'subtasks' array of the JSON and fill the organized node information into its' Evidence' field.Do not change other contents of the JSON.",
        )
    chat_result = user_proxy.initiate_chat(assistant, message=message)


from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
import os
from langchain.chains import GraphCypherQAChain
from py2neo import *
from neo4j import GraphDatabase
def FSKG_N():
    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "huzi1234")
    )
    # 使用参数化查询模板
    query = """
    MATCH (w:Weakness)-[:type]->(t:type {name: 'normal'})
    WITH w 
    MATCH (w)-[r:alleviation_suggestions|GoodExample|BadExample]->(n)
    RETURN 
        w.name AS weakness_name,
        w.description AS description,
        TYPE(r) AS relation_type,
        n.name AS related_node_name,
        HEAD(labels(n)) AS node_label
    """

    with driver.session() as session:
        result = session.run(query)
        records = [dict(record) for record in result]  # 转换为字典列表

    driver.close()
    print(records)

    # 后续处理（替换原有 transform_response）
    transformed_data = transform_vulnerability_data(records)

    def save_to_json(data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"数据已成功保存到 {filename}")

    output_path = "./Output/normal_vul.json"
    save_to_json(transformed_data, output_path)
    plan = read_json_files("./Output/Verilog_Plan.json")
    plan['Suggestion'] = transformed_data
    save_to_json(plan, './Output/Verilog_PlanV1.json')

import colorama
from colorama import Fore, Style
import copy
colorama.init(autoreset=True)

def FSKG_P():
    # 初始化配置
    config_list = [
        {
            "model": "gpt-4o",
            'api_key': '',
            'base_url': '',
            "temperature": 0.1,
        }
    ]

    # 读取原始数据并创建可修改副本
    original_data = read_json_files('./Output/vul.json')
    processed_data = copy.deepcopy(original_data)
    STG = read_json_files('./Output/FSMCR.json')

    # 处理Potential漏洞
    if 'Potential' in processed_data:
        cwe_ids = list(processed_data['Potential'].keys())
        for cwe_id in cwe_ids:
            print(Fore.CYAN + f"\n{'=' * 40}\n开始处理 {cwe_id}\n{'=' * 40}")

            states = processed_data['Potential'][cwe_id]
            state_list = [states]
            valid_states = []

            for state_str in state_list:
                try:
                    # 解析状态信息
                    #condition = re.search(r"condition':\s*['\"](.+?)['\"]", state_str).group(1)

                    #print(Fore.YELLOW + f"\n分析状态 {state_id}：")
                    print(Fore.YELLOW + f"STG：{STG}")

                    # 执行漏洞判断
                    result = graph_retrieval_tool_cwe(cwe_id, STG)

                    # 可视化显示知识图谱信息
                    print(Fore.MAGENTA + "\n[知识图谱信息]")
                    for confirm in result['confirm_contents']:
                        print(f"• {confirm}")

                    # 显示判断结果
                    print(Fore.GREEN + "\n[推理过程]")
                    print(result['judgment'].content)

                    # 根据结果处理数据
                    if "YES" in result['judgment'].content:
                        valid_states.append(state_str)
                        print(Fore.RED + f"判定结果： 存在漏洞（保留）")
                    elif "NO" in result['judgment'].content:
                        print(Fore.GREEN + f"判定结果：不存在漏洞（移除）")

                except Exception as e:
                    print(Fore.RED + f"处理状态时出错：{e}")
                    continue

            # 更新处理后的状态数据
            # if valid_states:
            #     processed_data['Potential'][cwe_id] = '  - ' + '  - '.join(valid_states)
            # else:
            #     del processed_data['Potential'][cwe_id]
            #     print(Fore.RED + f"\n移除空漏洞条目：{cwe_id}")

    # 保存清理后的数据
    with open('./Output/vul_processed.json', 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    print(Fore.CYAN + "\n数据处理完成，结果已保存到 vul_processed.json")

def FSKG():
    config_list = [
        {
            "model": "gpt-4o",
            'api_key': '',
            'base_url': '',
            "temperature": 0.1,
        }
    ]
    llm_config = {"config_list": config_list, "cache_seed": 42}


    original_data = read_json_files('./Output/vul.json')
    processed_data = copy.deepcopy(original_data)

    assistant = autogen.ConversableAgent(
        name="Assistant",
        system_message="You are a top-tier Verilog expert with experience in retrieving required information for the following task using graph_retrieval_tool. "
                       "You can help with Retrieving required information "
                       "Return 'TERMINATE' when the task is done.",
        llm_config=llm_config,
    )

    user_proxy = autogen.ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    assistant.register_for_llm(name="graph_retrieval_tool",
                               description="input task_description, return information for task")(graph_retrieval_tool)

    user_proxy.register_for_execution(name="graph_retrieval_tool")(graph_retrieval_tool)

    structure_keys = list(processed_data.get('Structure', {}).keys())
    structure_results = []
    for key in structure_keys:
        result = graph_retrieval_tool(key)
        structure_results.append(result)

    potential_keys = list(processed_data.get('Potential', {}).keys())
    potential_results = []
    for key in potential_keys:
        result = graph_retrieval_tool(key)
        potential_results.append(result)

    # 保存结构化数据
    user_proxy.initiate_chat(assistant, message=f"Structure results: {structure_results}\nTERMINATE")
    if potential_results:
        user_proxy.initiate_chat(assistant, message=f"Potential results: {potential_results}\nTERMINATE")
    else:
        user_proxy.initiate_chat(assistant, message="No valid Potential results found.\nTERMINATE")

    all_results = {
        "Structure": structure_results,
        "Potential": potential_results
    }
    # 整合逻辑
    for category in ['Structure', 'Potential']:
        # 遍历data1中的每个条目
        for item in all_results.get(category, []):
            # 获取当前条目的描述
            desc = item['weakness_name']

            # 从data2对应类别中查找匹配的位置信息
            position_info = processed_data.get(category, {}).get(desc, None)

            # 添加position字段
            if position_info:
                if isinstance(position_info, list):
                    item['position'] = ", ".join([str(p).strip() for p in position_info])
                else:
                    item['position'] = str(position_info).strip()
            else:
                item['position'] = "No position information available"

    save_json_file(all_results)
    Verilog_Plan = read_json_files('./Output/Verilog_PlanV1.json')

    # 先单独保存 Structure 部分
    structure_only_path = './Output/Structure_Suggestion.json'
    os.makedirs(os.path.dirname(structure_only_path), exist_ok=True)

    structure_output = {
        "message": "The following Verilog code has the issues listed below. Please modify the code according to the suggestions.",
        "suggestions": all_results['Structure']
    }

    with open(structure_only_path, 'w', encoding='utf-8') as f:
        json.dump(structure_output, f, ensure_ascii=False, indent=4)

    # 原有逻辑：Potential append 到 Suggestion
    for i in range(len(all_results['Potential'])):
        Verilog_Plan["Suggestion"].append(all_results["Potential"][i])

    # 原有逻辑：保存最终 V2
    file_path = './Output/Verilog_PlanV2.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(Verilog_Plan, f, ensure_ascii=False, indent=4)


import csv
#gpt-4o
#claude-3-5-haiku-20241022
#deepseek-r1
#qwen3-coder-plus
#gpt-5
def Code_Agent(args):
    model = "gpt-4o"

    def csv_to_text(csv_path):
        text_lines = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # 用制表符分隔列，保持表格结构
                text_lines.append("\t".join(row))
        return "\n".join(text_lines)

    CSV_PATH = ""
    #CSV_PATH = "D://pycharm//autogen-0.2.36//V2.0//Output//vul.json"
    csv_text = csv_to_text(CSV_PATH)

    if model == "RTLCoder":
        from ctransformers import AutoModelForCausalLM
        Agent_state = 'Code'
        TCRG = read_json_files('./Output/Verilog_Plan.json')
        Verilog_Engineer_message = get_prompts(Agent_state, 'Verilog_Engineer',
                                      Agents_config=Agents_config, module_des=TCRG)
        model_path = "E://data//hub//models--ishorn5--RTLCoder-v1.1-gguf-4bit//snapshots//fc60b2440a782487654f573bbaed2c8a39647e8e//ggml-model-q4_0.gguf"
        # Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
        llm = AutoModelForCausalLM.from_pretrained(model_path, model_type="mistral", gpu_layers=0, max_new_tokens=2000,
                                                   context_length=6048, temperature=0.2, top_p=0.95)
        print(llm(Verilog_Engineer_message))

    else:
        config_list = [
            {
                "model": model,
                'api_key': '',
                'base_url': '',
                "temperature": 0.2,
            }
        ]
        llm_config = {"config_list": config_list, "cache_seed": 42}
        # Agent_state LLM role's prompts
        Agent_state = 'Code'
        TCRG = read_json_files('./Output/Verilog_Plan.json')
        #TCRG["Suggestion"] = csv_text
        print("star!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(TCRG)

        Verilog_Engineer_message = get_prompts(Agent_state, 'Verilog_Engineer', Agents_config=Agents_config, module_des=TCRG)
        print(Verilog_Engineer_message)
        Verilog_Verify_Assistant_message = get_prompts(Agent_state, 'Verilog_Verify_Assistant',
                                               Agents_config=Agents_config, module_des=args.Modlue_Des)



        Verilog_Engineer = autogen.ConversableAgent(
            name="Verilog_Engineer",
            system_message=Verilog_Engineer_message,
            llm_config=llm_config,
        )

        user_proxy = autogen.ConversableAgent(
            name="User",
            llm_config=False,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            human_input_mode="NEVER",
        )
        # LLM Role: Verilog_Engineer
        #tool
        Verilog_Engineer_message = get_prompts(Agent_state, 'Verilog_Engineer',
                                      Agents_config=Agents_config, module_des=args.Modlue_Des)
        # Register the tool signature with the assistant agent.
        Verilog_Engineer.register_for_llm(name="save_verilog_files", description="save_verilog_files")(save_verilog_files)
        user_proxy.register_for_execution(name="save_verilog_files")(save_verilog_files)
        chat_result = user_proxy.initiate_chat(Verilog_Engineer, message=Verilog_Engineer_message)

#gpt-4o
#claude-3-5-haiku-20241022
#deepseek-r1
#qwen3-coder-plus
#gpt-5
import os, glob, csv, json
from openai import OpenAI

def Code_Agent_Stage2(args):
    """
    第二次代码生成（简化版）
    - 读取 Stage1 Verilog（文件 or 目录 *.v）
    - 读取安全知识（csv/json/文本）
    - 合并进 TCRG，调用 LLM 二次生成并 save
    """
    stage1_path = getattr(args, "stage1_verilog_path", "./Output/Verilog.v")
    knowledge_path = getattr(args, "security_knowledge_path", "./Output/Structure_Suggestion.json")

    # ---------- 1) 两个通用读取函数 ----------
    def read_any(path: str) -> str:
        """读 .json / .csv / 其它文本"""
        ext = os.path.splitext(path)[-1].lower()
        if ext == ".json":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return json.dumps(json.load(f), ensure_ascii=False, indent=2)
        if ext == ".csv":
            lines = []
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for row in csv.reader(f):
                    lines.append("\t".join(row))
            return "\n".join(lines)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def read_verilog(path: str) -> str:
        """读单个 .v 或目录下所有 .v 拼起来"""
        if os.path.isdir(path):
            parts = []
            for fp in sorted(glob.glob(os.path.join(path, "*.v"))):
                parts.append(f"// ===== FILE: {os.path.basename(fp)} =====\n{read_any(fp)}\n")
            return "\n".join(parts).strip()
        return read_any(path)

    prev_verilog = read_verilog(stage1_path)
    security_knowledge = read_any(knowledge_path)

    # ---------- 2) 读取 plan + 塞上下文 ----------
    query = security_knowledge + prev_verilog

    client = OpenAI(
        base_url='',
        api_key='',
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{query}",
            }
        ],
        temperature=0.2,
        model="deepseek-r1",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

#gpt-4o
#claude-3-5-haiku-20241022
#deepseek-r1
#qwen3-coder-plus
#gpt-5

def Debug_Agent():
    config_list = [
        {
            "model": "gpt-4o",
            'api_key': '',
            'base_url': 'https://api.v3.cm/v1',
            # "temperature": 0.0,
        }
    ]
    llm_config = {"config_list": config_list, "cache_seed": 42}
    assistant = autogen.ConversableAgent(
        name="Verilog Engineer",
        system_message="You are a Verilog RTL designer that verify the functionality using external tool 'verilog_checker'.",
        llm_config=llm_config,
    )

    user_proxy = autogen.ConversableAgent(
        name="UserProxy",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    assistant.register_for_llm(name="verilog_checker",
                               description="Input the path of the verilog code and the path of the testbench file in sequence to check the functional correctness of the verilog code.")(
        verilog_checker)
    user_proxy.register_for_execution(name="verilog_checker")(verilog_checker)

    message = (
        "Please using external tool 'verilog_checker' to check the functional correctness of the verilog code in the verilog code path of: D://pycharm//autogen-0.2.36//V2.0//Input//ast_demo.v, and the verilog testbench file path : D://pycharm//autogen-0.2.36//V2.0//Input//ast_demo_tb.v \n"
        "After check the functional correctness of verilog, reply TERMINATE to end.")
    chat_result = user_proxy.initiate_chat(assistant, message=message)

def main():
    #create_security()
    #High_level_Plan_gent(args)
    #CSTEE_Agent(args)
   # FSMCR()
    #FSKG_N()
    #SG_Check()
    #FSKG_P()
    #FSKG()
    #Code_Agent(args)
    Code_Agent_Stage2(args)
    #dynamics_security_prompt()
    #Debug_Agent()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Agent')
    parser.add_argument('--Modlue_Des', type=dict, default={
        'QuestionDescription': {
            """"
"I would like you to implement a module named TopModule with the following interface. "
                        "All input and output ports are one bit unless otherwise specified."
                        "- input  clk"
                        "- input  areset"
                        "- input  in"
                        " - output out"
                        "The module should implement a Moore machine with the diagram described below:"
                        "S010 (0) --0-->  S010\n"
                        "S010 (0) --1-->  S010\n"
                        "S000 (0) --0-->  S001\n"
                        "S000 (0) --1-->  S001\n"
                        "S001 (0) --0-->  S011\n"
                        "S001 (0) --1-->  S101\n"
                        "S011 (0) --0-->  S011\n"
                        "S011 (0) --1-->  S011\n"
                        "S101 (0) --0-->  S110\n"
                        "S101 (0) --1-->  S110\n"
                        "S110 (0) --0-->  S111\n"
                        "S110 (0) --1-->  S111\n"
                        "S111 (1) --0-->  S101\n"
                        "S111 (1) --1-->  S101\n"
                        "S100 (0) --0-->  S101\n"
                        "S100 (0) --1-->  S101\n"
                        "It should asynchronously reset into state S000 if reset if high."

"""



    }}, help='user input')
    parser.add_argument('--TCRG', type=dict, default={'TCRG': {""}}, help='user input')
    parser.add_argument('--model-name', type=str, help='model name')
    parser.add_argument('--base-url', type=str, help='base url')
    parser.add_argument('--verbose', default=True, action='store_true', help='verbose')
    args = parser.parse_args()

    main()