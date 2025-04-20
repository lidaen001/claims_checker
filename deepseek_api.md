首次调用 API
DeepSeek API 使用与 OpenAI 兼容的 API 格式，通过修改配置，您可以使用 OpenAI SDK 来访问 DeepSeek API，或使用与 OpenAI API 兼容的软件。
PARAM	VALUE
base_url *       	https://api.deepseek.com
api_key	apply for an API key
* 出于与 OpenAI 兼容考虑，您也可以将 base_url 设置为 https://api.deepseek.com/v1 来使用，但注意，此处 v1 与模型版本无关。
* deepseek-chat 模型已全面升级为 DeepSeek-V3，接口不变。 通过指定 model='deepseek-chat' 即可调用 DeepSeek-V3。
* deepseek-reasoner 是 DeepSeek 最新推出的推理模型 DeepSeek-R1。通过指定 model='deepseek-reasoner'，即可调用 DeepSeek-R1。
调用对话 API
在创建 API key 之后，你可以使用以下样例脚本的来访问 DeepSeek API。样例为非流式输出，您可以将 stream 设置为 true 来使用流式输出。
curl
python
nodejs
# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)


模型 & 价格
下表所列模型价格以“百万 tokens”为单位。Token 是模型用来表示自然语言文本的的最小单位，可以是一个词、一个数字或一个标点符号等。我们将根据模型输入和输出的总 token 数进行计量计费。
模型 & 价格细节
模型(1)	deepseek-chat	deepseek-reasoner
上下文长度	64K	64K
最大思维链长度(2)	-	32K
最大输出长度(3)	8K	8K
标准时段价格
（北京时间 08:30-00:30）	百万tokens输入（缓存命中）(4)	0.5元	1元
	百万tokens输入（缓存未命中）	2元	4元
	百万tokens输出 (5)	8元	16元
优惠时段价格(6)
（北京时间 00:30-08:30）	百万tokens输入（缓存命中）	0.25元（5折）	0.25元（2.5折）
	百万tokens输入（缓存未命中）	1元（5折）	1元（2.5折）
	百万tokens输出	4元（5折）	4元（2.5折）
1.deepseek-chat 模型对应 DeepSeek-V3；deepseek-reasoner 模型对应 DeepSeek-R1。
2.思维链为deepseek-reasoner模型在给出正式回答之前的思考过程，其原理详见推理模型。
3.如未指定 max_tokens，默认最大输出长度为 4K。请调整 max_tokens 以支持更长的输出。
4.关于上下文缓存的细节，请参考DeepSeek 硬盘缓存。
5.deepseek-reasoner的输出 token 数包含了思维链和最终答案的所有 token，其计价相同。
6.DeepSeek API 现实行错峰优惠定价，每日优惠时段为北京时间 00:30-08:30，其余时间按照标准价格计费。请求的计价时间为该请求完成的时间。
扣费规则
扣减费用 = token 消耗量 × 模型单价，对应的费用将直接从充值余额或赠送余额中进行扣减。 当充值余额与赠送余额同时存在时，优先扣减赠送余额。
产品价格可能发生变动，DeepSeek 保留修改价格的权利。请您依据实际用量按需充值，定期查看此页面以获知最新价格信息。

上一页
首次调用 API


