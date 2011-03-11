import simplejson

def load_conf(file_path):
    fp = open(file_path, 'r')
    data = fp.read()
    fp.close()

    return simplejson.loads(data)

