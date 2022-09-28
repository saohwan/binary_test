import os.path

import fosslight_binary.binary_analysis
from flask import Flask, jsonify, request
import requests

from fosslight_binary._jar_analysis import analyze_jar_file
# from flask import json
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def test_post():
    file_paths = request.get_json()
    print(file_paths)
    a = file_paths["file_path"]
    print(a)
    output_file_name = 'test'
    formatt = 'excel'

    result = fosslight_binary.binary_analysis.find_binaries(path_to_find_bin=a, output_dir=a,
                                                            format=formatt)
    # M = dict(zip(range(len(result) + 1), result))
    # total = json.dumps(result)
    # result Tuple => str 변환
    json_str = json.dumps(result)

    # result Str => JSON??
    json_list = json.loads(json_str)

    # Excel Key 값
    key = ["Binary Name", "OSS Name", "OSS Version", "License", "Download Location", "Homepage", "Copyright Text",
           "Exclude", "Comment"]

    # Result 결과 값 넣을 변수 지정
    result_json = []

    # JSON 변환한 Result 값 반복문 실행
    for arr in json_list[1]:
        json_arr = {}
        # Result 결과 값을 하나씩 실행해서 Key, Value JSON 변환
        for idx, value in enumerate(arr):
            if len(key) > idx:
                json_arr[key[idx]] = value
        # JSON 값 Append
        result_json.append(json_arr)

    return jsonify({"result": result_json})


if __name__ == '__main__':
    app.run()
