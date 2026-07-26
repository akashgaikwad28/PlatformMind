# Clean Architecture

```mermaid
graph TD
    subgraph Infrastructure Layer
        SQLite["SQLite DB"]
        Chroma["ChromaDB"]
        GitHub["GitHub API"]
        LLM["LLM Provider (Groq)"]
    end

    subgraph API Layer
        FastAPI["FastAPI App"]
        Router["Routers"]
        DI["Container"]
    end

    subgraph Application Layer
        Planner["Planner"]
        ExecEngine["Execution Engine"]
        Memory["Memory Engine"]
        Learn["Learning Engine"]
        Interfaces["Interfaces (Ports)"]
    end

    subgraph Domain Layer
        Models["Models (Instruction, Result)"]
        VO["Value Objects"]
        Exceptions["Domain Exceptions"]
    end

    API Layer --> Application Layer
    Infrastructure Layer --> Application Layer
    Application Layer --> Domain Layer
    
    %% Dependency Inversion
    Application Layer -. "Defines" .-> Interfaces
    Infrastructure Layer -. "Implements" .-> Interfaces
```
