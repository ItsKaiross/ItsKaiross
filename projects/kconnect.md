# K Connect

**Every organization. Every event. Connected.**

K Connect is a comprehensive multi-organization event, task, student, and attendance management platform designed for school and campus organizations. It combines organization public websites, internal management tools, event planning and approval workflows, QR-based attendance tracking, and detailed reporting into one unified system.

## 🎯 Overview

K Connect enables organizations to manage their complete event lifecycle from a single platform:

```
CREATE ORGANIZATION → INVITE STAFF → MANAGE STUDENTS → CREATE EVENT → 
PROFESSOR APPROVAL → ADMIN PUBLICATION → ASSIGN PARTICIPANTS → 
ORGANIZE TASKS → TRACK CALENDAR → GENERATE STUDENT QR → 
CONDUCT EVENT → SCAN ATTENDANCE → REPORT & HISTORY
```

## 🚀 Key Features

### Multi-Tenant Architecture
- **Platform-level system administration** - System admins manage all organizations
- **Organization isolation** - Complete data separation between organizations
- **Custom organization slugs** - Each organization gets its own branded URL (e.g., `/css`, `/acm`)
- **Public organization pages** - Showcase events and information to visitors
- **Organization branding** - Customizable logos, colors, and descriptions

### Authentication & Authorization
- **Google OAuth integration** - Secure authentication via institutional Google accounts
- **Role-based access control (RBAC)** - Granular permission system
- **Role hierarchy**:
  - System Admin (platform-level)
  - Organization Admin/President
  - Vice President
  - Treasurer (financial management)
  - Professor (event approval)
  - Representative (event creation and management)
- **Invitation system** - Email-based onboarding with secure tokens
- **Direct provisioning** - Quick member addition for routine onboarding

### Organization Management
- Organization CRUD operations
- Organization status management (active/archived)
- Member management with role assignment
- Team directory with real-time messaging
- Organization settings and configuration
- Public contact form for external feedback
- Audit logging for all administrative actions

### Academic Structure
- **Academic sessions** - Year-based organization (e.g., "2023-2024")
- **Semesters** - Term-based tracking within sessions
- **Courses** - Degree programs (e.g., "BS Computer Science")
- **Sections** - Class groupings with year levels (1st Year, 2nd Year, etc.)
- Hierarchical structure linking students to sections, courses, and sessions

### Student Management
- **Manual student creation** - Add students individually
- **CSV/Excel import** - Bulk student import with preview and validation
- **Student directory** - Searchable and filterable student roster
- **Student profiles** - Complete student information including:
  - Student number (unique identifier)
  - Personal details (name, email, phone)
  - Academic information (course, year level, section)
- **Enrollment history** - Track student section assignments over time
- **Student QR codes** - Unique, reusable QR identity for attendance

### Event Management
- **Event proposal system** - Create detailed event proposals with:
  - Basic information (title, description, dates, venue)
  - Event objectives
  - Program/agenda items with time slots
  - Budget items (estimates for planning)
  - File attachments
- **Event approval workflow**:
  - Draft → Submitted → Approved/Rejected/Revision Requested
  - Professor-level approval with comments
  - Approval history tracking
- **Event publication** - Admin-controlled publication to public pages
- **Event categories** - Organize events by type
- **Event participant management**:
  - Add specific students
  - Add entire sections
  - Add by year level or course
  - Track required vs optional attendees
- **Event email integration** - Send event details via Gmail
- **Event exports** - PDF and Word document generation

### Attendance System
- **QR-based student attendance**:
  - Generate secure, organization-branded QR codes
  - Single or batch QR generation
  - QR revocation and regeneration
  - Live QR scanning during events
  - Duplicate scan protection
  - Attendance verification for required attendees
- **Member attendance tracking**:
  - Track organization member attendance at events
  - Mark present/absent/late status
  - View member attendance roster
- **Attendance history** - Complete attendance records per student
- **Real-time scanning** - Instant attendance registration

### Task Management
- **Task creation and assignment** - Assign tasks to representatives
- **Event-linked tasks** - Associate tasks with specific events
- **Task lifecycle**:
  - Status: Not Started → In Progress → Completed → Cancelled
  - Progress tracking (0-100%)
  - Due dates and priorities
- **Task activity log** - Complete audit trail of changes
- **Task comments** - Threaded discussion on tasks
- **My Tasks view** - Personal task dashboard for representatives

