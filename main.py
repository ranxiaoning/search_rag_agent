import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import requests, json
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import tempfile
import shutil

# 加载环境变量
load_dotenv(override=True)

# 内置搜索工具
search_tool = TavilySearch(max_results=5, topic="general", tavily_api_key=os.getenv("TAVILY_API_KEY"))

# 初始化嵌入模型
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_API_URL"))

# 全局向量存储
vectorstore = None


class WeatherQuery(BaseModel):
    loc: str = Field(description="The location name of the city")


@tool(args_schema=WeatherQuery)
def get_weather(loc):
    """
    查询即时天气函数
    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称，\
    注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，则loc参数需要输入'Beijing'；
    :return：OpenWeather API查询即时天气的结果，具体URL请求地址为：https://api.openweathermap.org/data/2.5/weather\
    返回结果对象类型为解析之后的JSON格式对象，并用字符串形式进行表示，其中包含了全部重要的天气信息
    """
    # Step 1.构建请求
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2.设置查询参数
    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),  # 输入API key
        "units": "metric",  # 使用摄氏度而不是华氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    # Step 3.发送GET请求
    response = requests.get(url, params=params)

    # Step 4.解析响应
    data = response.json()
    return json.dumps(data)


class FileUpload(BaseModel):
    file_path: str = Field(description="上传文件的路径")
    file_type: str = Field(description="文件类型，txt或pdf")


@tool(args_schema=FileUpload)
def process_uploaded_file(file_path: str, file_type: str):
    """
    处理上传的TXT或PDF文件，将其内容加载到向量数据库中用于后续检索
    :param file_path: 上传文件的路径
    :param file_type: 文件类型，txt或pdf
    :return: 处理结果的确认信息
    """
    global vectorstore

    try:
        # 根据文件类型选择合适的加载器
        if file_type.lower() == 'pdf':
            loader = PyPDFLoader(file_path)
        else:  # 默认为txt
            loader = TextLoader(file_path, encoding='utf-8')

        # 加载文档
        documents = loader.load()

        print(documents)
        # 分割文本
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)

        # 创建或更新向量存储
        if vectorstore is None:
            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embeddings,
                persist_directory="./chroma_db"
            )
        else:
            vectorstore.add_documents(splits)

        return f"成功处理{file_type.upper()}文件，已加载到知识库中。共处理{len(splits)}个文本块。"

    except Exception as e:
        return f"处理文件时出错: {str(e)}"


@tool
def rag_retrieval(query: str):
    """
    从已上传的文档中检索相关信息
    :param query: 检索查询
    :return: 检索到的相关文档内容
    """
    global vectorstore

    if vectorstore is None:
        return "尚未上传任何文档，请先使用process_uploaded_file工具上传文档。"

    try:
        # 执行相似性搜索
        docs = vectorstore.similarity_search(query, k=3)

        # 格式化结果
        result = "从上传文档中检索到的相关信息:\n\n"
        for i, doc in enumerate(docs):
            result += f"文档片段 {i + 1}:\n{doc.page_content}\n\n"

        return result
    except Exception as e:
        return f"检索过程中出错: {str(e)}"


# 创建工具列表
tools = [search_tool, get_weather, process_uploaded_file, rag_retrieval]

# 创建模型
model = ChatDeepSeek(model="deepseek-chat", api_key=os.getenv('DEEPSEEK_API_KEY'))

# 创建图
graph = create_react_agent(model=model, tools=tools)




if __name__ == '__main__':
    # 示例：处理用户查询
    # response = graph.invoke({"messages": [{"role": "user", "content": "你知道虞书欣和张昊玥的事情吗"}]})
    # print(response)
    # print(response["messages"][-1].content)


    # 使用RAG功能查询
    rag_response = graph.invoke({"messages": [{"role": "user", "content": "我需要上传C:\\Users\\Administrator\\Desktop\\nan\\HuangNan-DS.pdf这个文件，根据我上传的文件，黄楠是谁"}]})
    print(rag_response["messages"][-1].content)