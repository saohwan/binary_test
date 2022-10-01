import json

import fosslight_binary.binary_analysis
import requests
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/', methods=['POST'])
def test_post():
    request_api = request.get_json()
    binary_dir = request_api["file_path"]
    format_set = request_api["output_dir"]
    result = fosslight_binary.binary_analysis.find_binaries(path_to_find_bin=binary_dir, output_dir=binary_dir,
                                                            format=format_set)

    # result Tuple = > str 변환
    json_str = json.dumps(result)

    # result Str => JSON??
    json_list = json.loads(json_str)

    # result 값에는 success (boolean) 값이 존재, 해당 값은 불 필요한 결과 값이기 때문에 제거.
    del json_list[0]

    rows = json_list[0]

    # Excel Key 값
    keys = ["Binary Name", "OSS Name", "OSS Version", "License", "Download Location", "Homepage", "Copyright Text",
            "Exclude", "Comment"]

    # zip은 두 순회가능한 객체에서 짧은 횟수만큼만 순회
    result_json = [dict(zip(keys, row)) for row in rows]

    result_data = []
    for info in result_json:
        # vulnerability_data = rest_api 호출

        # print(vulnerability_data)

        # print(info['OSS Name'])
        if len(info['OSS Name']) == 0:
            continue
        idx = info['OSS Name'].find(':')
        if idx < 0:
            idx = 0
        data = {
            'ossName': info['OSS Name'][idx + 1:],
            # 'ossName2': re.sub(r'\:.*$', info['OSS Name']),
            'ossVersion': info['OSS Version'],
            # vulnability_data = info['Vulnerability']
        }

        print(data)

        api_key_id = '_token'
        api_key_secret = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5AZm9zc2xpZ2h0Lm9yZyJ9.3jWpmXwz73emxQ6tYjf1nkecLK3Br6Jth08trgF-gxQ'
        header = {
            '_token': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5AZm9zc2xpZ2h0Lm9yZyJ9.3jWpmXwz73emxQ6tYjf1nkecLK3Br6Jth08trgF-gxQ'}

        vulnerability_data = requests.post("https://demo.fosslight.org/api/v1/vulnerability_max_data", headers=header,
                                           params=data)

        print(vulnerability_data)
        data['vulnerabilityData'] = vulnerability_data

        result_data.append(data)

    print(result_data)

    # del result_json[0]

    # a = jsonify(result_json)

    # b_val = [e["OSS Name"] for e in result_json]
    #
    # print(b_val)
    #
    # name_key = ["ossName"]
    # # for res in b_val:
    # #     print(res)
    #
    # # sum_val = [dict(zip(name_key, res)) for res in b_val]
    # sum_val = [dict(zip(name_key, b_val))]
    # print(sum_val)

    # return b_val

    return jsonify(result_data)


if __name__ == '__main__':
    app.run()