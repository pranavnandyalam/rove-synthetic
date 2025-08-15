# Rove Synthetic - System Flowchart

## Complete System Architecture

```mermaid
graph TB
    %% User Interface Layer
    subgraph "User Interface"
        UI[User Browser]
        FORM[Input Form]
        RESULTS[Results Display]
        FEEDBACK[Feedback Form]
    end

    %% Web Layer
    subgraph "Flask Web Application"
        APP[app.py]
        ROUTES[Route Handlers]
        TEMPLATES[Jinja2 Templates]
    end

    %% Business Logic Layer
    subgraph "Business Logic"
        REC[recommender.py]
        ROUTING[routing.py]
        VCALC[value_calc.py]
    end

    %% Data Access Layer
    subgraph "Data Access"
        API[reference.py]
        DB[sql_lite.py]
        MOCK[Mock Data]
    end

    %% External Systems
    subgraph "External Systems"
        AMADEUS[Amadeus API]
        SQLITE[(SQLite Database)]
    end

    %% User Flow
    UI --> FORM
    FORM --> APP
    APP --> ROUTES
    ROUTES --> REC
    
    %% Recommendation Flow
    REC --> ROUTING
    ROUTING --> API
    API --> AMADEUS
    
    %% Fallback Flow
    ROUTING --> MOCK
    MOCK --> ROUTING
    
    %% Value Calculation
    ROUTING --> VCALC
    VCALC --> REC
    
    %% Response Flow
    REC --> ROUTES
    ROUTES --> TEMPLATES
    TEMPLATES --> RESULTS
    RESULTS --> UI
    
    %% Feedback Flow
    UI --> FEEDBACK
    FEEDBACK --> APP
    APP --> DB
    DB --> SQLITE
    
    %% Styling with better contrast
    classDef webLayer fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#0d47a1
    classDef businessLayer fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c
    classDef dataLayer fill:#e8f5e8,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    classDef externalLayer fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100
    
    class APP,ROUTES,TEMPLATES webLayer
    class REC,ROUTING,VCALC businessLayer
    class API,DB,MOCK dataLayer
    class AMADEUS,SQLITE externalLayer
```

## Detailed User Journey Flow

```mermaid
flowchart TD
    START([User visits website]) --> LOAD[Load homepage with examples]
    LOAD --> FORM{User fills form?}
    
    FORM -->|No| WAIT[Wait for user input]
    WAIT --> FORM
    
    FORM -->|Yes| VALIDATE[Validate form data]
    VALIDATE --> VALID{Valid input?}
    
    VALID -->|No| ERROR[Show validation error]
    ERROR --> FORM
    
    VALID -->|Yes| SEARCH[Search for recommendations]
    SEARCH --> API_CALL[Call Amadeus API]
    
    API_CALL --> API_SUCCESS{API success?}
    
    API_SUCCESS -->|No| MOCK_DATA[Use mock flight data]
    API_SUCCESS -->|Yes| REAL_DATA[Use real flight data]
    
    MOCK_DATA --> PROCESS
    REAL_DATA --> PROCESS
    
    PROCESS[Process flight offers] --> CALC_VPM[Calculate value-per-mile]
    CALC_VPM --> ADD_COMPARATORS[Add hotel & gift card comparators]
    ADD_COMPARATORS --> RANK[Rank by value-per-mile]
    RANK --> DISPLAY[Display recommendations]
    
    DISPLAY --> USER_RATE{User provides feedback?}
    
    USER_RATE -->|No| END([Session ends])
    USER_RATE -->|Yes| SAVE_FEEDBACK[Save feedback to database]
    SAVE_FEEDBACK --> FLASH[Show thank you message]
    FLASH --> END
    
    %% Styling with better contrast and readability
    classDef startEnd fill:#2e7d32,stroke:#1b5e20,stroke-width:3px,color:#ffffff,font-weight:bold
    classDef process fill:#1976d2,stroke:#0d47a1,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef decision fill:#f57c00,stroke:#e65100,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef data fill:#7b1fa2,stroke:#4a148c,stroke-width:2px,color:#ffffff,font-weight:bold
    
    class START,END startEnd
    class LOAD,SEARCH,PROCESS,CALC_VPM,ADD_COMPARATORS,RANK,DISPLAY,SAVE_FEEDBACK,FLASH process
    class FORM,VALID,API_SUCCESS,USER_RATE decision
    class MOCK_DATA,REAL_DATA data
```

## Data Processing Flow

```mermaid
flowchart LR
    subgraph "Input Data"
        ORIGIN[Origin Airport]
        DEST[Destination Airport]
        DATE[Departure Date]
        MILES[Miles Available]
    end
    
    subgraph "API Processing"
        AUTH[OAuth2 Authentication]
        SEARCH[Flight Search]
        PARSE[Parse Response]
    end
    
    subgraph "Business Logic"
        VPM[Value Per Mile Calc]
        RANK[Ranking Algorithm]
        FILTER[Affordability Filter]
    end
    
    subgraph "Output Data"
        FLIGHT_RECS[Flight Recommendations]
        HOTEL_COMP[Hotel Comparison]
        GIFT_COMP[Gift Card Comparison]
    end
    
    ORIGIN --> AUTH
    DEST --> AUTH
    DATE --> AUTH
    MILES --> VPM
    
    AUTH --> SEARCH
    SEARCH --> PARSE
    PARSE --> VPM
    VPM --> RANK
    RANK --> FILTER
    FILTER --> FLIGHT_RECS
    FILTER --> HOTEL_COMP
    FILTER --> GIFT_COMP
    
    %% Styling with better contrast
    classDef input fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:#01579b,font-weight:bold
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c,font-weight:bold
    classDef output fill:#e8f5e8,stroke:#388e3c,stroke-width:2px,color:#1b5e20,font-weight:bold
    
    class ORIGIN,DEST,DATE,MILES input
    class AUTH,SEARCH,PARSE,VPM,RANK,FILTER process
    class FLIGHT_RECS,HOTEL_COMP,GIFT_COMP output
```

