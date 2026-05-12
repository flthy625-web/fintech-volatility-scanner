#!/bin/bash

# Fintech 教育 App 启动脚本

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 检查 Python 和 Streamlit 是否安装
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "未找到 Python 3！\n\n请先安装 Python 3.8 或更高版本。\n\n访问：https://www.python.org/downloads/" buttons {"确定"} default button 1 with icon stop'
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    osascript -e 'display dialog "首次运行，正在安装依赖...\n\n这可能需要几分钟时间。" buttons {"确定"} default button 1 with icon note'

    # 创建虚拟环境
    python3 -m venv venv
    source venv/bin/activate

    # 安装依赖
    pip install --upgrade pip
    pip install -r requirements.txt

    osascript -e 'display dialog "安装完成！应用即将启动..." buttons {"确定"} default button 1 with icon note'
else
    source venv/bin/activate
fi

# 启动 Streamlit
streamlit run app.py --server.headless true --server.port 8501 &

# 等待服务器启动
sleep 3

# 打开浏览器
open http://localhost:8501

# 显示提示
osascript -e 'display notification "应用已在浏览器中打开" with title "Fintech 教育 App" sound name "Glass"'

# 保持脚本运行
wait
