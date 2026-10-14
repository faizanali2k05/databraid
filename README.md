# databraid

Record lightweight, serializable lineage edges without adopting a full data platform.

```bash
python -m pip install databraid
```

```python
from databraid import Lineage

lineage = Lineage()
lineage.add("feature_table:v2", ["events:raw", "users:clean"], "join", metadata={"job": "daily"})
payload = lineage.as_dicts()
```

The in-memory log is dependency-free, thread-safe, serializable, and accepts a clock function for reproducible pipelines. It records metadata only; it does not inspect or copy the underlying datasets.