## Error Handling Flow

```mermaid
flowchart TD
    REQUEST[User Request] --> TRY_API[Try API Call]
    
    TRY_API --> API_ERROR{API Error?}
    API_ERROR -->|No| SUCCESS[Process Real Data]
    API_ERROR -->|Yes| CHECK_CREDS{API Credentials?}
    
    CHECK_CREDS -->|Missing| USE_MOCK[Use Mock Data]
    CHECK_CREDS -->|Invalid| USE_MOCK
    CHECK_CREDS -->|Network Error| USE_MOCK
    
    USE_MOCK --> LOG_ERROR[Log Error]
    LOG_ERROR --> SUCCESS
    
    SUCCESS --> VALIDATE_DATA{Data Valid?}
    VALIDATE_DATA -->|No| SHOW_ERROR[Show Error Message]
    VALIDATE_DATA -->|Yes| PROCESS[Process Data]
    
    PROCESS --> CALC_ERROR{Calculation Error?}
    CALC_ERROR -->|Yes| SHOW_ERROR
    CALC_ERROR -->|No| DISPLAY[Display Results]
    
    SHOW_ERROR --> REQUEST
    
    %% Styling with better contrast
    classDef error fill:#ffcdd2,stroke:#d32f2f,stroke-width:3px,color:#b71c1c,font-weight:bold
    classDef success fill:#c8e6c9,stroke:#388e3c,stroke-width:2px,color:#1b5e20,font-weight:bold
    classDef process fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#0d47a1,font-weight:bold
    
    class API_ERROR,CHECK_CREDS,VALIDATE_DATA,CALC_ERROR error
    class SUCCESS,PROCESS,DISPLAY success
    class TRY_API,USE_MOCK,LOG_ERROR process
```

## File Dependencies Flow

```mermaid
graph TD
    subgraph "Entry Points"
        MAIN[main.py]
        APP[app.py]
        TEST[test_requirements.py]
    end
    
    subgraph "Core Modules"
        REC[recommender.py]
        ROUTING[routing.py]
        VCALC[value_calc.py]
        REF[reference.py]
        DB[sql_lite.py]
    end
    
    subgraph "Templates"
        LAYOUT[templates/layout.html]
        INDEX[templates/index.html]
    end
    
    subgraph "Configuration"
        ENV[.env]
        REQ[requirements.txt]
    end
    
    %% Dependencies
    MAIN --> REF
    MAIN --> ROUTING
    
    APP --> REC
    APP --> DB
    APP --> VCALC
    APP --> LAYOUT
    APP --> INDEX
    
    REC --> ROUTING
    REC --> VCALC
    
    ROUTING --> REF
    ROUTING --> VCALC
    
    TEST --> VCALC
    TEST --> REC
    TEST --> APP
    
    APP --> ENV
    MAIN --> ENV
    
    %% Styling with better contrast
    classDef entry fill:#fff8e1,stroke:#f57c00,stroke-width:2px,color:#e65100,font-weight:bold
    classDef core fill:#e8f5e8,stroke:#388e3c,stroke-width:2px,color:#1b5e20,font-weight:bold
    classDef template fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c,font-weight:bold
    classDef config fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:#01579b,font-weight:bold
    
    class MAIN,APP,TEST entry
    class REC,ROUTING,VCALC,REF,DB core
    class LAYOUT,INDEX template
    class ENV,REQ config
```

## Value Calculation Flow

```mermaid
flowchart TD
    INPUT[Cash Price & Miles] --> CALC[Calculate VPM]
    
    CALC --> FLIGHT{Redemption Type?}
    FLIGHT -->|Flight| FLIGHT_CPM[1.3¢/mi]
    FLIGHT -->|Hotel| HOTEL_CPM[0.7¢/pt]
    FLIGHT -->|Gift Card| GIFT_CPM[0.5¢/pt]
    
    FLIGHT_CPM --> FLIGHT_CALC[VPM = Price - Taxes / Miles]
    HOTEL_CPM --> HOTEL_CALC[VPM = Price / Points]
    GIFT_CPM --> GIFT_CALC[VPM = Face Value / Points]
    
    FLIGHT_CALC --> RANK[Rank by VPM]
    HOTEL_CALC --> RANK
    GIFT_CALC --> RANK
    
    RANK --> AFFORDABLE{Affordable with user's miles?}
    AFFORDABLE -->|Yes| SHOW[Show in recommendations]
    AFFORDABLE -->|No| HIDE[Hide from affordable list]
    
    SHOW --> OUTPUT[Display Results]
    HIDE --> OUTPUT
    
    %% Styling with better contrast
    classDef input fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:#01579b,font-weight:bold
    classDef calc fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c,font-weight:bold
    classDef output fill:#e8f5e8,stroke:#388e3c,stroke-width:2px,color:#1b5e20,font-weight:bold
    
    class INPUT input
    class CALC,FLIGHT_CPM,HOTEL_CPM,GIFT_CPM,FLIGHT_CALC,HOTEL_CALC,GIFT_CALC,RANK calc
    class SHOW,HIDE,OUTPUT output
``` 