# Animal Shelter Angular + Spring Boot

## Requirements

- Docker Desktop for PostgreSQL and the Spring API
- Node.js 22+ for the Angular development server

Java and Maven are only needed when running the backend outside Docker.

## Start the database and API

From this `App` folder:

```powershell
docker compose up --build
```

The PostgreSQL database runs on `localhost:5432` and the API runs on `http://localhost:8080`.

## Start Angular

In a second terminal:

```powershell
Set-Location shelter-ui
npm install
npm start
```

Open `http://localhost:4200`. The Angular animal grid requests data from `http://localhost:8080/api/animals`.

## Stop services

```powershell
docker compose down
```

Add `-v` only when you intentionally want to delete the local database volume.
