import subprocess

def start_batch(a,b):
    filepath = r'detail.bat'
    i = 1
    SW_HIDE = 0
    SW_MINIMIZE = 6
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    while i <= b:
        subprocess.Popen([filepath, str(a)], creationflags=subprocess.CREATE_NEW_CONSOLE)
        i = i + 1
        a = a + 50000

a = input("Batas Awal : ")

print("\n-----Setiap scraper otomatis menambahkan 50 ribu id-----\n")
b = input("Banyak Scraper : ")
print("-----Start Scrape shopid dari {} sampai {}".format(a, int(a) - 1 + int(b)*50000))
start_batch(int(a),int(b))
