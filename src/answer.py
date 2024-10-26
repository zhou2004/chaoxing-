from openai import OpenAI
import re

"""
此脚本为一个简易的GPT-3.5模型，需要自己配置api,用于回答chaoxing的题目测试，作为一个简单的题库
因为知识有限，回答的答案正确率比较低，主要用于学习
"""


def reload_api(api:str, base_url:str) :
    # 配置api
    global client
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api,
        base_url=base_url
    )



#配置api
# client = OpenAI(
#     # defaults to os.environ.get("OPENAI_API_KEY")
#     api_key = API,
#     base_url = Base_URL
# )


#实例化一个问题类
class Ansewer:
    """
    The class is used for searching answers 
    """
    #初始化包含两个参数，question：问题，question_tpye:问题类型
    def __init__(self, question: str,question_type:str):
        self.question = question
        self.question_type = question_type
        self.answer = ""
        self.final_answer = ""

    #问题信息构建，用于抛给AI问答
    def _std_message_constructor(self, classification: str, content: str):

        if classification == "single":
            prefix = "你是一个超级学霸，这是一道单选题，请直接给出答案 "
        elif classification == "multiple":
            prefix = "你是一个超级学霸，这是一道多选题，不止一个答案，请给出所有答案选项,每个选项以逗号隔开,如:A,B,C "
        elif classification == "judgement":
            prefix = "你是一个超级学霸，这是一道判断题，请直接给出答案 "
        elif classification == "completion":
            prefix = "你是一个超级学霸，这是一道填空题，请直接给出答案,若有多个答案，不要有标点符号 "
        else :
            prefix = "你是一个超级学霸，这是一道简答题，请简要回答，字数在100字以内"
        return [{'role': "user", 'content': prefix+content}]



    #核心函数，分题目类型把问题给AI并拿到答案
    def get_answer(self):
        #先构建问题
        messages = self._std_message_constructor(
            self.question_type, self.question)

        #流式调用AI，获取问题答案
        self.gpt_35_api_stream(messages)

        """
        下列判断用于简单的检索答案
        """
        #单选题检索
        if self.question_type == "single":
            #匹配答案的A-D选项
            pattern = re.compile(r"([A-D])")
            mat=pattern.search(self.answer)
            if mat is not None:
                self.final_answer = mat.group(0)
            else:
                self.final_answer = 'C'
                print("答案解释失败，随机回答")
                #raise Exception("单选题答案解析失败")

        #多选题检索
        elif self.question_type == "multiple":
            pattern = re.compile(r"([A-F])")
            mat = pattern.search(self.answer)
            if mat is not None:
                self.final_answer = self.answer
            else:
                self.final_answer = "A,C"
                print("答案解释失败，随机回答")
                #raise Exception("多选题答案解析失败")

        #判断题检索
        elif self.question_type == "judgement":
            pattern = re.compile(r"([A-B])")
            mat=pattern.search(self.answer)
            if mat is not None:
                self.final_answer = mat.group(0)
            else:
                self.final_answer = 'A'
                print("答案解释失败，随机回答")
                #raise Exception("判断题答案解析失败")

        #填空题检索
        elif self.question_type == "completion":
            self.final_answer = self.answer

        return self.final_answer

        
            
        

    def gpt_35_api_stream(self, messages: list):
        """为提供的对话消息创建新的回答 (流式传输)

        Args:
            messages (list): 完整的对话消息
        """
        answer = []
        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # self.answer = str(chunk.choices[0].delta.content).join("")
                answer.append(str(chunk.choices[0].delta.content))
        
        self.answer = "".join(answer)
                

#此为测试代码
if __name__ == '__main__':
    question =  """
                1【单选题】设样本空间为,根据概率的公理化定义可知事件A的概率P(A)为A的函数,该函数的定义域为( )
                A样本空间\nB样本空间的所有子集构成的集合\nC\nD
                """
    # 非流式调用
    # gpt_35_api(messages)
    # 流式调用
    question_type = 'single'
    an = Ansewer(question,question_type)
    ans = an.get_answer()
    print(ans)
