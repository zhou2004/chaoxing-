from src.chapter import *
import json
from bs4 import BeautifulSoup
from src.font_decoder import FontDecoder


#解析章节的iframe的json内容，以字典形式返回
def iframe_decode(iframe_element) -> dict:
    if not iframe_element:
        return None
    data_attribute = iframe_element.get_attribute('data')
    if data_attribute is None:
        return None
    objectid = iframe_element.get_attribute('objectid')

    # 解析JSON字符串
    data_json_str = data_attribute.encode().decode('unicode-escape')
    data_json = json.loads(data_json_str)

    # 提取所需的值，例如'mid'
    mid = data_json.get('mid', None)
    return data_json


#解析题目的html页面，以字典形式返回
def decode_questions_info(html_content) -> dict:
    def replace_rtn(text):
        return text.replace('\r', '').replace('\t', '').replace('\n', '')

    soup = BeautifulSoup(html_content, "lxml")
    form_data = {}
    form_tag = soup.find("form")

    fd = FontDecoder(html_content)  # 加载字体
    if not fd.finished:
        return None
    # 抽取表单信息
    for input_tag in form_tag.find_all("input"):
        if 'name' not in input_tag.attrs or 'answer' in input_tag.attrs["name"]:
            continue
        form_data.update({
            input_tag.attrs["name"]: input_tag.attrs.get("value", '')
        })

    form_data['questions'] = []
    for div_tag in form_tag.find_all("div", class_="singleQuesId"):  # 目前来说无论是单选还是多选的题class都是这个
        q_title = replace_rtn(fd.decode(div_tag.find("div", class_="Zy_TItle").text))
        q_options = ''
        for li_tag in div_tag.find("ul").find_all("li"):
            q_options += replace_rtn(fd.decode(li_tag.text)) + '\n'
        q_options = q_options[:-1]  # 去除尾部'\n'

        # 尝试使用 data 属性来判断题型
        q_type_code = div_tag.find('div', class_='TiMu').attrs['data']
        if q_type_code == '0':
            q_type = 'single'
        elif q_type_code == '1':
            q_type = 'multiple'
        elif q_type_code == '2':
            q_type = 'completion'
        elif q_type_code == '3':
            q_type = 'judgement'

        form_data["questions"].append({
            'id': div_tag.attrs["data"],
            'title': q_title,  # 题目
            'options': q_options,  # 选项 可提供给题库作为辅助
            'type': q_type,  # 题型 可提供给题库作为辅助
            'answerField': {
                'answer' + div_tag.attrs["data"]: '',  # 答案填入处
                'answertype' + div_tag.attrs["data"]: q_type_code
            }
        })
    # 处理答题信息
    form_data['answerwqbid'] = ",".join([q['id'] for q in form_data['questions']]) + ","
    return form_data



