# Software Construction & Development Report

## Velocity Nexus Prime Vehicle Ecosystem

### 1. Process Model Implemented

**Agile-V Model Hybrid Approach**
We implemented a hybrid process model combining Agile methodology with the V-Model.

- **Agile:** Allowed for iterative UI development.
- **V-Model:** Ensured rigorous verification of the SQL Database logic.

### 2. Design Patterns

- **Singleton:** Used in `database/connection.py` to manage SQL resources efficiently.
- **Repository Pattern:** Used in `repositories/vehicle_repo.py` to separate SQL queries from Python logic.
- **Facade:** The Service layer acts as a facade for the complex database operations.

### 3. Lehman's Laws of Evolution

- **Law of Continuing Change:** The system was designed with modular `src` folders to allow easy addition of new Manufacturers (e.g., Tesla) without breaking existing code.
- **Law of Increasing Complexity:** We managed complexity by strictly separating the UI (Tkinter) from the Data (SQL).

### 4. Database Normalization (DBS)

- **1NF:** Atomic values in all columns.
- **2NF:** All non-key attributes dependent on the Primary Key.
- **3NF:** Removed transitive dependencies (e.g., separating `Manufacturers` from `VehicleModels`).
