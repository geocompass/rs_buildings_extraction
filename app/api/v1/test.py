from app.libs.redprint import Redprint
api = Redprint('test')


@api.route('', methods=['GET'])
# @auth.login_required
def get_test():
    return "testttt"
