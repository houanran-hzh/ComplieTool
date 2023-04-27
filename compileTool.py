import os
import glob
import time
import subprocess
import re



"""
apktool实现反编译和重打包
"""
def check_java_env():
    process = subprocess.Popen("java",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    output = stdout.decode("utf-8")
    if stderr:
        print("please check your jre or jdk config!!!")
        time.sleep(2)
        exit()

def decompile(apk_path):
    cmd = "java -jar apktool.jar d " + apk_path
    ret = os.system(cmd)
    if ret != 0 :
        print("someting wrong with decomplie apk")


def repackage(smali_path):
    cmd = "java -jar apktool.jar b " + smali_path + " -o " + smali_path +"_rpkg.apk"
    ret = os.system(cmd)
    if ret != 0 :
        print("someting wrong with repackage apk")




"""
检查当前是否存在签名文件
如果
"""
class Singer():
    def _init_(self):
        self.keystore = ""
        self.alias = ""
        self.apk_path = ""
        self.password = ""

    def choose_keystore(self):
        keystore_list = glob.glob("*.jks")



        if len(keystore_list) == 0:
            print("there are no jks exist,do you want to generate a keysotre[Y/N]")
            choose = input()
            if choose == "y" or choose =="Y" :
                print("please input your keystore name:")
                self.keystore = input()+ ".jks"
                print("please input your alias name(item of keystore):")
                self.alias = input()    
                self.generate_signkey()
            else:
                print("please move a keystore to current dir!") 
                time.sleep(10)  
                exit()


        elif len(keystore_list) > 1:
            print("please choose whitch keystore to use:")
            print("current choice: "+str(keystore_list))
            kestore = input()
            while(kestore not in keystore_list):
                print("please input correct keystore name:")
                kestore = input()
            self.keystore = kestore + ".jks"

        else:
            print("the only keystore in current dir is " + keystore_list[0]+",ganna use this keystore.")
            self.keystore = keystore_list[0] 
            time.sleep(0)





    def choose_alias(self):
        print("please input your password of your keystore：")
        while True:
            self.password = input()

            #use subprocess to check items in a keystore
            process = subprocess.Popen(["keytool","-list","-v","-keystore",self.keystore ,"-storepass",self.password],
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout,stderr = process.communicate()
            output = stdout.decode("utf-8")
            print(output)
            print(stderr)
            alias_pattern = re.compile(r"别名:(.+)")
            alias_list = alias_pattern.findall(output)

            if process.poll() is None:
                process.kill()



            if alias_list:
                print("please choose a alias:\n" + str(alias_list))
                alias = input()
                while alias not in alias_list:
                    print("please input correct alias name!:")
                    alias = input()
                self.alias = alias
                break

            else:
                print("please input the correct password")






    def generate_signkey(self):
        cmd = "keytool -genkeypair -alias "+self.alias+" -keyalg RSA -keysize 2048 -validity 365000 -keystore " + self.keystore +".jks"
        ret = os.system(cmd)
        if ret != 0:
            print("someting wrong with generate signkey")


    def sign_apk(self):
        cmd = "jarsigner -verbose -sigalg RSA -digestalg SHA1 -keystore "+ self.keystore + " " + self.apk_path + " " + self.alias
        ret = os.system(cmd)
        if ret != 0 :
            print("someting wrong with sign_apk")


    def signer(self):
        print("please input the path of apk you want to sign")
        while True:
            apk_path = input()
            if not os.path.exists(apk_path):
                print("please input the right path:xxx/xxx/xxx/xx.apk")
            else:
                break
        self.apk_path = apk_path
        self.choose_keystore()
        self.choose_alias()
        self.sign_apk()



    #decompiler("/home/heou/mytools/com.ximalaya.ting.android_9.1.15.3_593.apk")





if __name__ == '__main__':
    #check_java_env()
    while True:
        print("please input:d for decomplie,b for repackage,s for signing model,exit for exit:")
        order = input()
        if order == 'd':
            print("please input your apk path:")
            while True:
                apk_path = input()
                if not os.path.exists(apk_path):
                    print("please input the right path:xxx/xxx/xxx/xx.apk")
                else:
                    break
            decompile(apk_path)
            print("decomplie finished!")


        elif order == 'b':
            print("please input your smali file path:")
            while True:
                smali_path = input()
                if not os.path.exists(smali_path):
                    print("please input the right smali path:xxx/xxx/xxx/")
                else:
                    break
            repackage(smali_path) 
            print("repackage finished!")


        elif order == 's':
            singer = Singer()
            singer.signer()
            print("signer model finish!")

        elif order == 'exit':
            exit()


        else:
            print("please input the right order(d,b,or s)")