### Calendar & Scheduling
- **Organization calendar** - View all events, tasks, and meetings
- **Personal calendar** - Representative-specific view
- **Meeting management**:
  - Schedule organization meetings
  - Mark member attendance
  - Meeting history
- **Date-based filtering** - View events by date range
- **Calendar exports** - Export organization schedules

### Real-Time Communication
- **Team messaging** - Internal chat between organization members
- **Conversation threads** - One-on-one and group conversations
- **Live websocket updates** - Real-time message delivery
- **Member directory** - Browse and message team members
- **Unread message tracking** - Track unread conversation counts

### Reporting & Analytics
- **Event attendance reports**:
  - Attendance overview with present/absent counts
  - Student-level attendance details
  - Export to PDF
- **Student attendance statistics**:
  - Total events attended
  - Attendance rate
  - Event history
- **Section attendance reports**:
  - Attendance by section
  - Academic session filtering
  - PDF export
- **Representative task completion reports**:
  - Task completion rates per representative
  - Overdue task tracking
- **Organization analytics**:
  - Total students, events, tasks
  - Event status distribution
  - Activity metrics

### Public Features
- **Global event discovery** - Browse all published events across organizations
- **Organization directory** - Discover all active organizations
- **Public organization pages** - View organization details and upcoming events
- **Event filtering** - Filter by date, organization, category
- **Contact forms** - Allow visitors to send feedback to organizations

### System Administration
- **Organization management** - Create, edit, archive organizations
- **Admin assignment** - Invite and manage organization administrators
- **Member provisioning** - Direct member access provisioning
- **Invitation management** - Resend, cancel, and track invitations
- **System-wide audit logs** - Platform-level activity tracking
- **Role management** - View and manage system roles
- **Cross-organization visibility** - Monitor all organizations

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MySQL
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: Google OAuth 2.0, python-jose (JWT)
- **Document Generation**: ReportLab (PDF), python-docx (Word)
- **QR Codes**: qrcode library with PIL
- **Async Support**: httpx for async HTTP requests

### Frontend
- **Framework**: Next.js 16.3.2 (React 19)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **QR Scanning**: jsQR library
- **Real-time**: WebSocket integration

### Infrastructure
- **Server**: Uvicorn with standard extras
- **Database Driver**: PyMySQL with cryptography
- **Environment Management**: python-dotenv
- **File Uploads**: python-multipart
- **Validation**: Pydantic 2 with settings management

## 📁 Project Structure

```
Kconnect/
├── fastapi-backend/          # FastAPI backend application
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   │   ├── auth.py      # Authentication
│   │   │   ├── organizations.py
│   │   │   ├── events.py
│   │   │   ├── students.py
│   │   │   ├── attendance.py
│   │   │   ├── tasks.py
│   │   │   ├── calendar.py
│   │   │   ├── meetings.py
│   │   │   ├── conversations.py
│   │   │   ├── reports.py
│   │   │   ├── system.py
│   │   │   └── ...
│   │   ├── core/            # Core utilities
│   │   │   ├── security.py  # JWT, OAuth
│   │   │   ├── permissions.py
│   │   │   └── ws_manager.py # WebSocket manager
│   │   ├── database/        # Database configuration
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── repositories/    # Data access layer
│   │   └── services/        # Business logic
│   ├── migrations/          # Alembic migrations
│   ├── scripts/             # Utility scripts
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
│
├── nextjs-frontend/         # Next.js frontend application
│   ├── app/                # App router
│   │   ├── (auth)/         # Auth pages
│   │   ├── (public)/       # Public pages
│   │   ├── dashboard/      # Organization dashboard
│   │   └── system/         # System admin
│   ├── features/           # Feature modules
│   │   ├── academic/       # Academic structure
│   │   ├── attendance/     # Attendance tracking
│   │   ├── auth/           # Authentication
│   │   ├── calendar/       # Calendar views
│   │   ├── events/         # Event management
│   │   ├── meetings/       # Meeting scheduling
│   │   ├── organization/   # Organization management
│   │   ├── public/         # Public-facing features
│   │   ├── reports/        # Reporting & analytics
│   │   ├── students/       # Student management
│   │   ├── system/         # System admin features
│   │   ├── tasks/          # Task management
│   │   └── team/           # Team messaging
│   ├── lib/               # Shared utilities
│   ├── types/             # TypeScript types
│   ├── public/            # Static assets
│   └── package.json       # Node dependencies
│
└── docs/                  # Documentation
    ├── K_Connect_System_Documentation.md
    ├── invitation-migration.md
    ├── notifications.md
    └── ogranization-funds.md
```

