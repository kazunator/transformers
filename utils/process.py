import json
import os
import re

o = os.environ["KV"]
o = json.loads(o)

from collections import Counter

data = """
 {
    "vit": {
        "single-gpu": [
            {
                "test": "tests/models/vit/test_modeling_vit.py::ViTModelTest::test_foo",
                "commit": "4b7de7cf31573a3b924c3473e1b8cc913cb0f63a",
                "pr_number": null,
                "author": "ydshieh",
                "merged_by": null
            },
            {
                "test": "tests/models/vit/test_modeling_vit.py::ViTModelTest::test_foo_2",
                "commit": "4b7de7cf31573a3b924c3473e1b8cc913cb0f63a",
                "pr_number": null,
                "author": "zucchini-nlp",
                "merged_by": null
            }
        ],
        "multi-gpu": []
    },
    "bert": {
        "single-gpu": [
            {
                "test": "tests/models/bert/test_modeling_bert.py::BertModelTest::test_foo",
                "commit": "4b7de7cf31573a3b924c3473e1b8cc913cb0f63a",
                "pr_number": null,
                "author": "ydshieh",
                "merged_by": null
            },
            {
                "test": "tests/models/bert/test_modeling_bert.py::BertModelTest::test_foo_3",
                "commit": "4b7de7cf31573a3b924c3473e1b8cc913cb0f63a",
                "pr_number": null,
                "author": "ydshieh",
                "merged_by": null
            }
        ],
        "multi-gpu": []
    },
    "gpt2": {
        "single-gpu": [
            {
                "test": "tests/models/gpt2/test_modeling_gpt2.py::GPT2ModelTest::test_foo_4",
                "commit": "4b7de7cf31573a3b924c3473e1b8cc913cb0f63a",
                "pr_number": null,
                "author": "zucchini-nlp",
                "merged_by": null
            },
            {
                "test": "tests/models/gpt2/test_modeling_gpt2.py::GPT2ModelTest::test_foo_5",
                "commit": "4b7de7cf31573a3b924c3473e1b8cc913cb0f63a",
                "pr_number": null,
                "author": "zucchini-nlp",
                "merged_by": null
            }
        ],
        "multi-gpu": []
    }
}
"""
data = json.loads(data)


# with open("new_model_failures_with_bad_commit.json") as fp:
#     data = json.load(fp)

# for model, model_result in data.items():
#     for device, failed_tests in model_result.items():
#         for failed_test in failed_tests:
#             author = failed_test["author"].replace("-", "_").upper() + "_SLACK_ID"
#             if author in o:
#                 author = o[author]
#             failed_test["author"] = f"<@{author}>"

# group `author` or `merged_by`

new_data = {}

for model, model_result in data.items():
    for device, failed_tests in model_result.items():
        for failed_test in failed_tests:
            author = failed_test["author"]

            # # TODO: we want to make it an internal member instead of checking it's in secrets
            # if not author.replace("-", "_").upper() + "_SLACK_ID" in o:
            #     author = failed_test["merged_by"]

            if author not in new_data:
                new_data[author] = Counter()

            model_name = failed_test["test"].split("/")[2]
            new_data[author].update([model_name])

for author in new_data:
    new_data[author] = dict(new_data[author])

output = {}
for author, item in new_data.items():
    key = author.replace("-", "_").upper() + "_SLACK_ID"
    if key in o:
        author = f"<@{o[key]}>"
    output[author] = item

print(json.dumps(output, indent=4).replace('"', '\\"').replace("\n", "\\n"))

