from fastapi import FastAPI, Request
from analyzer.parser import parse_code
from analyzer.analyzer import ComplexityAnalyzer

app = FastAPI()

@app.post("/analyze")
async def analyze_code(request: Request):
    data = await request.json()
    code = data.get("code")
    if not code:
        return {"error": "Missing code"}

    try:
        tree = parse_code(code)
        analyzer = ComplexityAnalyzer()
        time, space = analyzer.analyze(tree)
        return {"time_complexity": time, "space_complexity": space}
    except Exception as e:
        return {"error": str(e)}
