import PySide6.QtCore as QtCore

file_path = "test2.txt"
file = QtCore.QFile(file_path)
if file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
    stream = QtCore.QTextStream(file)
    stream.setAutoDetectUnicode(True)  # 자동으로 인코딩 검사
    text = stream.readAll()
    file.close()
    print(text)
    if "\r\n" in text:
        print("File EOL: Windows")
    elif "\r" in text:
        print("File EOL: Mac")
    else:
        print("File EOL: Unix")
    file.close()
