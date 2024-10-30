from alanbasepy import *

class arraytobin:
    def __init__(self):
        return

    def pocess(self, file):
        # 读取C源文件并提取数组数据 
        with open(file, 'r') as f: 
            c_content = f.read()
        f.close()

        start = c_content.index("{")
        end = c_content.index("}")
        result = c_content[start +1:end]
        # result =re.search(r"\{(.*?)\}", c_content).group(1)

        # 提取数组，去除空格和换行，并按逗号分割
        array_str = result.replace(' ', '')
        array_str = array_str.replace('\n', '')
        hex_numbers = array_str.split(',')

        # 把十六进制字符串转换成整数并存储到列表
        list_num = [int(hex_num.strip(), 16) for hex_num in hex_numbers if hex_num.strip()]

        filepath = file.replace('.c', '.bin')
        if fileExists(filepath) == True:
            os.remove(filepath)
        binfile = open(filepath, 'ab+') #追加写入
        for content in list_num:
            content= content.to_bytes(1, 'big')
            binfile.write(content)
        binfile.close()

        # # 打印列表 
        # print(list_num)
