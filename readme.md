# Jadx-AI MCP + TRAE 使用指南

## ✅ 配置

1. **TRAE MCP 配置** - 將mcp_config.json文件复制到`C:\Users\当前用户名\.trae`，并且文件里配置内容的路径要确保正确
2. **JADX 插件安装** - 已安装到 `jadx-1.5.5\plugins\jadx-ai-mcp-6.4.0.jar`
3. **依赖包安装** - Python 依赖已安装
4. **jadx下载**  -到官网下载解压到jadx-1.5.5

## 📝 使用步骤

### 第一步：启动 JADX GUI

**方法 1（推荐）：**
双击运行 `start-jadx-with-plugin.bat`

**方法 2：**
进入 `jadx-1.5.5\bin` 目录，双击运行 `jadx-gui.bat`

### 第二步：在 JADX GUI 中打开 APK

1. JADX GUI 启动后
2. 点击 **File → Open File** 
3. 选择你要分析的 APK 文件
4. 等待反编译完成

### 第三步：在 TRAE 中开始使用

现在你可以在 TRAE 中使用以下功能了！

## 🔧 可用的 MCP 工具

### 基础查询
- `get_android_manifest` - 获取 AndroidManifest.xml
- `get_all_classes` - 列出所有类
- `get_package_tree` - 查看包结构
- `get_main_activity_class` - 获取主 Activity

### 代码分析
- `get_class_source` - 获取特定类的源代码
- `get_methods_of_class` - 列出类的方法
- `get_fields_of_class` - 列出类的字段
- `fetch_current_class` - 获取当前在 JADX 中选中的类

### 搜索功能
- `search_classes_by_keyword` - 按关键字搜索类
- `search_method_by_name` - 搜索方法
- `get_method_by_name` - 获取特定方法

### 资源分析
- `get_strings` - 获取 strings.xml
- `get_resource_file` - 获取资源文件
- `get_all_resource_file_names` - 列出所有资源文件

### 重构工具
- `rename_class` - 重命名类
- `rename_method` - 重命名方法
- `rename_field` - 重命名字段
- `rename_variable` - 重命名变量

### 交叉引用
- `get_xrefs_to_class` - 查找类的引用
- `get_xrefs_to_method` - 查找方法的引用
- `get_xrefs_to_field` - 查找字段的引用

## 💡 使用示例

### 示例 1：查看 APK 基本信息
在 TRAE 中问：
> "帮我查看这个 APK 的基本信息，包括包名、主 Activity 和权限"

### 示例 2：搜索特定功能
在 TRAE 中问：
> "帮我搜索这个 APK 中与网络请求相关的代码"

### 示例 3：安全分析
在 TRAE 中问：
> "帮我分析这个 APK 是否有硬编码的密钥或不安全的网络请求"

### 示例 4：代码理解
在 TRAE 中问：
> "这个 MainActivity 类是做什么的？请用中文解释"

## 🛠️ 启动脚本

以后每次使用只需：
1. 双击 `start-jadx-with-plugin.bat` 启动 JADX GUI
2. 在 JADX 中打开你的 APK
3. 在 TRAE 中开始对话

## ⚠️ 注意事项

1. JADX AI MCP 插件默认监听端口 **8650**
2. 必须先在 JADX GUI 中打开 APK 才能使用 MCP 工具
3. 如果 TRAE 提示连接失败，请确认：
   - JADX GUI 正在运行
   - APK 已加载完成
   - 端口 8650 没有被占用

## 🔍 验证连接

要确认插件是否正常工作，可以检查 8650 端口是否在监听。

祝你分析愉快！🚀
