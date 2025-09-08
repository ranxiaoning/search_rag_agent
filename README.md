# LangGraph DeepSeek AI Agent项目

这是一个基于 LangGraph 和 DeepSeek 模型的 AI Agent项目，具备多工具调用能力，包括网络搜索、天气查询、文件处理和 RAG 检索功能。
<img width="1893" height="1399" alt="image" src="https://github.com/user-attachments/assets/13877388-834a-40e1-a769-5020a55209d7" />

## 功能特性

- 🤖 基于 DeepSeek 模型的智能对话
- 🔍 集成 Tavily 网络搜索工具
- 🌤️ OpenWeather 天气查询功能
- 📄 支持 TXT/PDF 文件上传和处理
- 🧠 RAG (检索增强生成) 文档检索功能
- 🔧 多工具调用和状态管理

## 项目结构

```
project/
├── main.py              # 主程序文件
├── .env                 # 环境变量配置文件
├── chroma_db/           # 向量数据库存储目录
├── requirements.txt     # Python 依赖包列表
└── README.md           # 项目说明文档
```

## 环境要求

- Python 3.8+
- Node.js 16+ (前端)
- pnpm (包管理器)

## 安装和设置

### 1. 克隆项目

```bash
git clone <your-project-repo>
cd <your-project-directory>
```

### 2. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 3. 设置环境变量

创建 `.env` 文件并配置以下环境变量：

```env
# DeepSeek API 密钥
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# OpenAI API 配置 (用于嵌入模型)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_URL=https://api.openai.com/v1

# Tavily 搜索 API 密钥
TAVILY_API_KEY=your_tavily_api_key_here

# OpenWeather API 密钥
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

### 4. 安装前端依赖

```bash
# 克隆前端项目
git clone https://github.com/langchain-ai/agent-chat-ui.git
cd agent-chat-ui

# 安装 pnpm (如果尚未安装)
npm install -g pnpm

# 检查 pnpm 版本
pnpm -v

# 安装项目依赖
pnpm install
```

## 运行项目

### 启动后端服务

```bash
langgraph dev
```

后端服务将在默认端口（通常是 8000）启动。

### 启动前端服务

```bash
# 在前端项目目录中
pnpm dev
```

前端服务将在默认端口（通常是 3000）启动。

## API 端点

启动后端服务后，可通过以下端点访问：

- `POST /invoke` - 调用代理处理用户输入
- `GET /graph` - 查看图结构
- `GET /playground` - 交互式测试界面

## 使用方法

### 1. 基本对话

直接与 AI Agent进行对话：

```
用户: 你好，你是谁？
AI: 我是基于 DeepSeek 模型的 AI 助手...
```

### 2. 网络搜索

```
用户: 搜索一下最新的 AI 新闻
AI: [使用搜索工具获取最新信息并回复]
```

### 3. 天气查询

```
用户: 今天北京的天气怎么样？
AI: [调用天气API获取数据并回复]
```

### 4. 文件处理

```
用户: 我需要上传 /path/to/document.pdf 这个文件
AI: [处理PDF文件并存储到向量数据库]
```

### 5. 文档检索

```
用户: 根据我上传的文件，XX主题是什么？
AI: [从已上传文档中检索相关信息并回答]
```

## 工具说明

### 1. 搜索工具 (TavilySearch)

- 功能：执行网络搜索
- 参数：查询关键词
- 返回：最相关的5个搜索结果

### 2. 天气查询 (get_weather)

- 功能：查询指定城市的天气
- 参数：城市英文名称 (如 Beijing)
- 返回：JSON格式的天气数据

### 3. 文件处理 (process_uploaded_file)

- 功能：处理上传的TXT或PDF文件
- 参数：文件路径和类型
- 返回：处理结果确认信息

### 4. RAG检索 (rag_retrieval)

- 功能：从已上传文档中检索信息
- 参数：查询语句
- 返回：相关文档内容

## 开发说明

### 自定义工具

要添加新工具，请按照以下步骤：

1. 使用 `@tool` 装饰器创建工具函数
2. 定义适当的参数模式 (使用 Pydantic 模型)
3. 将工具添加到 `tools` 列表中
4. 重新启动服务

### 修改模型

要更改使用的模型，修改 `model` 初始化代码：

```python
model = ChatDeepSeek(model="deepseek-chat", api_key=os.getenv('DEEPSEEK_API_KEY'))
```

### 调整向量数据库

当前使用 ChromaDB 作为向量存储，可以修改为其他向量数据库：

```python
# 例如使用 FAISS
from langchain_community.vectorstores import FAISS
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
```

## 故障排除

### 常见问题

1. **API 密钥错误**：确保所有环境变量已正确设置
2. **端口冲突**：修改默认端口或停止占用端口的其他服务
3. **依赖冲突**：使用虚拟环境管理 Python 依赖

### 日志查看

后端服务日志会直接显示在控制台，前端错误可以在浏览器开发者工具中查看。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目。

## 许可证

本项目基于 MIT 许可证开源。

## 支持

如有问题，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至项目维护者

---

感谢使用本 AI Agent项目！
