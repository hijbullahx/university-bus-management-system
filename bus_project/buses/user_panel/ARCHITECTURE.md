# User Panel Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        IUBAT BUS TRACKING SYSTEM                     │
│                         User Panel Architecture                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND LAYER                             │
│                     (user_map.html + JavaScript)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    HEADER SECTION                           │    │
│  │  • Title: "IUBAT Bus Tracker"                              │    │
│  │  • Route Selection Dropdown (Filter by route)              │    │
│  │  • Status Badge (Live/Simulation/No Buses)                 │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────────────────────────┐   │
│  │   SIDEBAR        │  │      MAP CONTAINER (Full Screen)      │   │
│  │   (Collapsible)  │  │                                        │   │
│  │                  │  │  • OpenStreetMap (Leaflet.js)         │   │
│  │  • Notifications │  │  • Bus Markers (Custom Icons)         │   │
│  │  • Quick Routes  │  │  • Popups (Enhanced Info)             │   │
│  │  • Toggle Button │  │  • Zoom/Pan Controls                  │   │
│  │                  │  │  • Follow Mode                        │   │
│  └──────────────────┘  └──────────────────────────────────────┘   │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    STATS BAR (Bottom)                       │    │
│  │  • Active Buses: 5  • Routes: 8  • Status: Online         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP Requests
                                    │ (Every 10 seconds)
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          API LAYER (Django)                          │
│                     /api/map-data/ Endpoint                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Function: bus_map_data(request)                                    │
│  Location: buses/api_views.py                                       │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ REQUEST PROCESSING                                          │   │
│  │  1. Parse route filter (optional)                           │   │
│  │  2. Query active buses (last 5 minutes)                     │   │
│  │  3. For each bus:                                           │   │
│  │     • Get current location                                  │   │
│  │     • Find next stop (time-based logic)                     │   │
│  │     • Calculate distance (Haversine formula)                │   │
│  │     • Calculate ETA (distance/speed)                        │   │
│  │  4. Build response JSON                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ RESPONSE FORMAT                                             │   │
│  │  {                                                          │   │
│  │    "buses": [                                               │   │
│  │      {                                                      │   │
│  │        "bus_id": 1,                                         │   │
│  │        "bus_number": "Bus-01",                              │   │
│  │        "route": "Mirpur - IUBAT",                           │   │
│  │        "latitude": 23.8859,                                 │   │
│  │        "longitude": 90.3971,                                │   │
│  │        "speed": 35.5,                                       │   │
│  │        "next_stop": "Main Gate",         ← NEW             │   │
│  │        "eta_minutes": 5,                 ← NEW             │   │
│  │        "distance_to_next_stop": 2.3,     ← NEW             │   │
│  │        "is_simulated": false                                │   │
│  │      }                                                      │   │
│  │    ],                                                       │   │
│  │    "total_active": 5,                                       │   │
│  │    "routes": [...]                        ← NEW             │   │
│  │  }                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Django ORM Queries
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER (Models)                       │
│                         PostgreSQL / SQLite                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │   BusRoute       │  │   BusLocation    │  │   Stopage       │  │
│  │                  │  │                  │  │                 │  │
│  │ • id             │  │ • bus (FK)       │  │ • route (FK)    │  │
│  │ • bus_number     │  │ • latitude       │  │ • name          │  │
│  │ • route          │  │ • longitude      │  │ • pickup_time   │  │
│  │ • is_shuttle     │  │ • speed          │  │                 │  │
│  │                  │  │ • timestamp      │  └─────────────────┘  │
│  │                  │  │ • is_active      │                       │
│  │                  │  │ • is_simulated   │  ┌─────────────────┐  │
│  │                  │  │ • driver (FK)    │  │ Notification    │  │
│  └──────────────────┘  └──────────────────┘  │                 │  │
│                                                │ • title         │  │
│                                                │ • message       │  │
│                                                │ • is_active     │  │
│                                                │ • priority      │  │
│                                                └─────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW DIAGRAM                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. USER ACTION                                                      │
│     └─→ Opens page or clicks bus icon                               │
│                                                                       │
│  2. FRONTEND JAVASCRIPT                                              │
│     └─→ fetch('/api/map-data/?route=1')  (every 10 seconds)        │
│                                                                       │
│  3. DJANGO VIEW (api_views.py)                                       │
│     ├─→ Parse request parameters                                    │
│     ├─→ Query BusLocation (last 5 min)                              │
│     ├─→ Query Stopage (for each bus)                                │
│     ├─→ Calculate distance (Haversine)                              │
│     ├─→ Calculate ETA (distance/speed)                              │
│     └─→ Return JSON response                                        │
│                                                                       │
│  4. FRONTEND UPDATES                                                 │
│     ├─→ Update/create markers on map                                │
│     ├─→ Update popup content                                        │
│     ├─→ Update stats bar                                            │
│     ├─→ Apply follow mode (if active)                               │
│     └─→ Show status badge                                           │
│                                                                       │
│  5. USER SEES                                                        │
│     └─→ Real-time bus positions with ETA                            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    KEY FEATURES & FUNCTIONS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Frontend JavaScript Functions:                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ • updateBusLocations()      → Fetches data every 10s       │    │
│  │ • createBusIcon()           → Custom bus markers           │    │
│  │ • createPopupContent()      → Enhanced popup HTML          │    │
│  │ • toggleFollowBus(id)       → Follow/unfollow logic        │    │
│  │ • filterAndFocusRoute(id)   → Route filtering              │    │
│  │ • toggleSidebar()           → Show/hide sidebar            │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  Backend Functions:                                                  │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ • calculate_distance()      → Haversine formula            │    │
│  │ • find_next_stop()          → Time-based stop detection    │    │
│  │ • calculate_eta()           → ETA calculation              │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                     TECHNOLOGY STACK                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Frontend:                                                           │
│  • HTML5 + CSS3 (Responsive design)                                 │
│  • JavaScript (Vanilla ES6+)                                        │
│  • Leaflet.js 1.9.4 (Map library)                                   │
│  • OpenStreetMap (Map tiles)                                        │
│                                                                       │
│  Backend:                                                            │
│  • Django 4.2+ (Web framework)                                      │
│  • Django REST Framework (API)                                      │
│  • Python 3.9+ (Language)                                           │
│  • PostgreSQL / SQLite (Database)                                   │
│                                                                       │
│  Infrastructure:                                                     │
│  • WSGI Server (Gunicorn recommended)                               │
│  • Nginx (Reverse proxy)                                            │
│  • CDN for static files (optional)                                  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                  SECURITY & PERFORMANCE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Security:                                                           │
│  ✓ No authentication required (public service)                      │
│  ✓ Read-only API endpoints                                          │
│  ✓ Input validation on filters                                      │
│  ✓ CSRF protection on forms                                         │
│  ✓ SQL injection prevention (ORM)                                   │
│                                                                       │
│  Performance:                                                        │
│  ✓ Database query optimization                                      │
│  ✓ Efficient marker reuse                                           │
│  ✓ Lazy loading                                                     │
│  ✓ Caching (Django cache framework)                                 │
│  ✓ CDN for static assets                                            │
│  ✓ Async API calls                                                  │
│  ✓ Minimal DOM manipulations                                        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                       LEGEND & SYMBOLS
═══════════════════════════════════════════════════════════════════════
 → : Data flow / Process flow
 ↓ : Downward flow
 FK: Foreign Key relationship
 ✓ : Implemented / Checked
 ← : New feature indicator
 • : List item / Feature point
═══════════════════════════════════════════════════════════════════════
