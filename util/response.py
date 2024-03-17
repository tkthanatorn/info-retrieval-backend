from fastapi import Response
import json


def response(
    status_code: int,
    result: any,
    msg: Exception | str | None,
) -> Response:
    content = dict()
    if status_code == 200 or status_code == 201:
        content["success"] = True
        content["result"] = result
        content["msg"] = "ok"
    else:
        content["success"] = False
        content["msg"] = str(msg)

    return Response(
        status_code=status_code,
        content=json.dumps(content),
        media_type="application/json",
    )
