import subprocess
import json

# C++プログラムのパス
cpp_program_path = './build/json-relay'

# C++プログラムをサブプロセスとして起動
process = subprocess.Popen(
    [cpp_program_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

data_to_send = {'name': 'Alice', 'age': 25}

stdout_data, stderr_data = process.communicate(json.dumps(data_to_send))

if stderr_data:
    print("Error:", stderr_data)

if stdout_data:
    received_json = json.loads(stdout_data)
    print("Received JSON:", received_json)
