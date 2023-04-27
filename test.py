import subprocess



            #use subprocess to check items in a keystore
process = subprocess.Popen("apktool",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr = process.communicate()
output = stdout.decode("utf-8")
if output:

    print(str(output) + "op")
else:
    print(str(stderr) + "err")
       