## 🔒 Security Features

- **OAuth 2.0 authentication** - No passwords stored
- **JWT session management** - Secure token-based sessions
- **Organization-scoped authorization** - Strict permission checks
- **Role-based access control** - Granular permission system
- **CSRF protection** - Secure state management
- **SQL injection prevention** - ORM-based queries
- **Audit logging** - Track all administrative actions
- **QR token security** - Cryptographically signed QR codes
- **Email verification** - Confirm Google account ownership

## 📊 Database Models

### Core Models
- **User** - Platform users with Google authentication
- **Organization** - Organizations using the platform
- **OrganizationMember** - User-organization relationships with roles
- **Role** - System roles (System Admin, Org Admin, Professor, etc.)
- **Permission** - Granular permissions
- **RolePermission** - Role-permission mappings

### Academic Models
- **AcademicSession** - Academic years
- **Semester** - Terms within sessions
- **Course** - Degree programs
- **Section** - Class sections with year levels
- **Student** - Student records
- **StudentEnrollment** - Student-section assignments

### Event Models
- **Event** - Event proposals and published events
- **EventObjective** - Event goals
- **EventProgramItem** - Event agenda
- **EventBudgetItem** - Event budget estimates
- **EventAttendee** - Expected event participants
- **EventApprovalHistory** - Approval workflow history
- **EventEmail** - Event email communication log

### Attendance Models
- **Attendance** - Student event attendance records
- **StudentQrCode** - Reusable student QR codes
- **Meeting** - Organization meetings
- **MemberAttendance** - Member meeting attendance

### Task & Communication Models
- **Task** - Task assignments
- **TaskActivity** - Task change history
- **Conversation** - Message threads
- **ConversationMessage** - Individual messages
- **OrganizationMessage** - Public feedback messages

### System Models
- **OrganizationInvitation** - Member invitation tokens
- **AuditLog** - System-wide activity log

## 🚦 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- MySQL 8.0+
- Google OAuth credentials

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd fastapi-backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create `.env` file with:
   ```env
   DATABASE_URL=mysql+pymysql://user:password@localhost/kconnect
   SECRET_KEY=your-secret-key
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd nextjs-frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create `.env.local` file with:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

5. **Access the application**:
   Open [http://localhost:3000](http://localhost:3000)

## 📖 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🧪 Testing

### Backend Tests
```bash
cd fastapi-backend
pytest
```

### Frontend Linting
```bash
cd nextjs-frontend
npm run lint
```

## 🔄 Planned Features

The following features are documented but not yet implemented:

### In-App Notification System
- Database-persisted notifications
- Real-time push via WebSocket
- Sound notifications
- Bell icon with unread count
- Notification panel with read/unread status
- Notifications for: task assignment, event approval, role changes, meetings, etc.

### Organization Funds Management
- Financial transaction ledger
- Income and expense tracking
- Draft and posted transaction states
- Event budget vs actual comparison
- Treasurer role with full access
- President/VP read-only access
- Financial reports and exports
- Receipt attachment support

## 🏗️ Development Phases

The project has been developed in phases:

1. ✅ **Authentication & RBAC** - User auth, roles, permissions
2. ✅ **Organization Management** - Org CRUD, members, invitations
3. ✅ **Academic Structure** - Sessions, courses, sections
4. ✅ **Student Management** - Student directory, imports
5. ✅ **Event Proposal** - Event creation with objectives, program, budget
6. ✅ **Event Approval** - Professor approval workflow
7. ✅ **Event Export** - PDF/Word generation, Gmail integration
8. ✅ **Event Publication** - Public event pages
9. ✅ **Event Participants** - Attendee selection and management
10. ✅ **Student QR** - QR code generation and management
11. ✅ **Attendance** - QR scanning and tracking
12. ✅ **Tasks** - Task assignment and tracking
13. ✅ **Calendar** - Organization and personal calendars
14. ✅ **Meetings** - Meeting scheduling and attendance
15. ✅ **Team Messaging** - Real-time internal communication
16. ✅ **Reporting** - Analytics and exports

## 🤝 Contributing

This is a private project. For questions or contributions, please contact the project maintainers.

## 📝 License

All rights reserved. This is proprietary software.

## 🎨 Brand

**K Connect** - Where **K** represents **Kairos** (the right or opportune moment), and **Connect** represents the connections between organizations, people, events, responsibilities, students, attendance, and important moments.

---

**Built with ❤️ for campus organizations**


