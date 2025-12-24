# Sonos Cloud Control Panel - Frontend Plan

## Overview

Build a modern web-based control panel to manage the Sonos venue audio system, including commercials, programs, scheduling, and real-time playback control. Host on Render with a Flask/FastAPI backend.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         RENDER.COM                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │  React Frontend │───▶│  Python Backend (FastAPI)           │ │
│  │  (Static Build) │    │  - Schedule API                     │ │
│  └─────────────────┘    │  - Playback Control API             │ │
│                         │  - Speaker Management API            │ │
│                         │  - Commercial/Program API            │ │
│                         └──────────────┬──────────────────────┘ │
└────────────────────────────────────────┼────────────────────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Sonos Control API  │
                              │   (api.sonos.com)    │
                              └──────────────────────┘
```

---

## Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query + Zustand
- **UI Components**: Shadcn/ui (modern, accessible)
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (Python)
- **Scheduler**: APScheduler (replaces `schedule` library)
- **Database**: SQLite (for schedule persistence)
- **Authentication**: Simple API key or JWT

### Deployment
- **Host**: Render.com
- **Frontend**: Static Site
- **Backend**: Web Service (Python)

---

## Current Schedule Reference

Based on your existing `scheduler.py`, here's the current schedule that will be pre-loaded:

### Weekly Schedule Overview

| Day       | AM Block      | DAY Block     | PM_FIRE Block |
|-----------|---------------|---------------|---------------|
| Monday    | 00:00 - 02:00 | 12:00 - 17:30 | 17:45 - 23:00 |
| Tuesday   | 00:00 - 02:00 | 11:00 - 17:30 | 17:45 - 23:00 |
| Wednesday | 00:00 - 02:00 | 11:00 - 17:30 | 17:45 - 23:00 |
| Thursday  | 00:00 - 02:00 | 11:00 - 17:30 | 17:45 - 23:00 |
| Friday    | 00:00 - 04:00 | 11:00 - 17:30 | 17:45 - 23:00 |
| Saturday  | 00:00 - 04:00 | 11:00 - 15:45 | 16:10 - 23:00 |
| Sunday    | 00:00 - 02:00 | 11:00 - 17:30 | 17:45 - 23:00 |

### Content Types
- **ad** - Advertisements/Commercials
- **adfire** - Fire Show Advertisements
- **fm** - Music Programming
- **sm** - Sustained Music
- **parking** - Parking Announcements
- **fireparking** - Fire Show Parking Announcements
- **TIGS** - Special Programs
- **pause** - Stop Playback

### Volume Levels
50, 65, 70, 75, 80, 85, 90, 95 (used as prefixes to content types)

---

## Frontend Pages & Features

### 1. Dashboard (Home)
```
┌──────────────────────────────────────────────────────────────┐
│  SONOS CLOUD CONTROL                          [Status: Live] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  NOW PLAYING    │  │  NEXT UP        │  │  SPEAKERS    │ │
│  │  ─────────────  │  │  ─────────────  │  │  ──────────  │ │
│  │  85fm           │  │  65ad @ 14:15   │  │  9/9 Online  │ │
│  │  Volume: 85     │  │  Ads Block      │  │  All Grouped │ │
│  │  [Pause] [Skip] │  │                 │  │              │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  TODAY'S SCHEDULE - Thursday                           │ │
│  │  ────────────────────────────────────────────────────  │ │
│  │  [Timeline visualization with current time marker]     │ │
│  │  00:00 ═══ 02:00    11:00 ════════════ 17:30    17:45 ═│ │
│  │   AM Block           DAY Block              PM_FIRE    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  QUICK ACTIONS                                         │ │
│  │  [▶ Play] [⏸ Pause All] [🔊 Set Volume] [🔄 Refresh]   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### 2. Schedule Manager
```
┌──────────────────────────────────────────────────────────────┐
│  WEEKLY SCHEDULE                                             │
├──────────────────────────────────────────────────────────────┤
│  [Monday] [Tuesday] [Wednesday] [Thursday] [Friday] [Sat/Sun]│
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  THURSDAY SCHEDULE                      [+ Add Slot]   │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  TIME     │ PROGRAM  │ VOLUME │ TYPE      │ ACTIONS    │ │
│  │  ─────────┼──────────┼────────┼───────────┼─────────── │ │
│  │  11:00    │ 75parking│   75   │ Parking   │ [Edit][Del]│ │
│  │  11:15    │ 85TIGS   │   85   │ TIGS      │ [Edit][Del]│ │
│  │  11:30    │ 70ad     │   70   │ Ad        │ [Edit][Del]│ │
│  │  11:45    │ 65fm     │   65   │ Music     │ [Edit][Del]│ │
│  │  12:00    │ 75ad     │   75   │ Ad        │ [Edit][Del]│ │
│  │  ...      │ ...      │  ...   │ ...       │    ...     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  [Save Changes] [Reset to Default] [Export Schedule]         │
└──────────────────────────────────────────────────────────────┘
```

