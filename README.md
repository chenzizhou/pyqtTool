# pyqtTool
工具开发快速模板
AutoGenerateUi.ui用designer设计然后用pyUIc自动生成，不用管它，我们自己封装一个UI类，以便于不用每次修改AutoGenerateUi.ui后自动生成的py文件把我们写好的自定义槽函数和信号覆盖
CustomSlot.py这个模块中类封装啦我们自定义的槽，和以前AutoGenerateUi类进行分离，独立管理，进行解耦
QJMS_TOOL.py这个模块是我们的最终正式工具类，集成UI和自定义槽,最终信和槽的绑定都在改类终实现（小技巧，调试可在AutoGenerateUi.py）

开发完成后，生成exe
https://blog.csdn.net/qq_48979387/article/details/132359366?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522a4a98c480e4f2a588b3712e9fe1f73a4%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=a4a98c480e4f2a588b3712e9fe1f73a4&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-8-132359366-null-null.142^v100^pc_search_result_base8&utm_term=pyinstaller%E5%86%85%E5%B5%8C%E6%96%87%E4%BB%B6%E5%88%B0%E5%8F%AF%E6%89%A7%E8%A1%8C%E6%96%87%E4%BB%B6%E4%B8%AD&spm=1018.2226.3001.4187

主要使用资源嵌入exe
1、创建asserts文件夹
2、把该函数添加到CustomSlot.py这个模块中，使生成的exe文件读取到资源文件
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".") # 当前工作目录的路径
 
    return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径
3、pip install pyinstaller
4、pyinstaller -w -F --add-data assets;assets my_app_name.py
参数说明：
-w 运行exe文件，不显示后台黑窗口
-F dist文件夹中只生成exe文件（--onefile）
--add-data 本地资源;目标资源


