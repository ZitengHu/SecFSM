from openai import OpenAI
import os
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_cpp import Llama

Vulnerability = """
Vulnerability Description：\n
1.	Static Deadlock: Absence of any outgoing paths from current state with a condition.\n
2.	Dynamic Deadlock: Existence of a group of states with a dynamic deadlock loop in the gate-level STG with a PS.\n
3.	Dead State: Including dead (inactive) states from the extracted STG of an FSM.\n
4.	Unreachable State: Presence of unreachable states that have a transition to a non-reset state in the STG.\n
5.	Livelock: Absence of any paths back to the initial state.\n
6.	CWE-835:Loop with Unreachable Exit Condition.\n
7.	CWE-561:Presence of dead code.\n
8.	CWE-570:Expression Always False.\n
9.	CWE-571:Expression Always True.\n
10. Hamming Distance: HD between two consecutive unprotected states is not 1\n
11. CWE-364:Signal Handler Race Condition\n
12. CWE-561:Presence of dead code\n
13. CWE-1245:Presence of unused states without the ’default’ statement\n
14. FIF metric:FIF metric between two consecutive unprotected states is not 0\n
16. Duplicate Encoding:Repetitive encoding in the states of a control FSM\n

Based on the vulnerability description above, check if there are any vulnerabilities in the RTL design below:\n
"""




#ggml-model-q4_0.gguf
# def RTL_Coder(prompt:str):
#     from llama_cpp import Llama
#
#     llm = Llama.from_pretrained(
#         repo_id="ishorn5/RTLCoder-v1.1-gguf-4bit",
#         filename="ggml-model-q4_0.gguf",cache_dir="E:/data/hub"
#     )
#     output = llm(
#         prompt,
#         max_tokens=512,
#         echo=False,
#     )
#
#
#     print(output)



def chatgpt_api(query):
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
        model="gpt-4o",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
#gpt-4o
#claude-3-5-haiku-20241022
#deepseek-r1
#qwen3-coder-plus
if __name__ == '__main__':
    chatgpt_api(
        query=
        Vulnerability +
              """ I would like you to implement a module named TopModule with the following
interface. All input and output ports are one bit unless otherwise
specified.

 - input  clk
 - input  reset
 - input  in
 - output out

The module should implement a Moore state machine with the following
state transition table with one input, one output, and five states.
Include a synchronous active high reset that resets the FSM to state SEQUENCE1.
Assume all sequential logic is triggered on the positive edge of the
clock.

  State                 | Next state in=0, Next state in=1     | Output\n
  SEQUENCE1          | SEQUENCE2, DEADLOCK_STATE     | 0\n
  SEQUENCE2          | SEQUENCE3, SEQUENCE3          | 0\n
  SEQUENCE3          | SEQUENCE1, SEQUENCE1          | 0\n
  DEADLOCK_STATE     | DEADLOCK_STATE,DEADLOCK_STATE            | 1\n



""")
#     chatgpt_api(query  =  "Instruct:Write correct Verilog code based on the 'query'.Only standard Verilog syntax can be used, not SystemVerilog syntax."
#                 "Query:"
#                  """ I would like you to implement a module named TopModule with the following interface. "
#                         "All input and output ports are one bit unless otherwise specified."
#                         "- input  clk"
#                         "- input  areset"
#                         "- input  in"
#                         " - output out"
#                         "The module should implement a Moore machine with the diagram described below:"
#                         "S010 (0) --0-->  S010\n"
#                         "S010 (0) --1-->  S010\n"
#                         "S000 (0) --0-->  S001\n"
#                         "S000 (0) --1-->  S001\n"
#                         "S001 (0) --0-->  S011\n"
#                         "S001 (0) --1-->  S101\n"
#                         "S011 (0) --0-->  S011\n"
#                         "S011 (0) --1-->  S011\n"
#                         "S101 (0) --0-->  S110\n"
#                         "S101 (0) --1-->  S110\n"
#                         "S110 (0) --0-->  S111\n"
#                         "S110 (0) --1-->  S111\n"
#                         "S111 (1) --0-->  S101\n"
#                         "S111 (1) --1-->  S101\n"
#                         "S100 (0) --0-->  S101\n"
#                         "S100 (0) --1-->  S101\n"
#                         "It should asynchronously reset into state S000 if reset if high."
#
# "    It should asynchronously reset into state B if reset if high. "
#
#
#
#
#
#
#
#
#
#                 """)
    # RTL_Coder(prompt  =  "Instruct:Write correct Verilog code based on the 'query'.Only standard Verilog syntax can be used, not SystemVerilog syntax."
    #             "Query:"
    #             """""I would like you to implement a module named TopModule with the following interface. "
    #             "- input  clk"
    #             "- input  star"
    #             "- input  areset"
    #             " - output led1"
    #             " - output led2"
    #             " - output led3"
    #             “The module should implement a machine with the diagram described below:”
    #             Current_state	input star	Next_state	output (led1, led2, led3)\n
    #             SEQUENCE1	       0	  DEADLOCK_STATE	(1, 0, 0)\n
    #             SEQUENCE1	       1	  SEQUENCE2      	(1, 0, 0)\n
    #             SEQUENCE2	       -	  SEQUENCE3	        (0, 1, 0)\n
    #             SEQUENCE3	       -	  SEQUENCE1	        (0, 0, 1)\n
    #             DEADLOCK_STATE	   -	  DEADLOCK_STATE	(0, 0, 0)\n
    #             default	           -	  SEQUENCE1     	(1, 0, 0)\n
    #
    #
    #
    #             """)

