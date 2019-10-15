from app.libs.redprint import Redprint
api = Redprint('test')


@api.route('', methods=['GET'])
def get_test():
    return "testttt"


@api.route('/1', methods=['GET'])
def get_tt():
    return "ddddd"
