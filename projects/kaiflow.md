# Kaiflow

Kaiflow is a local-first transaction management system for cash-in and cash-out
stores. It combines staff transaction entry, protected receipt scanning,
duplicate review, cash reconciliation, reporting, and role-based administration
in a mobile-responsive interface.

## Technology

- FastAPI, SQLAlchemy, and SQLite or MySQL for the API and data layer
- Next.js 16, React 19, TypeScript, and Tailwind CSS for the frontend
- Optional local Tesseract OCR for receipt text extraction
- Signed JWT authentication with optional Google sign-in

## Run locally

Backend (PowerShell):

```powershell
cd fastapi-backend
python -m pip install -r requirements.txt
$env:KAIFLOW_JWT_SECRET = "replace-with-a-long-random-secret"
python -m uvicorn app.main:app --reload
```

On startup, the API creates missing tables in the configured database and
idempotently seeds the default roles, services, branch, and system settings.
It does **not** seed user accounts. Bootstrap the first Super Admin directly in
the database, or promote an existing Google-created user. Google sign-ins start
with the `USER` role.

Frontend (another terminal):

```powershell
cd nextjs-frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The API defaults to `http://localhost:8000`.
Set `NEXT_PUBLIC_API_URL` in `nextjs-frontend/.env.local` when the API uses a
different address.

For backend configuration, create `fastapi-backend/.env`. The application also
loads `fastapi-backend/.env.local`, whose values take precedence. Important
settings include:

```dotenv
KAIFLOW_JWT_SECRET=replace-with-at-least-32-random-characters
KAIFLOW_DATABASE_URL=sqlite:///./kaiflow.db
KAIFLOW_FRONTEND_URL=http://localhost:3000
KAIFLOW_TOKEN_TTL_HOURS=24
KAIFLOW_MAX_RECEIPT_BYTES=8388608
```

Never commit real secrets or use the default JWT secret in production.

## Roles and access

- **Staff / User** processes and searches their own transactions, scans
  receipts, and views their profile.
- **Admin** manages store operations across authorized branches, reviews
  possible duplicates, views staff activity and reports, voids transactions,
  and performs daily cash reconciliation.
- **Super Admin** has Admin capabilities plus System Management for users,
  branches, services, fee rules, settings, and audit-history maintenance.

All permissions are enforced by the backend, not only hidden in the interface.

## Transaction workflow

- Manual cash-in and cash-out entry with service-fee and cash-total calculation
- Receipt upload from storage or a mobile device camera
- Protected receipt storage with file type and size validation
- SHA-256 exact-file detection and reference-number duplicate detection
- Optional OCR parsing for provider, transaction type, reference, amount, and
  wallet account details
- Required staff verification of scanned fields before saving
- Continue-duplicate flow requiring a reason and subsequent Admin review
- Personal and Admin transaction history, search, details, receipt viewing, and
  transaction voiding
- Audit events for sensitive and operational actions

Transaction parties are intentionally stored separately:

- `customer_name` and `customer_phone` identify the person using the store
  service and are entered by staff.
- `wallet_account_name` and `wallet_account_number` identify the account shown
  on the electronic transfer. Receipt scanning may populate these values.
- `store_account_used` identifies the store-owned wallet or bank account that
  handled the transfer.
- The authenticated user is recorded separately as the staff member who
  processed the transaction.

This distinction matters because the wallet account holder is not always the
customer—for example, a cash-out may be sent from a store-owned GCash account.

## Admin and Super Admin features

- Branch-filtered dashboard metrics and transaction lists
- Duplicate approval and rejection workflow
- Staff activity, daily reports, and audit history
- Opening and closing cash reconciliation
- User creation, role and branch assignment, password reset, enable/disable,
  and deletion safeguards
- Branch and service administration
- Configurable fixed or percentage fee rules by service, transaction type, and
  amount range
- Responsive staff and admin navigation, scrollable mobile sidebar, touch-sized
  controls, mobile tables, and compact dialogs
- Light, dark, and system appearance preferences

## Local data and receipt storage

With the default SQLite configuration, development data is stored in
`fastapi-backend/kaiflow.db`. Protected receipts are stored under
`fastapi-backend/storage/receipts`. Both locations are created as needed and
should not be committed.

## Local OCR

Image OCR is optional and remains on the store server. Install the Tesseract OCR
executable and ensure `tesseract.exe` is available on `PATH`, then install the
Python requirements. Current parsing recognizes GCash, Maya, BPI, BDO,
Metrobank, UnionBank, and GoTyme receipt text. It also normalizes masked GCash
account names when possible.

If Tesseract is unavailable or cannot read an image, Kaiflow still stores the
receipt and asks Staff to enter and verify the fields manually. Exact-file
hashing and duplicate checks remain active either way. OCR output is treated as
a suggestion and never bypasses backend validation or staff verification.

## Optional Google sign-in

Set the following values in `fastapi-backend/.env` to enable Google sign-in:

```dotenv
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
KAIFLOW_FRONTEND_URL=http://localhost:3000
```

Configure the same callback URI in Google Cloud. When these settings are not
present, standard username/password authentication remains available and the
Google backend flow stays disabled.

## Backend tests

```powershell
cd fastapi-backend
python -m pytest
```

Tests use an isolated SQLite database under `fastapi-backend/tests/`; they do
not use the database configured in your local `.env`. Test-only Staff, Admin,
and Super Admin accounts are created by the test fixtures.

## Frontend checks

```powershell
cd nextjs-frontend
npm run lint
npm run build
```

## Switch to MySQL

1. Install and start MySQL 8.x on the store server.
2. Create the `kaiflow` database and an application user with access to it.
3. Set the connection URL and JWT secret in `fastapi-backend/.env`:

```dotenv
KAIFLOW_DATABASE_URL=mysql+pymysql://kaiflow_user:YOUR_PASSWORD@127.0.0.1:3306/kaiflow
KAIFLOW_JWT_SECRET=replace-with-at-least-32-random-characters
```

Alternatively, provide `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`,
`MYSQL_PASSWORD`, and `MYSQL_DATABASE`. When a MySQL user and database are
configured this way, those settings take precedence over
`KAIFLOW_DATABASE_URL`.

The API creates missing tables and seed records on startup. `schema.sql` is a
readable MySQL reference copy of the schema. After changing a model, regenerate
it from `fastapi-backend/` with:

```powershell
python -m scripts.export_schema
```
