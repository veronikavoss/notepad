import chardet

with open('D:/Coding/Python/PySide6/notepad/test3.txt', "rb") as f:
    rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result["encoding"]
    print(encoding)
