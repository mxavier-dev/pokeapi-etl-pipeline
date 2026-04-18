# 🐍 PokéAPI ETL Pipeline

A production-oriented ETL pipeline built in Python to extract, transform, and load real data from the PokéAPI into a relational MySQL database.

---

## 📌 Objective

This project simulates a real-world data engineering workflow, focusing on:

* Consuming external APIs (real-world data)
* Transforming semi-structured JSON into structured datasets
* Relational data modeling
* Efficient batch data loading
* Deduplication using UPSERT logic
* Performance optimization (reducing database round-trips)

---

## 🏗️ Project Structure

```
etl_pokeapi/
├── data/
│   ├── raw/
│   └── processed/
│
├── db/
│   └── schema.sql
│
├── src/
│   ├── connect/
│   │   ├── config.py
│   │   └── connection.py
│   │
│   ├── utils/
│   │   └── logger.py
│   │
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── .gitignore
└── README.md
```

---

## 🔄 Pipeline Flow

```text
Extract → Transform → Load
```

### 1. Extract (`extract.py`)

* Fetches data from PokéAPI endpoints
* Handles pagination manually
* Returns raw JSON data

### 2. Transform (`transform.py`)

* Normalizes nested JSON structures
* Extracts relevant attributes (id, name, weight, height)
* Handles lists (types, abilities)
* Outputs structured pandas DataFrames

### 3. Load (`load.py`)

* Saves raw and processed data locally (JSON)
* Inserts data into MySQL using batch operations
* Uses `executemany()` for performance
* Implements UPSERT logic
* Handles many-to-many relationships (types, abilities)

---

## 🗄️ Database Model

### Core Tables

* `pokemon`
* `types`
* `abilities`

### Relationship Tables

* `pokemon_types`
* `pokemon_abilities`


## 🔗 Relationships

```text
pokemon 1---N pokemon_types N---1 types
pokemon 1---N pokemon_abilities N---1 abilities
```
---

## 📊 Sample Output

Example query result after pipeline execution:

| pokemon    | type1   | type2   |
|------------|--------|--------|
| bulbasaur  | grass  | poison |
| charmander | fire   | NULL   |
| squirtle   | water  | NULL   |

## 📸 Database Preview

Example query result from MySQL:

Command used:\
SELECT p.name AS pokemon,\
GROUP_CONCAT(t.name) AS types\
FROM pokemon p\
JOIN pokemon_types pt ON p.id = pt.pokemon_id\
JOIN types t ON pt.type_id = t.id\
GROUP BY p.id;\
<img width="179" height="208" alt="image" src="https://github.com/user-attachments/assets/595692b5-6951-4164-80c1-3026eab091f8" />


---

## ⚙️ Technologies

* Python 3.10+
* Pandas
* MySQL
* MySQL Connector
* Requests

---

## 🚀 Key Engineering Decisions

### ✔ Batch Inserts

```python
cursor.executemany()
```

Reduces database round-trips significantly.

### ✔ UPSERT Strategy

```sql
ON DUPLICATE KEY UPDATE
```

Ensures idempotent data loading.

### ✔ Optimized ID Resolution

```sql
LAST_INSERT_ID(id)
```

Avoids unnecessary SELECT queries.

### ✔ In-Memory Mapping (Cache)

```python
{name: id}
```

Avoids repeated lookups during relationship inserts.

---

## ▶️ How to Run

### 1. Clone repository

```bash
git clone https://github.com/mxavier-dev/etl-pokeapi.git
cd etl-pokeapi
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup database

Run the schema file:

```bash
mysql -u root -p -e "CREATE DATABASE etl_pokeapi;"
mysql -u root -p etl_pokeapi < db/schema.sql
```

### 5. Run pipeline

```bash
python src/pipeline.py
```
> If you encounter a "python not found" error, make sure Python is installed and added to your system PATH.  
> On some systems, you may need to use `python3` instead of `python`.

---

## ⏱️ Execution Time

This pipeline processes real data from the PokéAPI and performs multiple transformations and database operations.

- Expected runtime: **~3–5 minutes**
- Depends on:
  - API response time
  - Network latency
  - Database performance

This is expected behavior for a full data load without parallelization or caching layers.

---

## 📂 Data Output

* Raw data → `data/raw/`
* Processed data → `data/processed/`

Files are timestamped for versioning.

---

## ⚠️ Important Notes

* AUTO_INCREMENT IDs may skip values (expected behavior)
* SQL does not guarantee row order without `ORDER BY`
* Foreign keys require correct load ordering

---

## 📈 Possible Improvements

* Incremental data ingestion
* Parallel API requests
* Logging enrichment (metrics, timing)
* Dockerization
* Workflow orchestration (Airflow)

---

## 📚 What This Project Demonstrates

* Real API ingestion
* Data normalization
* Relational modeling
* Batch processing
* Performance optimization
* Transaction handling

---

## 📫 Contact

Developed by **Matheus de Freitas Xavier** • [Linkedin Profile](https://www.linkedin.com/in/matheus-xavier-a14b0732a)
