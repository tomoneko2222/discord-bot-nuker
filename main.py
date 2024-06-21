from colorama import Fore, Style, init
import shutil
import subprocess

# coloramaを初期化
init()

# バナーを中央に表示する関数
def print_banner(banner):
    # 現在のターミナルのサイズを取得
    columns, rows = shutil.get_terminal_size()
    for line in banner.split('\n'):
        # バナーの各行を中央に配置
        print(line.center(columns))

# バナーのテキスト
banner_text = """
 ██████╗ █████╗ ████████╗    ████████╗ ██████╗  ██████╗ ██╗     
██╔════╝██╔══██╗╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██║     ███████║   ██║          ██║   ██║   ██║██║   ██║██║     
██║     ██╔══██║   ██║          ██║   ██║   ██║██║   ██║██║     
╚██████╗██║  ██║   ██║          ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═════╝╚═╝  ╚═╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
╔═════════════════════════════════════════════════╗
║1.DMspam         2.Channeldelete  3.CreateChannel║
║4.nuker          5.roleDelete     6.roleCreate   ║
║7.allkick        8.allban         9.unbanall     ║
╚═════════════════════════════════════════════════╝

"""

# バナーを緑色で表示
print(Fore.MAGENTA + Style.BRIGHT)
print_banner(banner_text)
print(Style.RESET_ALL)

# ユーザーに入力を求める
user_input = input('   >')

# 入力に応じてスクリプトを実行
if user_input == '1':
    subprocess.run(['python', 'tool/dmspam.py'])
elif user_input == '2':
    subprocess.run(['python', 'tool/Channel alldelete.py'])
elif user_input == '3':
    subprocess.run(['python', 'tool/Create Channel.py'])
elif user_input == '4':
    subprocess.run(['python', 'tool/nuker.py'])
elif user_input == '5':
    subprocess.run(['python', 'tool/roleDelete.py'])
elif user_input == '6':
    subprocess.run(['python', 'tool/roleCreate.py'])
elif user_input == '7':
    subprocess.run(['python', 'tool/allkick.py'])
elif user_input == '8':
    subprocess.run(['python', 'tool/allban.py'])
elif user_input == '9':
    subprocess.run(['python', 'tool/unbanall.py'])
else:
    print("error")
