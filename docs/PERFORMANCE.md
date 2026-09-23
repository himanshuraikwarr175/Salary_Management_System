# Performance considerations (~10,000 employees)

## Goals

- List/search feels responsive  
- Dashboard aggregations complete in well under a second on local/Docker SQLite  
- Browser never downloads the full 10k row set  

## What we did

| Area | Approach |
|------|----------|
| List API | Server-side pagination (`page`, `page_size` capped at 100) |
| Search/filter | SQL `WHERE` + indexes on `full_name`, `employee_code`, `country_code`, `department` |
| Analytics | SQL `GROUP BY` / `SUM` / `AVG` — not Python loops over all employees |
| Seed | Batched inserts (500 rows) to keep load time reasonable |
| FX | Cached Frankfurter rates (~1 hour) so dashboard refresh does not hammer the provider |
| UI | TanStack Query caching; tables show page slices / capped breakdown rows |

## What we did not over-engineer

- Redis / read replicas  
- Materialized analytics tables  
- Full-text search engines  

At 10k rows on SQLite these are unnecessary for the assessment. If the org grew to hundreds of thousands of employees, we would move analytics to Postgres, add covering indexes, and consider cached summary tables refreshed on salary writes.

## How to verify

```bash
cd backend && source .venv/bin/activate
pytest -v
# Manual: open Employees, flip pages; open Dashboard with FX base USD
```
