# Bill on OpenAI Compatible

这是Puzzle Hunt活动CCBC 15中题目“Bill, 你的人工智能助手”的OpenAI实现版。比赛进行中时，由CCBC主办方承担AI费用，可在页面上直接调用。比赛结束后，修改为了用户自己需要负责AI调用的费用。

由于原版仅支持在Coze平台上调用，在比赛结束后，许多用户因无法访问Coze平台而无法使用。因此，我们特别制作了OpenAI API兼容版本。只要你有OpenAI兼容的API（绝大多数大模型都有OpenAI兼容模式），就可以使用本工具来还原Bill。

原题目见：[https://archive.cipherpuzzles.com/#/problem?c=ccbc15/problems/7/61](CCBC 15 存档站)

## 安装和启动

### 1. 准备配置文件

我们推荐使用 Python >= 3.8 版本。

首先你需要建立`config.json`文件。填写您的API地址，API密钥（sk）和模型名称。已经为您准备好了一份示例文件，您可以直接修改。

请注意，您使用的模型必须具有工具调用能力，推荐使用 `gpt-4o`。

```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "your-api-key-here",
  "model_name": "gpt-4o",
  "easy_mode": false
}
```

> 注： easy_mode 是一种调试模式，但它直接降低了题目的难度。

### 2. 初始化虚拟环境【可选】

我们强烈建议您使用 `venv` 创建虚拟环境。以下是初始化和激活虚拟环境的命令：

Windows用户：

```sh
python -m venv venv
venv\Scripts\activate
```

macOS/Linux用户：

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

在第一次启动之前，您需要安装 `requests` 库：

```sh
pip install requests
```

### 4. 运行

使用以下命令运行Bill：

```sh
python cli.py
```

启动后，您可以开始与Bill对话。

如果你想做题，请不要看`prompts.py`，你知道的，所有的秘密都在里面。

输入 `exit` 退出，或输入 `clear` 清除聊天历史。
