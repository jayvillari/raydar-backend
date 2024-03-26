from flask import Flask
from flask import jsonify
from extractor import events
import datetime
import json

PORT = 105

app = Flask(__name__)


def obj_dict(obj):
    if isinstance(obj, datetime.date):
        return dict(year=obj.year, month=obj.month, day=obj.day)
    else:
        return obj.__dict__


json_string = json.dumps(events, default=obj_dict)


@app.route("/events/", methods=["GET"])
def get_events():
    events = {"results": json.loads(json_string)}
    return events


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