### 3. Program Library
```
┌──────────────────────────────────────────────────────────────┐
│  PROGRAM LIBRARY                              [+ New Program]│
├──────────────────────────────────────────────────────────────┤
│  Filter: [All ▼] [Ads] [Music] [Parking] [TIGS] [Fire]      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  ADVERTISEMENTS (ad)                                   │ │
│  │  ──────────────────────────────────────────────────── │ │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │ │
│  │  │ 50ad │ │ 65ad │ │ 70ad │ │ 75ad │ │ 85ad │ ...    │ │
│  │  │ Vol50│ │ Vol65│ │ Vol70│ │ Vol75│ │ Vol85│        │ │
│  │  │[Play]│ │[Play]│ │[Play]│ │[Play]│ │[Play]│        │ │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘        │ │
│  │                                                        │ │
│  │  MUSIC (fm)                                            │ │
│  │  ──────────────────────────────────────────────────── │ │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │ │
│  │  │ 50fm │ │ 65fm │ │ 70fm │ │ 75fm │ │ 85fm │ ...    │ │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘        │ │
│  │                                                        │ │
│  │  PARKING ANNOUNCEMENTS (parking)                       │ │
│  │  ──────────────────────────────────────────────────── │ │
│  │  ...                                                   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### 4. Speaker Control
```
┌──────────────────────────────────────────────────────────────┐
│  SPEAKER MANAGEMENT                          [Refresh Status]│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    VENUE LAYOUT                         ││
│  │                                                         ││
│  │        [LEFT_POLE_01]    [CENTER_POLE]   [RIGHT_POLE_01]││
│  │             ●                 ●               ●         ││
│  │                                                         ││
│  │        [LEFT_POLE_02]       [STAGE]      [RIGHT_POLE_02]││
│  │             ●                 ●               ●         ││
│  │                                                         ││
│  │        [LEFT_POLE_03]  [BATHROOM_DOORS]  [RIGHT_POLE_03]││
│  │             ●                 ●               ●         ││
│  │                                                         ││
│  │        ● = Online/Grouped                               ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  INDIVIDUAL CONTROLS                                    ││
│  │  ───────────────────────────────────────────────────── ││
│  │  Speaker          │ Status │ Volume │ Actions          ││
│  │  RIGHT_POLE_03    │ ●      │ ████░░ │ [Solo] [Mute]    ││
│  │  RIGHT_POLE_01    │ ●      │ ████░░ │ [Solo] [Mute]    ││
│  │  RIGHT_POLE_02    │ ●      │ ████░░ │ [Solo] [Mute]    ││
│  │  ...              │        │        │                  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  [Group All] [Ungroup All] [Set Master Volume: ████░░ 75]   │
└──────────────────────────────────────────────────────────────┘
```

### 5. Favorites/Playlists
```
┌──────────────────────────────────────────────────────────────┐
│  SONOS FAVORITES                              [Refresh List] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  ID  │ NAME                    │ TYPE     │ ACTIONS    │ │
│  │  ────┼─────────────────────────┼──────────┼─────────── │ │
│  │  28  │ Opening Announcement    │ Playlist │ [▶ Play]   │ │
│  │  29  │ Parking Reminder        │ Playlist │ [▶ Play]   │ │
│  │  30  │ Commercial Block A      │ Playlist │ [▶ Play]   │ │
│  │  31  │ Commercial Block B      │ Playlist │ [▶ Play]   │ │
│  │  32  │ Background Music Mix    │ Playlist │ [▶ Play]   │ │
│  │  33  │ Main Music Rotation     │ Playlist │ [▶ Play]   │ │
│  │  34  │ Fire Show Intro         │ Playlist │ [▶ Play]   │ │
│  │  35  │ Closing Announcement    │ Playlist │ [▶ Play]   │ │
│  │  36  │ Special Event Music     │ Playlist │ [▶ Play]   │ │
│  │  ...                                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Selected: [None]  Volume: [███░░░ 65]  [▶ Play Selected]   │
└──────────────────────────────────────────────────────────────┘
```

---

## Backend API Design

### Base URL
`https://sonos-cloud-api.onrender.com/api/v1`

