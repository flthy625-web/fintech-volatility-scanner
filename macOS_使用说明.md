# 🎓 Fintech 教育 App - macOS 版使用说明

## ✅ 已创建的 macOS App

你的应用已经打包成 macOS App！

**位置**：`~/fintech-volatility-scanner/Fintech教育App.app`

---

## 🚀 如何使用

### 方法 1：直接双击打开（推荐）

1. 打开 Finder
2. 前往：`~/fintech-volatility-scanner/`
3. 双击 **Fintech教育App.app**
4. 首次运行会自动安装依赖（需要几分钟）
5. 安装完成后，浏览器会自动打开应用

### 方法 2：移动到应用程序文件夹

```bash
# 复制到应用程序文件夹
cp -r ~/fintech-volatility-scanner/Fintech教育App.app ~/Applications/

# 然后从启动台或应用程序文件夹打开
```

### 方法 3：创建桌面快捷方式

```bash
# 创建替身到桌面
ln -s ~/fintech-volatility-scanner/Fintech教育App.app ~/Desktop/Fintech教育App.app
```

---

## 📋 首次运行

### 1. 系统要求
- ✅ macOS 10.13 或更高版本
- ✅ Python 3.8 或更高版本

### 2. 首次启动流程

**第一步**：双击 App
- 如果提示"无法打开"，右键点击 → 选择"打开" → 点击"打开"

**第二步**：自动安装依赖
- 会弹出提示："首次运行，正在安装依赖..."
- 等待 2-5 分钟（取决于网速）

**第三步**：应用启动
- 安装完成后会提示："安装完成！应用即将启动..."
- 浏览器自动打开 `http://localhost:8501`

**第四步**：开始使用
- 🎉 应用已就绪！

---

## 🎯 功能说明

### 📊 市场扫描（主页）
- 多资产波动监控
- Binance USDT 交易对实时数据
- 量价关系分析
- 自动化预警

### 📚 学习中心（新增）
- 金融知识库
- 初级/中级/高级概念
- 学习进度追踪
- 实战案例分析

### 📝 知识测验（即将推出）
- 概念测试
- 实战分析题
- 即时反馈

---

## ⚠️ 常见问题

### Q1: 双击后没有反应？
**A**: 右键点击 App → 选择"打开" → 点击"打开"（macOS 安全机制）

### Q2: 提示"未找到 Python 3"？
**A**: 
```bash
# 安装 Python 3
brew install python3

# 或访问官网下载
open https://www.python.org/downloads/
```

### Q3: 端口被占用？
**A**: 
```bash
# 查找占用 8501 端口的进程
lsof -i :8501

# 杀死进程
kill -9 <PID>
```

### Q4: 如何关闭应用？
**A**: 
- 关闭浏览器标签页
- 或在终端运行：`pkill -f streamlit`

### Q5: 如何更新应用？
**A**: 
```bash
cd ~/fintech-volatility-scanner
git pull origin main
rm -rf venv  # 删除旧的虚拟环境
# 下次启动会自动重新安装依赖
```

---

## 🔧 手动启动（备用方案）

如果 App 无法正常工作，可以手动启动：

```bash
# 进入项目目录
cd ~/fintech-volatility-scanner

# 激活虚拟环境
source venv/bin/activate

# 启动应用
streamlit run app.py
```

---

## 📦 卸载

```bash
# 删除 App
rm -rf ~/fintech-volatility-scanner/Fintech教育App.app

# 删除整个项目（可选）
rm -rf ~/fintech-volatility-scanner
```

---

## 🎓 学习建议

1. **从学习中心开始**
   - 先学习基础概念
   - 理解流动性、波动率、量价关系

2. **结合市场扫描实践**
   - 观察真实市场数据
   - 验证所学理论

3. **完成知识测验**
   - 检验学习成果
   - 巩固知识点

4. **定期使用**
   - 每天观察市场变化
   - 培养市场直觉

---

## 📞 技术支持

- GitHub: https://github.com/flthy625-web/fintech-volatility-scanner
- Issues: https://github.com/flthy625-web/fintech-volatility-scanner/issues

---

## 📄 许可证

MIT License - 免费使用，仅供教育目的

---

**祝学习愉快！🎉**
