import json

import fosslight_binary.binary_analysis
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

    del json_list[0]

    rows = json_list[0]
    # Excel Key 값
    keys = ["Binary Name", "OSS Name", "OSS Version", "License", "Download Location", "Homepage", "Copyright Text",
            "Exclude", "Comment"]

    result_json = [dict(zip(keys, row)) for row in rows]

    # del result_json[0]

    return jsonify(result_json)


if __name__ == '__main__':
    app.run()
