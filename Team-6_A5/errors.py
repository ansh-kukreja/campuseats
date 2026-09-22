from flask import jsonify

class ProblemError(Exception):
    def __init__(self, status, title, detail, kind="bad-request", extra_headers=None):
        self.status=status; self.title=title; self.detail=detail; self.kind=kind; self.extra_headers=extra_headers or {}
        super().__init__(detail)

def problem(status, title, detail, kind="bad-request", extra_headers=None):
    body={"type":f"https://campuseats.example.com/problems/{kind}","title":title,"status":status,"detail":detail}
    response=jsonify(body); response.status_code=status; response.content_type="application/problem+json"
    for k,v in (extra_headers or {}).items(): response.headers[k]=v
    return response