### Endpoints

#### Authentication
```
POST /auth/login          - Login with credentials
POST /auth/refresh        - Refresh access token
```

#### Schedule Management
```
GET    /schedule                    - Get full weekly schedule
GET    /schedule/{day}              - Get schedule for specific day
POST   /schedule/{day}              - Add time slot
PUT    /schedule/{day}/{slot_id}    - Update time slot
DELETE /schedule/{day}/{slot_id}    - Delete time slot
POST   /schedule/reset              - Reset to default schedule
```

#### Playback Control
```
GET    /playback/status             - Get current playback status
POST   /playback/play               - Play specific program
POST   /playback/pause              - Pause all playback
POST   /playback/skip               - Skip to next scheduled item
POST   /playback/volume             - Set master volume
```

#### Programs
```
GET    /programs                    - List all available programs
GET    /programs/{type}             - Get programs by type (ad, fm, etc.)
POST   /programs                    - Create new program
PUT    /programs/{id}               - Update program
DELETE /programs/{id}               - Delete program
```

#### Speakers
```
GET    /speakers                    - List all speakers with status
GET    /speakers/{id}               - Get specific speaker details
POST   /speakers/group              - Group all speakers
POST   /speakers/ungroup            - Ungroup speakers
PUT    /speakers/{id}/volume        - Set individual speaker volume
```

#### Favorites
```
GET    /favorites                   - List Sonos favorites/playlists
POST   /favorites/{id}/play         - Play specific favorite
```

#### System
```
GET    /system/status               - Overall system health
GET    /system/logs                 - Recent scheduler logs
POST   /system/restart-scheduler    - Restart the scheduler
```

---

## Database Schema (SQLite)

```sql
-- Schedule slots
CREATE TABLE schedule_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_of_week TEXT NOT NULL,           -- monday, tuesday, etc.
    time TEXT NOT NULL,                   -- HH:MM format
    program_name TEXT NOT NULL,           -- e.g., "75ad", "85fm"
    block_type TEXT NOT NULL,             -- AM, DAY, PM_FIRE
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Programs (content types)
CREATE TABLE programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,            -- e.g., "75ad"
    volume INTEGER NOT NULL,              -- 50-95
    type TEXT NOT NULL,                   -- ad, fm, sm, parking, etc.
    favorite_ids TEXT,                    -- JSON array of favorite IDs used
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Execution logs
CREATE TABLE execution_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_name TEXT NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,                 -- success, error
    error_message TEXT
);

-- Settings
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Project Structure

```
sonos-cloud/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   ├── NowPlaying.tsx
│   │   │   │   ├── NextUp.tsx
│   │   │   │   ├── SpeakerStatus.tsx
│   │   │   │   ├── TodayTimeline.tsx
│   │   │   │   └── QuickActions.tsx
│   │   │   ├── Schedule/
│   │   │   │   ├── WeeklyView.tsx
│   │   │   │   ├── DaySchedule.tsx
│   │   │   │   ├── TimeSlotEditor.tsx
│   │   │   │   └── ScheduleImportExport.tsx
│   │   │   ├── Programs/
│   │   │   │   ├── ProgramLibrary.tsx
│   │   │   │   ├── ProgramCard.tsx
│   │   │   │   └── ProgramEditor.tsx
│   │   │   ├── Speakers/
│   │   │   │   ├── SpeakerGrid.tsx
│   │   │   │   ├── SpeakerCard.tsx
│   │   │   │   └── VolumeControl.tsx
│   │   │   ├── Favorites/
│   │   │   │   └── FavoritesList.tsx
│   │   │   └── ui/
│   │   │       └── (shadcn components)
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Schedule.tsx
│   │   │   ├── Programs.tsx
│   │   │   ├── Speakers.tsx
│   │   │   └── Favorites.tsx
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── schedule.ts
│   │   │   ├── playback.ts
│   │   │   ├── speakers.ts
│   │   │   └── favorites.ts
│   │   ├── store/
│   │   │   └── useAppStore.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── index.html
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI app entry
│   │   ├── config.py                    # Configuration
│   │   ├── database.py                  # SQLite connection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── schedule.py
│   │   │   ├── program.py
│   │   │   └── log.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── schedule.py
│   │   │   ├── playback.py
│   │   │   ├── programs.py
│   │   │   ├── speakers.py
│   │   │   ├── favorites.py
│   │   │   └── system.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── sonos_api.py             # Sonos API wrapper
│   │   │   ├── scheduler_service.py     # APScheduler integration
│   │   │   └── program_executor.py      # Runs programs
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── auth.py
│   ├── migrations/
│   │   └── init_db.sql
│   ├── requirements.txt
│   └── Dockerfile
│
├── scripts/                              # Existing scripts (kept)
│   └── ...
│
├── render.yaml                           # Render deployment config
└── README.md
```

---

## Render Deployment Configuration

### render.yaml
```yaml
services:
  # Backend API
  - type: web
    name: sonos-cloud-api
    runtime: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SONOS_CLIENT_ID
        sync: false
      - key: SONOS_CLIENT_SECRET
        sync: false
      - key: SONOS_REFRESH_TOKEN
        sync: false
      - key: API_SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        value: sqlite:///./sonos_cloud.db

  # Frontend Static Site
  - type: static
    name: sonos-cloud-frontend
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

