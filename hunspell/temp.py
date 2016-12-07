import json_processor as jp
import pprint

a = jp.get_all_entries()
result = []
for k, v in a.items():
    if ")" in k.trunk:
        result.append(k.trunk)
    if k.twig and ")" in k.twig:
        result.append(k.twig)
pprint.pprint (sorted(list(set(result))))
