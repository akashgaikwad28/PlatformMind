# Learning Loop

```mermaid
graph TD
    Exec[Execution Engine] --> Result[Execution Result]
    Result --> Learn[Learning Engine]
    
    Learn --> Metrics[Analyze Metrics (Time, Calls, Retries)]
    Learn --> Constraints[Extract Constraints]
    Learn --> Success[Calculate Success Rate]
    
    Metrics --> EMA[Update Exponential Moving Average]
    Success --> DB[Store in Learning Repository]
    Constraints --> DB
    
    DB --> MemEngine[Memory Engine]
    MemEngine --> Planner[Planner]
    Planner --> Exec
```
