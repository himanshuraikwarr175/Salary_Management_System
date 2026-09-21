import { useQuery } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { fetchEmployees, formatMoney } from "../api/client";
import { ErrorBox, Spinner } from "../components/Status";

const COUNTRIES = ["", "US", "IN", "GB", "DE", "CA", "AU", "SG", "JP"];
const DEPARTMENTS = [
  "",
  "Engineering",
  "Sales",
  "HR",
  "Finance",
  "Marketing",
  "Operations",
  "Product",
  "Customer Success",
];

export function EmployeesPage() {
  const [q, setQ] = useState("");
  const [country, setCountry] = useState("");
  const [department, setDepartment] = useState("");
  const [page, setPage] = useState(1);
  const [submitted, setSubmitted] = useState({
    q: "",
    country: "",
    department: "",
  });

  const list = useQuery({
    queryKey: ["employees", submitted, page],
    queryFn: () =>
      fetchEmployees({
        q: submitted.q || undefined,
        country: submitted.country || undefined,
        department: submitted.department || undefined,
        page,
        page_size: 20,
      }),
  });

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    setPage(1);
    setSubmitted({ q, country, department });
  }

  const totalPages = list.data
    ? Math.max(1, Math.ceil(list.data.total / list.data.page_size))
    : 1;

  return (
    <div className="space-y-5">
      <form
        onSubmit={onSubmit}
        className="grid gap-3 rounded-xl bg-white/90 p-4 shadow-sm ring-1 ring-slate-200/80 sm:grid-cols-4"
      >
        <label className="block text-sm sm:col-span-2">
          <span className="mb-1 block text-xs font-medium uppercase tracking-wide text-slate-500">
            Search
          </span>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Name, code, or email"
            className="w-full rounded-md border border-slate-200 px-3 py-2 outline-none ring-accent focus:ring-2"
          />
        </label>
        <label className="block text-sm">
          <span className="mb-1 block text-xs font-medium uppercase tracking-wide text-slate-500">
            Country
          </span>
          <select
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            className="w-full rounded-md border border-slate-200 px-3 py-2 outline-none ring-accent focus:ring-2"
          >
            {COUNTRIES.map((c) => (
              <option key={c || "all"} value={c}>
                {c || "All"}
              </option>
            ))}
          </select>
        </label>
        <label className="block text-sm">
          <span className="mb-1 block text-xs font-medium uppercase tracking-wide text-slate-500">
            Department
          </span>
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="w-full rounded-md border border-slate-200 px-3 py-2 outline-none ring-accent focus:ring-2"
          >
            {DEPARTMENTS.map((d) => (
              <option key={d || "all"} value={d}>
                {d || "All"}
              </option>
            ))}
          </select>
        </label>
        <div className="sm:col-span-4">
          <button
            type="submit"
            className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white hover:bg-accentDark"
          >
            Apply filters
          </button>
        </div>
      </form>

      {list.isLoading && <Spinner />}
      {list.isError && (
        <ErrorBox message={(list.error as Error).message || "Failed to load"} />
      )}

      {list.data && (
        <>
          <p className="text-sm text-slate-600">
            Showing {list.data.items.length} of {list.data.total.toLocaleString()}{" "}
            employees
          </p>
          <div className="overflow-hidden rounded-xl bg-white/90 shadow-sm ring-1 ring-slate-200/80">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-4 py-3 font-medium">Employee</th>
                  <th className="px-4 py-3 font-medium">Dept</th>
                  <th className="px-4 py-3 font-medium">Country</th>
                  <th className="px-4 py-3 font-medium">Salary</th>
                </tr>
              </thead>
              <tbody>
                {list.data.items.map((emp) => (
                  <tr key={emp.id} className="border-t border-slate-100">
                    <td className="px-4 py-3">
                      <Link
                        to={`/employees/${emp.id}`}
                        className="font-medium text-accentDark hover:underline"
                      >
                        {emp.full_name}
                      </Link>
                      <div className="text-xs text-slate-500">
                        {emp.employee_code} · {emp.job_title}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-slate-700">{emp.department}</td>
                    <td className="px-4 py-3 text-slate-700">
                      {emp.country_code}
                    </td>
                    <td className="px-4 py-3 font-medium text-ink">
                      {formatMoney(emp.annual_salary, emp.currency_code)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex items-center justify-between gap-3">
            <button
              type="button"
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-sm disabled:opacity-40"
            >
              Previous
            </button>
            <span className="text-sm text-slate-600">
              Page {page} / {totalPages}
            </span>
            <button
              type="button"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => p + 1)}
              className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-sm disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}