限速
DeepSeek API 不限制用户并发量，我们会尽力保证您所有请求的服务质量。
但请注意，当我们的服务器承受高流量压力时，您的请求发出后，可能需要等待一段时间才能获取服务器的响应。在这段时间里，您的 HTTP 请求会保持连接，并持续收到如下格式的返回内容：
非流式请求：持续返回空行
流式请求：持续返回 SSE keep-alive 注释（: keep-alive）
这些内容不影响 OpenAI SDK 对响应的 JSON body 的解析。如果您在自己解析 HTTP 响应，请注意处理这些空行或注释。
如果 30 分钟后，请求仍未完成，服务器将关闭连接。
错误码
您在调用 DeepSeek API 时，可能会遇到以下错误。这里列出了相关错误的原因及其解决方法。
错误码	描述
400 - 格式错误	原因：请求体格式错误 
解决方法：请根据错误信息提示修改请求体
401 - 认证失败	原因：API key 错误，认证失败 
解决方法：请检查您的 API key 是否正确，如没有 API key，请先 创建 API key
402 - 余额不足	原因：账号余额不足 
解决方法：请确认账户余额，并前往 充值 页面进行充值
422 - 参数错误	原因：请求体参数错误 
解决方法：请根据错误信息提示修改相关参数
429 - 请求速率达到上限	原因：请求速率（TPM 或 RPM）达到上限 
解决方法：请合理规划您的请求速率。
500 - 服务器故障	原因：服务器内部故障 
解决方法：请等待后重试。若问题一直存在，请联系我们解决
503 - 服务器繁忙	原因：服务器负载过高 
解决方法：请稍后重试您的请求
SON Output
在很多场景下，用户需要让模型严格按照 JSON 格式来输出，以实现输出的结构化，便于后续逻辑进行解析。
DeepSeek 提供了 JSON Output 功能，来确保模型输出合法的 JSON 字符串。
注意事项
1.设置 response_format 参数为 {'type': 'json_object'}。
2.用户传入的 system 或 user prompt 中必须含有 json 字样，并给出希望模型输出的 JSON 格式的样例，以指导模型来输出合法 JSON。
3.需要合理设置 max_tokens 参数，防止 JSON 字符串被中途截断。
4.在使用 JSON Output 功能时，API 有概率会返回空的 content。我们正在积极优化该问题，您可以尝试修改 prompt 以缓解此类问题。
样例代码
这里展示了使用 JSON Output 功能的完整 Python 代码：
import json
from openai import OpenAI

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com",
)

system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={
        'type': 'json_object'
    }
)

print(json.loads(response.choices[0].message.content))
模型将会输出：
{
    "question": "Which is the longest river in the world?",
    "answer": "The Nile River"
}
推理模型 (deepseek-reasoner)
deepseek-reasoner 是 DeepSeek 推出的推理模型。在输出最终回答之前，模型会先输出一段思维链内容，以提升最终答案的准确性。我们的 API 向用户开放 deepseek-reasoner 思维链的内容，以供用户查看、展示、蒸馏使用。
在使用 deepseek-reasoner 时，请先升级 OpenAI SDK 以支持新参数。
pip3 install -U openai
API 参数

输入参数：

omax_tokens：最终回答的最大长度（不含思维链输出），默认为 4K，最大为 8K。请注意，思维链的输出最多可以达到 32K tokens，控思维链的长度的参数（reasoning_effort）将会在近期上线。

输出字段：

oreasoning_content：思维链内容，与 content 同级，访问方法见访问样例
ocontent：最终回答内容

上下文长度：API 最大支持 64K 上下文，输出的 reasoning_content 长度不计入 64K 上下文长度中


支持的功能：对话补全，对话前缀续写 (Beta)


不支持的功能：Function Call、Json Output、FIM 补全 (Beta)


不支持的参数：temperature、top_p、presence_penalty、frequency_penalty、logprobs、top_logprobs。请注意，为了兼容已有软件，设置 temperature、top_p、presence_penalty、frequency_penalty 参数不会报错，但也不会生效。设置 logprobs、top_logprobs 会报错。

上下文拼接
在每一轮对话过程中，模型会输出思维链内容（reasoning_content）和最终回答（content）。在下一轮对话中，之前轮输出的思维链内容不会被拼接到上下文中，如下图所示：

请注意，如果您在输入的 messages 序列中，传入了reasoning_content，API 会返回 400 错误。因此，请删除 API 响应中的 reasoning_content 字段，再发起 API 请求，方法如访问样例所示。
访问样例
下面的代码以 Python 语言为例，展示了如何访问思维链和最终回答，以及如何在多轮对话中进行上下文拼接。
非流式
流式
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

