# Architecture and review workflow

```mermaid
flowchart LR
    S[Versioned synthetic source pack] --> D[Deterministic case assembly]
    D --> A[Allowlisted numbered source lines]
    A --> L[Bounded model request]
    L --> J[Strict JSON draft]
    J --> V[Exact citation and structural checks]
    V --> P[Pending independent semantic review]
    D --> G[Deterministic authority and hold guards]
    G --> H[Human-controlled assessment]
    P --> H
    H --> Q[Quality and effort measurement]
    Q --> ROI[Deterministic ROI inputs]
```

```mermaid
flowchart TD
    I[Select case] --> E[Inspect facts and source lines]
    E --> C[Validate source version and checks]
    C --> U{Unresolved source authority or scope?}
    U -->|Yes| HOLD[Hold: designated specialist or case owner]
    U -->|No| R[Human evidence assessment]
    HOLD --> N[New validated evidence and controlled version update required]
    R --> S{All required confirmations established?}
    S -->|No| HOLD
    S -->|Yes| READY[Ready for authorized human decision]
    READY --> STOP[Local demo stops: no execution or financial decision]
```

The source-specific controls are explicit authored rules grounded in visible packets. They are not model outputs or hidden answer keys. They never enter model generation context. Publication of these controls makes this a transparent development demonstration, not a blind benchmark. An independent evaluator must freeze their private case assessment before reviewing later live output.

The broader operating-model artifact describes future authorized execution stages. The implemented workbench deliberately ends at evidence assessment. Hashes detect changes against local manifests; they are not digital signatures or a production trust service.
