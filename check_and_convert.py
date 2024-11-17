import os
import subprocess
import requests
import json
import hashlib

UPSTREAM_REPO = 'https://github.com/SpaceTimee/Cealing-Host.git'
LOCAL_REPO_PATH = '/path/to/your/local/repo'
HASH_FILE = 'hash.txt'
ADGUARD_RULE_FILE = 'adguard_rules.txt'

def get_hash(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def fetch_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def convert_to_adguard_rules(data):
    json_data = json.loads(data)
    rules = []
    for entry in json_data:
        domains = entry[0]
        for domain in domains:
            rules.append(f"||{domain}^")
    return "\n".join(rules)

def main():
    try:
        # 拉取上游仓库的最新更新
        os.chdir(LOCAL_REPO_PATH)
        subprocess.run(['git', 'pull', UPSTREAM_REPO], check=True)

        # 读取并处理Cealing-Host.json文件
        data = fetch_data(os.path.join(LOCAL_REPO_PATH, 'Cealing-Host.json'))
        new_hash = get_hash(data)

        try:
            with open(HASH_FILE, 'r') as f:
                old_hash = f.read().strip()
        except FileNotFoundError:
            old_hash = ""

        if new_hash != old_hash:
            with open(HASH_FILE, 'w') as f:
                f.write(new_hash)

            adguard_rules = convert_to_adguard_rules(data)
            with open(ADGUARD_RULE_FILE, 'w') as f:
                f.write(adguard_rules)
            print("规则文件已更新.")
        else:
            print("没有变化.")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
