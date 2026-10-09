# System Architecture

```text
                +----------------------+
                |   Emergency Form     |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | ML Priority Model     |
                | Random Forest         |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Priority Queue        |
                | Heap / DSA            |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Resource Manager      |
                | Type + nearest unit   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Graph + Dijkstra      |
                | Shortest route        |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Flask Result / SQLite |
                +----------------------+
```