# Round 2
messages.append({'role': 'assistant', 'content': content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)
# ...
多轮对话
本指南将介绍如何使用 DeepSeek /chat/completions API 进行多轮对话。
DeepSeek /chat/completions API 是一个“无状态” API，即服务端不记录用户请求的上下文，用户在每次请求时，需将之前所有对话历史拼接好后，传递给对话 API。
下面的代码以 Python 语言，展示了如何进行上下文拼接，以实现多轮对话。
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "What's the highest mountain in the world?"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 1: {messages}")

# Round 2
messages.append({"role": "user", "content": "What is the second?"})
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 2: {messages}")

在第一轮请求时，传递给 API 的 messages 为：
[
    {"role": "user", "content": "What's the highest mountain in the world?"}
]
在第二轮请求时：
1.要将第一轮中模型的输出添加到 messages 末尾
2.将新的提问添加到 messages 末尾
最终传递给 API 的 messages 为：
[
    {"role": "user", "content": "What's the highest mountain in the world?"},
    {"role": "assistant", "content": "The highest mountain in the world is Mount Everest."},
    {"role": "user", "content": "What is the second?"}
]
对话前缀续写（Beta）
对话前缀续写沿用 Chat Completion API，用户提供 assistant 开头的消息，来让模型补全其余的消息。
注意事项
1.使用对话前缀续写时，用户需确保 messages 列表里最后一条消息的 role 为 assistant，并设置最后一条消息的 prefix 参数为 True。
2.用户需要设置 base_url="https://api.deepseek.com/beta" 来开启 Beta 功能。
样例代码
下面给出了对话前缀续写的完整 Python 代码样例。在这个例子中，我们设置 assistant 开头的消息为 "```python\n" 来强制模型输出 python 代码，并设置 stop 参数为 ['```'] 来避免模型的额外解释。
from openai import OpenAI

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com/beta",
)

messages = [
    {"role": "user", "content": "Please write quick sort code"},
    {"role": "assistant", "content": "```python\n", "prefix": True}
]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    stop=["```"],
)
print(response.choices[0].message.content)

上一页
多轮对话


Function Calling
Function Calling 让模型能够调用外部工具，来增强自身能力。
样例代码
这里以获取用户当前位置的天气信息为例，展示了使用 Function Calling 的完整 Python 代码。
Function Calling 的具体 API 格式请参考对话补全文档。
from openai import OpenAI

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of an location, the user shoud supply a location first",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)

messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
message = send_messages(messages)
print(f"Model>\t {message.content}")
这个例子的执行流程如下：
1.用户：询问现在的天气
2.模型：返回 function get_weather({location: 'Hangzhou'})
3.用户：调用 function get_weather({location: 'Hangzhou'})，并传给模型。
4.模型：返回自然语言，"The current temperature in Hangzhou is 24°C."
注：上述代码中 get_weather 函数功能需由用户提供，模型本身不执行具体函数。
上下文硬盘缓存
DeepSeek API 上下文硬盘缓存技术对所有用户默认开启，用户无需修改代码即可享用。
用户的每一个请求都会触发硬盘缓存的构建。若后续请求与之前的请求在前缀上存在重复，则重复部分只需要从缓存中拉取，计入“缓存命中”。
注意：两个请求间，只有重复的前缀部分才能触发“缓存命中”，详间下面的例子。

例一：长文本问答
第一次请求
messages: [
    {"role": "system", "content": "你是一位资深的财报分析师..."}
    {"role": "user", "content": "<财报内容>\n\n请总结一下这份财报的关键信息。"}
]
第二次请求
messages: [
    {"role": "system", "content": "你是一位资深的财报分析师..."}
    {"role": "user", "content": "<财报内容>\n\n请分析一下这份财报的盈利情况。"}
]
在上例中，两次请求都有相同的前缀，即 system 消息 + user 消息中的 <财报内容>。在第二次请求时，这部分前缀会计入“缓存命中”。

