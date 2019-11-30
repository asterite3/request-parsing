import os
import json
import glob
import difflib

from parse import parse

def convert_primitive(x):
    if not isinstance(x, dict) or 'type' not in x:
        return x
    t = x['type']
    is_correct_primitive_type = \
        t == 'string' and isinstance(x['value'], basestring) or \
        t == 'number' and isinstance(x['value'], (int, long, float)) or \
        (t == 'bool' or t == 'boolean') and isinstance(x['value'], bool) or \
        t == 'array' and isinstance(x['value'], list)
    if is_correct_primitive_type:
        return x['value']
    return x


def deep_compare(a, b):
    a = convert_primitive(a)
    b = convert_primitive(b)

    if a == b:
        return True

    if type(a) != type(b):
        return False

    if isinstance(a, dict):
        for k, v in a.iteritems():
            if k not in b:
                return False
            if not deep_compare(a[k], b[k]):
                return False
        return True
    elif isinstance(a, list):
        if len(a) != len(b):
            return False
        for idx, el in enumerate(a):
            if not deep_compare(el, b[idx]):
                return False
        return True
    return False



def check_same_parsing(req, correct):
    parsed = parse(req)
    return deep_compare(parsed, correct), parsed

def jsondiff(a, b):
    a_json_lines = json.dumps(a, sort_keys=True, indent=4).splitlines()
    b_json_lines = json.dumps(b, sort_keys=True, indent=4).splitlines()
    return '\n'.join(difflib.context_diff(a_json_lines, b_json_lines))

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

    tests = sorted([
        {"fname": fname, "num": int(os.path.basename(fname).split('.')[0])}
        for fname in glob.glob("samples/*.request")
    ], key=lambda test: test["num"])

    for test in tests:
        all_ok = True
        test_fname = test["fname"]
        print "test", test_fname, "...",
        with open("samples/parsed/%d.json" % test["num"]) as parsed_test_file:
            correct_parsing = json.load(parsed_test_file)
        with open(test_fname) as request_file:
            request = request_file.read()
        same, parsed = check_same_parsing(request, correct_parsing)
        if same:
            print "OK"
        else:
            print "parsing differed:", jsondiff(parsed, correct_parsing)
            all_ok = False
            break
    if all_ok:
        print "ALL OK"