# LangSmith Screenshot Capture Guide

Use this after Phase 5 eval passes locally. LangSmith tracing must be enabled in `.env`:

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key
LANGCHAIN_PROJECT=sungrid-support-agent
```

## Steps

1. Run eval for LangSmith traces (VS Code: open `scripts/run_evaluation.py`, or use `--cases 1,3`):
   ```powershell
   .\.venv\Scripts\python scripts\run_evaluation.py --cases 1,3
   ```

2. Open https://smith.langchain.com and select project **sungrid-support-agent**.

3. Open the two most recent runs:
   - **Warranty trace:** question about 35% production / warranty (Case 1)
   - **Safety trace:** burning smell near inverter (Case 3)

4. For each trace, screenshot showing:
   - Full node chain: classify → retrieve → generate → validate → risk → format
   - Retrieved documents / inputs panel (if visible)
   - Run metadata (project name, latency)

5. Save as:
   - `assets/langsmith_trace_warranty.png`
   - `assets/langsmith_trace_safety.png`

These images will be embedded in the Phase 7 README.
