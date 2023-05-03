import os


class Complier:
    def __init__(self,input,mode) -> None:
        self.input_filePath = input
        self.mode = mode

    def decompile(self):
        cmd = "java -jar apktool.jar d " + self.input_filePath
        ret = os.system(cmd)
        if ret != 0 :
            print("someting wrong with decomplie apk")
        else:
            print("decomplie finished!")    

    def repackage(self):
        cmd = "java -jar apktool.jar b " + self.input_filePath + " -o " + self.input_filePath +"_rpkg.apk"
        ret = os.system(cmd)
        if ret != 0 :
            print("someting wrong with repackage apk")
        else:
            print("repackage finished!")


def run_complier(mode):
    if mode == 'd':
        print("please input your apk path:")
        while True:
            apk_path = input()
            if not os.path.exists(apk_path):
                print("please input the right path:xxx/xxx/xxx/xx.apk")
            else:
                break
        complier = Complier(apk_path,mode)    
        complier.decompile()


    elif mode == 'b':
        print("please input your smali file path:")
        while True:
            smali_path = input()
            if not os.path.exists(smali_path):
                print("please input the right smali path:xxx/xxx/xxx/")
            else:
                break
        complier = Complier(smali_path,mode)    
        complier.repackage()