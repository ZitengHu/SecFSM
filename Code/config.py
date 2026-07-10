from dis import Instruction

Agents_config = {
                'state':{
                    'Plan':{
                            'Planner': {
                                        'Task':{'task':{"You are a Verilog RTL designer that can break down complicated implementation into subtasks implementation plans."}
                                        },
                                        'Verilog_Example':{'Verilog_Example':{
                                                    "[Example Begin1]"
                                                    "[Target Problem]"
                                                    "### Problem :"
                                                    "Implement the following Moore state machine with 3 input (clk, areset, in) and 1 output (out) ."
                                                    "The module should implement a Moore state machine with the following state transition table with one input, one output, and four states. "
                                                    "The following table is the state transition table of the Moore's state machine: "
                                                    "the first column is the current state, the second column is the output, and the third column is the state transition based on the input.After '-->' in the third column is the name of the next_state."
                                                    "table:"
                                                    "row0:state  | output          | --input--> next_state  \n"
                                                    "row1:A      | (output=0)      | --in=0--> A            \n"
                                                    "row2:A      | (output=0)      | --in=1--> B            \n"
                                                    "row3:B      | (output=0)      | --in=0--> C            \n"
                                                    "row4:B      | (output=0)      | --in=1--> B            \n"
                                                    "row5:C      | (output=0)      | --in=0--> A            \n"
                                                    "row6:C      | (output=0)      | --in=1--> D            \n"
                                                    "row7:D      | (output=1)      | --in=0--> C            \n"
                                                    "row8:D      | (output=1)      | --in=1--> B            \n"
                                                    "answer:"
                                                    "```json "
                                                    '{'
                                                    '      "Suggestion": ['
                                                    '      ],'
                                                    '      "subtasks": ['
                                                    '        {'
                                                    '          "id": "1",'
                                                    '          "type": "Module Interface",'
                                                    '          "content": "",'
                                                    '          "Security": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "2",'
                                                    '          "type": "State Encoding",'
                                                    '          "content": "Binary encoding for 4 states: A(00), B(01), C(10), D(11)",'
                                                    '          "Security": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "3",'
                                                    '          "type": "State Register",'
                                                    '          "content": "Sequential logic for state update: async reset to A, else update to next_state"'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "4",'
                                                    '          "type": "State Transition",'
                                                    '          "content": "Combinational logic for state transitions with full case coverage",'
                                                    '          "Security": "",'
                                                    '          "dynamic_subtasks": ['
                                                    '            {'
                                                    '              "id": "4.1",'
                                                    '              "State": "A",'
                                                    '              "Evidence": "A --in=0--> A\n A--in=1--> B   "'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.2",'
                                                    '              "State": "B",'
                                                    '              "Evidence": "B --in=0--> C\n B --in=1--> B"'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.3",'
                                                    '              "State": "C",'
                                                    '              "Evidence": "C --in=0--> A\nC --in=1--> D"'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.4",'
                                                    '              "type": "D",'
                                                    '              "Evidence": "D --in=0--> C\n D--in=1--> B"'
                                                    '            }'
                                                    '          ]'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "5",'
                                                    '          "type": "Output Logic",'
                                                    '          "content": "Combinational output: 1 when in state D, 0 otherwise",'
                                                    '          "Security": "",'
                                                    '          "dynamic_subtasks": ['
                                                    '            {'
                                                    '              "id": "5.1",'
                                                    '              "type": "A",'
                                                    '              "Evidence": "Output = 0"'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "5.2",'
                                                    '              "type": "B",'
                                                    '              "Evidence": "Output = 0"'
                                                    '            }'
                                                    '            {'
                                                    '              "id": "5.3",'
                                                    '              "type": "C",'
                                                    '              "Evidence": "Output = 0"'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "5.4",'
                                                    '              "type": "D",'
                                                    '              "Evidence": "Output = 1"'
                                                    '            }'
                                                    '          ]'
                                                    '        }'
                                                    '      ]'
                                                    '    }'
                                                    "[Example End1]"
                                                    "[Example Begin2]"
                                                    "[Target Problem]"
                                                    "### Problem :"
                                                    ""
                                                    "The module should implement a Moore state machine with the following state transition table with three input (clk, reset, w), one output(z), and five states. "
                                                    "The following table is the state transition table of the Moore's state machine: "
                                                    "the first column is the current state, the second column is the output, and the third column is the state transition based on the input.After '-->' in the third column is the name of the next_state."
                                                    "table:"
                                                    "row0:state  | output          | --input--> next_state  \n"
                                                    "row1:A      | (output=0)      | --in=0--> A            \n"
                                                    "row2:A      | (output=0)      | --in=1--> B            \n"
                                                    "row3:B      | (output=0)      | --in=0--> D            \n"
                                                    "row4:B      | (output=0)      | --in=1--> C            \n"
                                                    "row5:C      | (output=0)      | --in=0--> D            \n"
                                                    "row6:C      | (output=0)      | --in=1--> E            \n"
                                                    "row7:D      | (output=0)      | --in=0--> A            \n"
                                                    "row8:D      | (output=0)      | --in=1--> F            \n"
                                                    "row9:E      | (output=1)      | --in=0--> D            \n"
                                                    "row10:E     | (output=1)      | --in=1--> E            \n"
                                                    "row11:F     | (output=1)      | --in=0--> D            \n"
                                                    "row12:F     | (output=1)      | --in=1--> C            \n"
                                                    "answer:"
                                                    "```json "
                                                    '{'
                                                    '      "Suggestion": ['
                                                    '      ],'
                                                    '      "subtasks": ['
                                                    '        {'
                                                    '          "id": "1",'
                                                    '          "type": "Module Interface",'
                                                    '          "content": "",'
                                                    '          "Security": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "2",'
                                                    '          "type": "State Encoding",'
                                                    '          "content": "Binary encoding for 6 states: A, B, C, D, E, F",'
                                                    '          "Security": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "3",'
                                                    '          "type": "State Register",'
                                                    '          "content": "Sequential logic for state update: async reset to A, else update to next_state",'
                                                    '          "Evidence": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "4",'
                                                    '          "type": "State Transition",'
                                                    '          "content": "Combinational logic for state transitions with full case coverage",'
                                                    '          "Security": "",'
                                                    '          "dynamic_subtasks": ['
                                                    '            {'
                                                    '              "id": "4.1",'
                                                    '              "State": "A",'
                                                    '              "Evidence": "A --in=0--> A\n A -in=1--> B",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.2",'
                                                    '              "State": "B",'
                                                    '              "Evidence": "B  --in=0--> D\n B -in=1--> C ",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.3",'
                                                    '              "State": "C",'
                                                    '              "Evidence": "C  --in=0--> D\n C --in=1--> E",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.4",'
                                                    '              "type": "D",'
                                                    '              "Evidence": "D --in=0--> A\n D -in=1--> F ",'
                                                    '            },'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.5",'
                                                    '              "State": "E",'
                                                    '              "Evidence": "E --in=0--> D\n E --in=1--> E",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.6",'
                                                    '              "type": "F",'
                                                    '              "Evidence": "F --in=0--> D \n F --in=1--> C",'
                                                    '            }'
                                                    '          ]'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "5",'
                                                    '          "type": "Output Logic",'
                                                    '          "content": "Combinational output: 1 when in state E and F, 0 otherwise",'
                                                    '          "Security": "",'
                                                    '          "dynamic_subtasks": ['
                                                    '            {'
                                                    '              "id": "5.1",'
                                                    '              "type": "A",'
                                                    '              "Evidence": "output=0",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "5.2",'
                                                    '              "type": "B",'
                                                    '              "Evidence": "output=0",'
                                                    '            }'
                                                    '            {'
                                                    '              "id": "5.3",'
                                                    '              "type": "C",'
                                                    '              "Evidence": "output=0",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "5.4",'
                                                    '              "type": "D",'
                                                    '              "Evidence": "output=0",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "5.5",'
                                                    '              "type": "E",'
                                                    '              "Evidence": "output=1",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "5.6",'
                                                    '              "type": "F",'
                                                    '              "Evidence": "output=1",'
                                                    '            }'
                                                    '          ]'
                                                    '        }'
                                                    '      ]'
                                                    '    }'
                                                    "```"
                                                    "[Example End2]"}
                                        },
                                        'Instruction': {
                                            'Instruction':
                                                    "Let's think step by step. "
                                                    "1.Based on the Problem description, set up a sequential implementation plans. "
                                                    "2.Each subtask should focus on implement only one signal at a time. Extract the corresponding source contexts in the [Target Problem] section of each subtask into the 'source' field. "
                                                    "3.Create subtasks based on the form of constructing subtasks in the [Example]."
                                                    "The task id number indicates the sequential orders. Return the subtasks in json format as below. "
                                                    '{'
                                                    '      "Suggestion": ['
                                                    '      ],'
                                                    '      "subtasks": ['
                                                    '        {'
                                                    '          "id": "1",'
                                                    '          "type": "Module Interface",'
                                                    '          "content": "",'
                                                    '          "Security": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "2",'
                                                    '          "type": "State Encoding",'
                                                    '          "content": "",'
                                                    '          "Security": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "3",'
                                                    '          "type": "State Register",'
                                                    '          "content": "",'
                                                    '          "Evidence": ""'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "4",'
                                                    '          "type": "State Transition",'
                                                    '          "content": "Combinational logic for state transitions with full case coverage",'
                                                    '          "Security": "",'
                                                    '          "dynamic_subtasks": ['
                                                    '            {'
                                                    '              "id": "4.1",'
                                                    '              "State": "A",'
                                                    '              "Evidence": "",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "4.2",'
                                                    '              "State": "B",'
                                                    '              "Evidence": "",'
                                                    '            },'
                                                    '          ...'
                                                    '        },'
                                                    '        {'
                                                    '          "id": "5",'
                                                    '          "type": "Output Logic",'
                                                    '          "content": "",'
                                                    '          "Security": "",'
                                                    '          "dynamic_subtasks": ['
                                                    '            {'
                                                    '              "id": "5.1",'
                                                    '              "type": "A",'
                                                    '              "Evidence": "",'
                                                    '            },'
                                                    '            {'
                                                    '              "id": "5.2",'
                                                    '              "type": "B",'
                                                    '              "Evidence": "",'
                                                    '            }'
                                                    '           ...'
                                                    '          ]'
                                                    '        }'
                                                    '      ]'
                                                    '    }'
                                            },
                                        'rule': {
                                            'rule': "Make sure the task plans satisfy the following rules! Do not make the plans that violate the following rules!!!"
                                                    "- Make a plan to define the module with its input and output first."
                                                    "- Functionality must be checked at the end."
                                                    "- Do not plan the implementation of logic or signal from the input ports."
                                                    "- There is test bench to test the functional correctness. Do not plan generating testbench to test the generated verilog code."
                                                    "- Don't make a plan only with clock or control signals. The clock or control signals should be planned with register or wire signal."
                                                    "- Don't make a plan on implementing the signal or next state logics which are not related to the module outputs."
                                                    "- For module related to Finite State Machine (FSM), try to determine the number of states first and then make the plan to implement FSM."
                                                    "- For module related to Finite State Machine or Moore State Machine, if the state or current_state is an input port signal of the module,You must Do Not implement the state flip-flops for state transition in TopModule."
                                            },

                                        },
                            'Plan_Verify_Assistant': {
                                                      'Task': {'Task': 'checks the consistency between the sub-tasks and the module description, '
                                                                       'Please check if tasks have been designed for each state.'},
                                                      'rule': {'rule': "1.If it does not cover every state, propose modification suggestions. "
                                                                       "2.If it is covered, no suggestions will be provided. Then save the plan that planner generated to the following path: D://pycharm//autogen-0.2.36//V2.0//Output//Verilog_Plan.json. "
                                                                       "3.Then reply TERMINATE to end."},
                                                      },
                    },
                'CSTEE':{
                    'Verilog_Engineer': {
                        'Task': {'task': {"You are a Verilog RTL designer that identify the state, state_transitions , state input and state output .You need to study the following three examples carefully and then follow 'Instruction' "}},
                        'Verilog_Example': {'Example': {
                                                              "[Example begin1]"
                                                              "  I would like you to implement a module named TopModule with the following"
                                                              "  interface. All input and output ports are one bit unless otherwise"
                                                              "  specified."
                                                              "   - input  clk"
                                                              "   - input  a "
                                                              "   - input  b "
                                                              "   - input  areset"
                                                              "   - input  in"
                                                              "   - output out"
                                                                
                                                              "  The module should implement a Moore state machine with the following"
                                                              "  state transition table with one input, one output, and four states."
                                                              "  Implement this state machine. Include a positive edge triggered"
                                                              "  asynchronous reset that resets the FSM to state A. Assume all sequential"
                                                              "  logic is triggered on the positive edge of the clock.Protection state B: The B state can only be entered from the A state.\n"
                                                              "    state | next state in=0, next state in=1 | output\n"
                                                              "    A     | A, B                             | a\n"
                                                              "    B     | C, B                             | a+b\n"
                                                              "    C     | A, D                             | a\n"
                                                              "    D     | C, B                             | b\n"
                                                               "answer:"
                                                               '{ '
                                                               '         "init_state":['
                                                               '                   {"name": "A", "output":"out=a-b", "condition":"a-b", protected":NULL}'
                                                               '                  ]'
                                                               '         "states":['
                                                               '                    {"name": "A", "output":"out=a", "condition":"NULL", protected":"NULL"},'
                                                               '                    {"name": "B", "output":"out=a+b", "condition":"a+b", protected":The B state can only be entered from the A state.},'
                                                               '                    {"name": "C", "output":"out=a", "condition":"NULL", protected":"NULL"}'
                                                               '                    {"name": "D", "output":"out=b", "condition":"NULL", protected":"NULL"}'
                                                               '                  ],'
                                                               '         "transitions": ['
                                                               '                     {"from": "A", "to": "A", "condition":in=0},'
                                                               '                     {"from": "A", "to": "B", "condition":in=1},'
                                                               '                     {"from": "B", "to": "C", "condition":in=0},'
                                                               '                     {"from": "B", "to": "B", "condition":in=1},'
                                                               '                     {"from": "C", "to": "A", "condition":in=0},'
                                                               '                     {"from": "C", "to": "D", "condition":in=1},'
                                                               '                     {"from": "D", "to": "C", "condition":in=0},'
                                                               '                     {"from": "D", "to": "B", "condition":in=1},'
                                                               '                     ],'
                                                                        '} '
                                                                ''
                                                              "[Example end1]"
                                                              "[Example Begin2]"
                                                               "[Target Problem]"
                                                              " ### Problem :"
                                                               "Implement the following Moore state machine with 3 input (clk, areset, in) and 1 output (out) ."
                                                               "The module should implement a Moore state machine with the following state transition table with one input, one output, and four states. "
                                                                "State A is the initial state. Protection state B: The B state can only be entered from the A state."
                                                               "table:"
                                                               "row0:state  | output          | --input--> next_state  \n"
                                                               "row1:A      | (out=0)      | --1=1--> A            \n"
                                                               "row2:A      | (out=0)      | --in=1--> B            \n"
                                                               "row3:B      | (out=0)      | --in=0--> C            \n"
                                                               "row4:B      | (out=0)      | --in=1--> B            \n"
                                                               "row5:C      | (out=0)      | --in=0--> A            \n"
                                                               "row6:C      | (out=0)      | --1=0--> D            \n"
                                                               "row7:D      | (out=1)      | --in=0--> C            \n"
                                                               "row8:D      | (out=1)      | --in=1--> B            \n"
                                                               "answer:"
                                                               '{ '
                                                               '         "init_state":['
                                                               '                   {{"name": "A", "output": "out=0", "condition":"NULL", protected":"NULL"}}'
                                                               '                  ],'
                                                               '         "states":['
                                                               '                    {"name": "A", "output": "out=0", "condition":"NULL", protected":"NULL"},'
                                                               '                    {"name": "B", "output": "out=1", "condition":"NULL", protected":"The B state can only be entered from the A state."},'
                                                               '                    {"name": "C", "output": "out=0", "condition":"NULL", protected":"NULL"}'
                                                               '                    {"name": "D", "output": "out=0", "condition":"NULL", protected":"NULL"}'
                                                               '                  ],'
                                                               '         "transitions": ['
                                                               '                     {"from": "A", "to": "A", "condition":1=1},'
                                                               '                     {"from": "A", "to": "B", "condition":in=1},'
                                                               '                     {"from": "B", "to": "C", "condition":in=0},'
                                                               '                     {"from": "B", "to": "B", "condition":"in=1},'
                                                               '                     {"from": "C", "to": "A", "condition":in=0},'
                                                               '                     {"from": "C", "to": "D", "condition":1=0},'
                                                               '                     {"from": "D", "to": "C", "condition":in=0},'
                                                               '                     {"from": "D", "to": "B", "condition":in=1},'
                                                               '                     ],'
                                                                        '} '
                                                                ''
                                                               "[Example end2]"
                                                               "[Example Begin3]"
                                                               "[Target Problem]"
                                                               "### Problem :"
                                                               ""
                                                               "The module should implement a Moore state machine with the following state transition table with three input (clk,a,b reset, w), one output(z), and five states. "
                                                                "State C is the initial state"
                                                               "row0:state  | output          | --input--> next_state  \n"
                                                               "row1:A      | (z=a+b)      | --in=0--> A            \n"
                                                               "row2:A      | (z=a+b)      | --in=1--> B            \n"
                                                               "row3:B      | (z=a-b)      | --in=0--> D            \n"
                                                               "row4:B      | (z=a-b)      | --in=1--> C            \n"
                                                               "row5:C      | (z=a)      | --true--> D            \n"
                                                               "row6:C      | (z=a)      | --in=1--> E            \n"
                                                               "row7:D      | (z=a)      | --in=0--> A            \n"
                                                               "row8:D      | (z=a)      | --in=1--> F            \n"
                                                               "row9:E      | (z=b)      | --in=0--> D            \n"
                                                               "row10:E     | (z=b)      | --in=1--> E            \n"
                                                               "row11:F     | (z=b)      | --in=0--> D            \n"
                                                               "row12:F     | (z=b)      | --in=1--> C            \n"
                                                               "answer:"
                                                               '{ '
                                                               '         "init_state":['
                                                               '                   {"name": "C", "output":"z=0", "condition":NULL, protected":NULL}'
                                                               '                  ]'
                                                               '         "states":['
                                                               '                    {"name": "A", "output":"z=a+b", "condition""a+b", protected":"NULL"},'
                                                               '                    {"name": "B", "output":"z=a-b", "condition":"a-b" protected":"NULL"},'
                                                               '                    {"name": "C", "output":"z=a", "condition":"NULL", protected":"NULL"}'
                                                               '                    {"name": "D", "output":"z=a", "condition":"NULL", protected":"NULL"}'
                                                               '                    {"name": "E", "output":"z=b", "condition":"NULL", protected":"NULL"}'
                                                               '                    {"name": "F", "output":"z=b", "condition":"NULL", protected":"NULL"}'
                                                               '                  ],'
                                                               '         "transitions": ['
                                                               '                     {"from": "A", "to": "A", "condition":in=0},'
                                                               '                     {"from": "A", "to": "B", "condition":in=1},'
                                                               '                     {"from": "B", "to": "D", "condition":in=0},'
                                                               '                     {"from": "B", "to": "C", "condition":in=1},'
                                                               '                     {"from": "C", "to": "D", "condition":true},'
                                                               '                     {"from": "C", "to": "E", "condition":in=1},'
                                                               '                     {"from": "E", "to": "D", "condition":in=0},'
                                                               '                     {"from": "E", "to": "E", "condition":in=1},'
                                                               '                     {"from": "F", "to": "D", "condition":in=0},'
                                                               '                     {"from": "F", "to": "C", "condition":in=1},'
                                                               '                     ],'
                                                                        '} '
                                                                ''
                                                               "[Example end3]"

                        }
                        },
                                'Instruction': {'Instruction':
                                            'Please extract state details, transition details, and output details from the "QuestionDescription" and format the output as per the specified JSON structure.'
                                            'Extract information only according to "QuestionDescription", do not Extract information form "Example1","Example2" and "Example3"'
                                            'In the "states" field, if more than one value is affecting the "output", place the value that affects the "output" in the "condition" field.'
                                            'For example, "output":"z=a+b", "condition""a+b". '
                                            'The return format must follow ```json and ``` format. '
                                            '{'
                                            '    "init_state":['
                                            '               {"name": "state", "output":out_inf, "condition":condition_inf, "protected":protected_inf}'
                                             '            ],'
                                            '   "states":['
                                            '               {"name": "state1", "output":out_inf, "condition":condition_inf, "protected":protected_inf},'
                                            '               {"name": "state2", "output":out_inf, "condition":"condition_inf", "protected":protected_inf},'
                                            '               ...'
                                            '            ]'
                                            '   "transitions": ['
                                                               '                     {"from": "state1", "to": "state2", "condition":condition_inf},'
                                                               '                     {"from": "state1", "to": "state1", "condition":condition_inf},'
                                            '                                         ...'
                                            '                  ]'
                                            '}'
                                             },
                                'rule': {
                                    'rule': '- Do not write verilog code.'
                                },
                                'last':{'last_prompt': 'Save the generated json file to the path: D://pycharm//autogen-0.2.36//V2.0//Output//FSMCR.json'
                                                       'After finished the task, reply TERMINATE to end.'}

                    },
                },
                'TCRG_state':{

                },
                'FSM_Desgin':{
                    'Verilog_Engineer': {
                        'Task': {'task': {"You are a top FSM Verilog expert with the ability to use 'graph_retrieval_tool' to retrieve information when a retrieval tool is needed. "
                                          "Return 'TERMINATE' when the task is done."}},
                        'FSMKnowledge':{'FSMKnowledge': {'1.If the number of states is less than or equal to 4, then the finite state machine belongs to a Small scale design.'
                                                         '2.If the number of states is greater than 4 and less than or equal to 24, then the finite state machine design belongs to a Mid scale design'
                                                         '3.If the number of states is greater than 24, then the finite state machine design belongs to a Large scale design.'}},
                        'Instruction': {'Instruction':
                                                'Let us think step by step.'
                                                '1.Determine the number of states of the finite state machine based on the question description. '
                                                '2.Based on the results of the previous step and FSMKnowledge, determine and output the size of the finite state machine in QuestionDescription.description:[design scale].For example, Small scale design, Mid scale design and Large scale design.'
                                                '3.Retrieve relevant information using "graph_retrieval_tool" based on the design scale.description:[design scale].For example, Small scale design, Mid scale design and Large scale design.'
                                                '4.Organize the retrieved content strictly in the following format.'
                                                ' {'
                                                '       "Type_of_Status_Code": "code type",'
                                                '       "Application_Scenario": "the code applicated the scenario",'
                                                '       "Examples":[examples1, examples2]'
                                                ' }'
                                                '5.Save the output json file to the following path:D://pycharm//autogen-0.2.36//Output//Verilog_State_Coding.json'
                                                'After organizing the required state encoding information, reply TERMINATE to end.'

                                },
                    },
                },
                'FSM_Security':{
                    'Verilog_Engineer': {
                        'Task': {'task': {"You are a top FSM Verilog expert with the ability to use 'graph_retrieval_tool' to retrieve information when a retrieval tool is needed. "
                                          "Return 'TERMINATE' when the task is done."}},
                        'FSMKnowledge':{'State Code': {''}},
                        'Instruction': {'Instruction':
                                                '1.Retrieve relevant security information ".Retrieve relevant security information and return full content. description:[State code]'
                                                '2.Organize the retrieved content strictly in the following format.'
                                                '{'
                                                'weakness:'
                                                '   {'
                                                '       "id": "1",\n'
                                                '       "weakness": "weakness name",\n'
                                                '       "description" : "weakness description",\n'
                                                '       "good example": "good weakness example",\n'
                                                '       "bad example": "bad weakness example",\n'
                                                '       "fidelityChecking":"FidelityChecking",\n'
                                                '   },'
                                                'weakness:'
                                                '   {'
                                                '       "id": "2",\n'
                                                '       "weakness": "weakness name",\n'
                                                '       "description" : "weakness description",\n'
                                                '       "good example": "good weakness example",\n'
                                                '       "bad example": "bad weakness example",\n'
                                                '       "fidelityChecking":"FidelityChecking",\n'
                                                '   },'
                                                '...'
                                                '}'
                                                '2.Save the output json file to the following path: D://pycharm//autogen-0.2.36//Output//Verilog_Security.json'
                                                '3.After save the json file, reply TERMINATE to end.'

                                },
                    },
                },
                'Code':{ 'Verilog_Engineer': {'Task': {'task': 'You are a Verilog RTL designer that only writes verilog code using correct Verilog syntax based on the [Subtask list] definition.' },
                                             'Instruction': {'Instruction':
                                                            'Let us think step by step.'
                                                            '1.Refer to the "Suggestions" field to avoid these security issues.Determine the form of the vulnerability based on the "description", "GoodExample", and "BadExample", and then write code based on "alleviation_suggestions"'
                                                            '2.Write Verilog code base on "Suggestions" and "subtasks".'
                                                            '3.Explain in the comments the section on safety recommendations.'
                                                            '4.After completing all code writing tasks, save the verilog code.'
                                                            },
                                             'rule': {'rule': 'Only output the generated Verilog code.'
                                                                      '- Be careful not to use SystemVerilog syntax when generating Verilog code.'
                                                                },
                                                     'last':{'last_prompt': 'The output strictly follows the following format:<verilog>{the target code}</verilog>'
                                                                            'Save the generated Verilog object code:{the target code} to the path: D://pycharm//autogen-0.2.36//V2.0//Output//verilog.v'
                                                                            'After finished the Verilog Code, reply TERMINATE to end.'}
                                                     },
                         'Verilog_Verify_Assistant': {'Task': {'task': 'Perform syntax checks on the generated code to the path: D://pycharm//autogen-0.2.36//V2.0//Output//verilog.v'
                                                                   
                                                                       ''},
                                                       'rule': {'rule': '-Do not provide any advice other than grammar advice.'},},

                },
                'Debug_state':{
                                'Verilog_Engineer': {'Task': {'task': 'You are a Verilog RTL designer that only writes code using correct Verilog syntax and verify the functionality.'
                                                                      'You need to run the verilog_simulation_tool to make sure the functional correctness before TERMINATE.' },
                                                     'Instructions': {'Instructions': '1. Use the verilog_simulation_tool to verify the syntax and functional correctness of the Completed Verilog Module.'
                                                                                      '2. Use the waveform_trace_tool to trace the waveform of functional incorrect signals by inputting the verilog_simulation_tool result.'
                                                                                      '3. Debug the waveform and verilog source code and find out the signals need to be corrected.'
                                                                                      '4. Repeat above steps until pass the syntax and functional check.' },
                                                     'Constraints': {'Constraints':'- Do not use typedef enum in the verilog code.'
                                                                                   "- There is test bench to test the functional correctness. You don't need to generate testbench to test the generated verilog code."
                                                                                   "- Do not use $display or $finish in the module implementation."
                                                                                   "- You can not modify the testbench."
                                                                                   "- Declare all ports as logic; use wire or reg for signals inside the block."
                                                                                   "- Don't use state_t. Use 'reg' or 'logic' for signals as registers or Flip-Flops."
                                                                                   "- for combinational logic, you can use wire assign or always @(*)."
                                                                                   "- for combinational logic with an always block do not explicitly specify the sensitivity list; instead use always @(*)"
                                                                                   "- Don't generate duplicated signal assignments or blocks."
                                                              },
                                                     'last':{'last_prompt': 'The output strictly follows the following format:<verilog>{the target code}</verilog>'
                                                                             'Save the generated Verilog object code:{the target code} to the path: D:\pycharm\autogen-0.2.36\Output\verilog.v'}
                             },
                }
                }
}