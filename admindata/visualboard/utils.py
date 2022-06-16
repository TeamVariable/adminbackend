from rest_framework.response import Response


def msg_ok(status: int=200):
    return Response({"msg": "ok"}, status=status)