import os
from concurrent.futures import ThreadPoolExecutor
import threading
import whisper
import json

folder_path = '/home/aistudio/wav/wav'
threads = []
lock = threading.Lock()
model = whisper.load_model("/home/aistudio/large-v3-turbo.pt")
def send_request(language, file):
    print(f'开始处理{file}')
    try:
        result = model.transcribe("./wav/wav/"+file,language=language)
    except Exception as e:
        with open(f'./error.txt', 'a', encoding='utf-8') as f:
            f.write(file + '出错' +'\n')
        return
    # 使用线程锁来同步文件写入
    with lock:
        with open(f'./output/{language}_whisper.csv', 'a', encoding='utf-8') as f:
            f.write(file + ',' + json.dumps(result,ensure_ascii=False).replace('\n', ''))
            f.write('\n')
send_lst = []
saved_lst = []
for root, dirs, files in os.walk('./output'):
    for file in files:
        if file.find('_whisper.csv') != -1:
            with open('./output/'+file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    saved_lst.append(line.split(',',1)[0].strip().lower())
            #saved_lst.append(file.split(',',1)[0])
for root, dirs, files in os.walk(folder_path):
    for file in files:
        # 检查文件是否以.wav结尾
        if file.endswith('.wav'):
            if file in saved_lst:
                #print(f'跳过{file}')
                continue
            #files = {"file": open("/home/aistudio/wav/wav/"+file, "rb")}
            if file.find('_urss') != -1:
                language = 'ru'
            elif file.find('_fr') != -1:
                language = 'fr'
            elif file.find('_uk') != -1:
                language = 'en'
            elif file.find('_jap') != -1:
                language = 'ja'
            elif file.find('_rok') != -1: #韩国
                language = 'ko'
            elif file.find('_nk') != -1: #朝鲜
                language = 'ko'
            elif file.find('_chi') != -1:
                language = 'zh'
            elif file.find('_rda') != -1: #民主德国的法语简写...
                language = 'de'
            elif file.find('_us') != -1:
                language = 'en'
            elif file.find('_anz') != -1: #ANZAC 澳新军团
                language = 'en'
            elif file.find('_fin') != -1:
                language = 'fi'
            elif file.find('_isr') != -1: #以色列官方语言是希伯来语
                language = 'he'
            elif file.find('_nor') != -1:
                language = 'no'
            elif file.find('_pol') != -1:
                language = 'pl'
            elif file.find('_swe') != -1:
                language = 'sv'
            elif file.find('_tch') != -1: # #TCH (from tchèque, French for "Czech") works on ingame flare markers.
                language = 'cs'
            else:
                continue
            send_request(language, file)