例二：多轮对话
第一次请求
messages: [
    {"role": "system", "content": "你是一位乐于助人的助手"},
    {"role": "user", "content": "中国的首都是哪里？"}
]
第二次请求
messages: [
    {"role": "system", "content": "你是一位乐于助人的助手"},
    {"role": "user", "content": "中国的首都是哪里？"},
    {"role": "assistant", "content": "中国的首都是北京。"},
    {"role": "user", "content": "美国的首都是哪里？"}
]
在上例中，第二次请求可以复用第一次请求开头的 system 消息和 user 消息，这部分会计入“缓存命中”。

例三：使用 Few-shot 学习
在实际应用中，用户可以通过 Few-shot 学习的方式，来提升模型的输出效果。所谓 Few-shot 学习，是指在请求中提供一些示例，让模型学习到特定的模式。由于 Few-shot 一般提供相同的上下文前缀，在硬盘缓存的加持下，Few-shot 的费用显著降低。
第一次请求
messages: [    
        {"role": "system", "content": "你是一位历史学专家，用户将提供一系列问题，你的回答应当简明扼要，并以`Answer:`开头"},
        {"role": "user", "content": "请问秦始皇统一六国是在哪一年？"},
        {"role": "assistant", "content": "Answer:公元前221年"},
        {"role": "user", "content": "请问汉朝的建立者是谁？"},
        {"role": "assistant", "content": "Answer:刘邦"},
        {"role": "user", "content": "请问唐朝最后一任皇帝是谁"},
        {"role": "assistant", "content": "Answer:李柷"},
        {"role": "user", "content": "请问明朝的开国皇帝是谁？"},
        {"role": "assistant", "content": "Answer:朱元璋"},
        {"role": "user", "content": "请问清朝的开国皇帝是谁？"}
]
第二次请求
messages: [    
        {"role": "system", "content": "你是一位历史学专家，用户将提供一系列问题，你的回答应当简明扼要，并以`Answer:`开头"},
        {"role": "user", "content": "请问秦始皇统一六国是在哪一年？"},
        {"role": "assistant", "content": "Answer:公元前221年"},
        {"role": "user", "content": "请问汉朝的建立者是谁？"},
        {"role": "assistant", "content": "Answer:刘邦"},
        {"role": "user", "content": "请问唐朝最后一任皇帝是谁"},
        {"role": "assistant", "content": "Answer:李柷"},
        {"role": "user", "content": "请问明朝的开国皇帝是谁？"},
        {"role": "assistant", "content": "Answer:朱元璋"},
        {"role": "user", "content": "请问商朝是什么时候灭亡的"},        
]
在上例中，使用了 4-shots。两次请求只有最后一个问题不一样，第二次请求可以复用第一次请求中前 4 轮对话的内容，这部分会计入“缓存命中”。

查看缓存命中情况
在 DeepSeek API 的返回中，我们在 usage 字段中增加了两个字段，来反映请求的缓存命中情况：
1.
prompt_cache_hit_tokens：本次请求的输入中，缓存命中的 tokens 数（0.1 元 / 百万 tokens）
2.
3.
prompt_cache_miss_tokens：本次请求的输入中，缓存未命中的 tokens 数（1 元 / 百万 tokens）
4.
硬盘缓存与输出随机性
硬盘缓存只匹配到用户输入的前缀部分，输出仍然是通过计算推理得到的，仍然受到 temperature 等参数的影响，从而引入随机性。其输出效果与不使用硬盘缓存相同。
其它说明
1.
缓存系统以 64 tokens 为一个存储单元，不足 64 tokens 的内容不会被缓存
2.
3.
缓存系统是“尽力而为”，不保证 100% 缓存命中
4.
5.
缓存构建耗时为秒级。缓存不再使用后会自动被清空，时间一般为几个小时到几天
6.
