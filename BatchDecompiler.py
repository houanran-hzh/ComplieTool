import os
#需要apktool，和这个脚本放在同一个文件夹，输入输出改个文件夹就行，会遍历文件夹下所有文件

class Batch_decomplier():
    def __init__(self,source,output) -> None:
        self.source_dir = source
        self.output_dir = output
        self.apk_list = ""




    def getFiles(self):
        for filepath,dirnames,filenames in os.walk(self.source_dir):
            for filename in filenames:
                self.apk_list.append(os.path.join(filepath,filename))
        


    def singleDecomplie(apkAbsDir):
        print("apkdir = " + apkAbsDir)
        outPut = outPutAbsDir+apkAbsDir.split('\\')[-1]
        print("output dir =" + outPut)
        cmd = ("java -jar ./apktool.jar d {} --output {}").format(apkAbsDir,outPut)
        print(cmd)
        result = os.system(cmd)
        if (result != 0):
            print(("file {} decomplie failure").format(apkAbsDir))
        else:
            print(("file {} decomplie success").format(apkAbsDir))


    def batchDecomplie():
        for apk in self.apk_List:
            i = 0
            i = i + 1
            if (i > 10):
                return
            print(apk)
            self.singleDecomplie(apk)




#或许人是无法理解这世界更多，所以后怕困于深渊便隐忍不说
#或许人可侥幸自救但嘲讽为何，如此往复永远出走永无理想国