---

## Implementation Steps

### Phase 1: Backend Foundation
1. Set up FastAPI project structure
2. Create SQLite database with schema
3. Migrate existing schedule from `scheduler.py` to database
4. Build Sonos API service wrapper (refactor from existing scripts)
5. Implement schedule CRUD endpoints
6. Implement playback control endpoints

### Phase 2: Frontend Foundation
1. Initialize React + Vite + TypeScript project
2. Set up Tailwind CSS and Shadcn/ui
3. Create API client with React Query
4. Build Dashboard page with real-time status
5. Build basic navigation/layout

### Phase 3: Schedule Management
1. Build weekly schedule view component
2. Create time slot editor modal
3. Implement drag-and-drop schedule editing
4. Add schedule import/export functionality

### Phase 4: Program & Speaker Control
1. Build Program Library page
2. Build Speaker Control page with visual layout
3. Implement individual speaker volume controls
4. Add real-time speaker status updates

### Phase 5: Favorites & Polish
1. Build Favorites page
2. Add quick play functionality
3. Implement system logs view
4. Add error handling and loading states
5. Mobile responsive design

### Phase 6: Deployment
1. Create Render account/project
2. Configure environment variables
3. Deploy backend service
4. Deploy frontend static site
5. Set up custom domain (optional)
6. Configure SSL/HTTPS

---

## Key Features Summary

| Feature | Description |
|---------|-------------|
| Real-time Dashboard | See current playback, next scheduled, speaker status |
| Schedule Editor | Visual weekly schedule with drag-drop editing |
| Program Library | Browse and instantly play any program |
| Speaker Control | Individual volume, grouping, visual venue map |
| Favorites Browser | Quick access to Sonos playlists |
| Responsive Design | Works on desktop, tablet, and mobile |
| Live Updates | WebSocket for real-time status updates |
| Schedule Persistence | Database-backed schedule survives restarts |
| One-click Deploy | Render.yaml for easy deployment |

---

## Environment Variables Required

```env
# Sonos API (from existing scripts)
SONOS_CLIENT_ID=1b66f808-68aa-47db-92dd-13ee474757ba
SONOS_CLIENT_SECRET=61510ebb-aad5-4691-9efa-05c81260df92
SONOS_REFRESH_TOKEN=pWPbYeKxsAsQQGemUiAzuTTxltXOisfu

# Backend
API_SECRET_KEY=<generated>
DATABASE_URL=sqlite:///./sonos_cloud.db
TIMEZONE=America/New_York

# Frontend
VITE_API_URL=https://sonos-cloud-api.onrender.com
```

---

## Ready to Build?

This plan covers everything needed to build a complete control panel for your Sonos venue system. The frontend will:

1. Display the exact schedule currently in your `scheduler.py`
2. Allow real-time control of commercials and programs
3. Provide visual speaker management
4. Enable schedule modifications without code changes
5. Deploy easily to Render with automatic HTTPS

Let me know when you're ready to start implementation!
