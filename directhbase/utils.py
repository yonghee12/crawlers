from happybase.util import ensure_bytes
import happybase
import pickle


def isinstances(object, classinfos: list):
    inspection = [isinstance(object, c) for c in classinfos]
    return any(inspection)


def convert_set_type(value):
    if isinstance(value, str):
        return value
    else:
        return pickle.dumps(value)


def convert_set_mapping_dic(dic):
    new_dic = {}
    for k, v in dic.items():
        new_dic[k] = convert_set_type(v)
    return new_dic


def convert_get_mapping_dic(dic):
    new_dic = {}
    for k, v in dic.items():
        new_dic[convert_get_type(k)] = convert_get_type(v)
    return new_dic


def convert_get_type(encoded, force_decode=False):
    if encoded is None:
        return None
    else:
        if force_decode:
            try:
                return pickle.loads(encoded)
            except Exception as e:
                print(e)
                try:
                    return encoded.decode("utf-8")
                except Exception as e:
                    print(e)
                    return encoded
        else:
            try:
                return encoded.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    return pickle.loads(encoded)
                except Exception as e:
                    print(e)
                    return encoded
