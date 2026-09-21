import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { Link, useParams } from "react-router-dom";
import {
  fetchEmployee,
  fetchSalaryHistory,
  formatMoney,
  updateSalary,
} from "../api/client";
import { ErrorBox, Spinner } from "../components/Status";

export function EmployeeDetailPage() {
  const { id } = useParams();
  const employeeId = Number(id);
  const queryClient = useQueryClient();
  const [salary, setSalary] = useState("");
  const [note, setNote] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  const employee = useQuery({
    queryKey: ["employee", employeeId],
    queryFn: () => fetchEmployee(employeeId),
    enabled: Number.isFinite(employeeId),
  });

  const history = useQuery({
    queryKey: ["salary-history", employeeId],
    queryFn: () => fetchSalaryHistory(employeeId),
    enabled: Number.isFinite(employeeId),
  });

  const mutation = useMutation({
    mutationFn: () => updateSalary(employeeId, salary, note),
    onSuccess: async () => {
      setMessage("Salary updated.");
      setNote("");
      await queryClient.invalidateQueries({ queryKey: ["employee", employeeId] });
      await queryClient.invalidateQueries({
        queryKey: ["salary-history", employeeId],
      });
      await queryClient.invalidateQueries({ queryKey: ["employees"] });
      await queryClient.invalidateQueries({ queryKey: ["summary"] });
    },
    onError: (err: Error) => setMessage(err.message),
  });

  if (employee.isLoading) return <Spinner />;
  if (employee.isError || !employee.data) {
    return <ErrorBox message="Employee not found or API unavailable." />;
  }

  const emp = employee.data;

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    setMessage(null);
    mutation.mutate();
  }

  return (
    <div className="space-y-6">
      <Link
        to="/employees"
        className="text-sm font-medium text-accentDark hover:underline"
      >
        ← Back to employees
      </Link>

      <section className="rounded-xl bg-white/90 p-6 shadow-sm ring-1 ring-slate-200/80">
        <p className="text-xs font-semibold uppercase tracking-wider text-accent">
          {emp.employee_code}
        </p>
        <h2 className="mt-1 font-display text-3xl font-semibold text-ink">
          {emp.full_name}
        </h2>
        <p className="mt-1 text-slate-600">
          {emp.job_title} · {emp.department} · {emp.country_code}
        </p>
        <dl className="mt-5 grid gap-3 sm:grid-cols-2">
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">
              Email
            </dt>
            <dd className="text-sm font-medium">{emp.email}</dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">
              Current annual salary
            </dt>
            <dd className="text-lg font-semibold text-ink">
              {formatMoney(emp.annual_salary, emp.currency_code)}
            </dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">
              Hire date
            </dt>
            <dd className="text-sm font-medium">{emp.hire_date}</dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">
              Status
            </dt>
            <dd className="text-sm font-medium">
              {emp.is_active ? "Active" : "Inactive"}
            </dd>
          </div>
        </dl>
      </section>

      <section className="rounded-xl bg-white/90 p-6 shadow-sm ring-1 ring-slate-200/80">
        <h3 className="font-display text-xl font-semibold text-ink">
          Update salary
        </h3>
        <p className="mt-1 text-sm text-slate-600">
          Currency stays {emp.currency_code}. A history row is written on every
          change.
        </p>
        <form onSubmit={onSubmit} className="mt-4 grid gap-3 sm:grid-cols-2">
          <label className="block text-sm">
            <span className="mb-1 block text-xs font-medium uppercase tracking-wide text-slate-500">
              New annual salary
            </span>
            <input
              required
              type="number"
              min="0.01"
              step="0.01"
              value={salary}
              onChange={(e) => setSalary(e.target.value)}
              placeholder={String(emp.annual_salary)}
              className="w-full rounded-md border border-slate-200 px-3 py-2 outline-none ring-accent focus:ring-2"
            />
          </label>
          <label className="block text-sm">
            <span className="mb-1 block text-xs font-medium uppercase tracking-wide text-slate-500">
              Note (optional)
            </span>
            <input
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Promotion, market adjustment…"
              className="w-full rounded-md border border-slate-200 px-3 py-2 outline-none ring-accent focus:ring-2"
            />
          </label>
          <div className="sm:col-span-2">
            <button
              type="submit"
              disabled={mutation.isPending}
              className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white hover:bg-accentDark disabled:opacity-60"
            >
              {mutation.isPending ? "Saving…" : "Save salary"}
            </button>
            {message && (
              <p className="mt-2 text-sm text-slate-700">{message}</p>
            )}
          </div>
        </form>
      </section>

      <section className="overflow-hidden rounded-xl bg-white/90 shadow-sm ring-1 ring-slate-200/80">
        <div className="border-b border-slate-100 px-4 py-3">
          <h3 className="font-display text-lg font-semibold text-ink">
            Salary history
          </h3>
        </div>
        {history.isLoading && (
          <div className="px-4">
            <Spinner />
          </div>
        )}
        {history.data && history.data.length === 0 && (
          <p className="px-4 py-6 text-sm text-slate-600">No changes yet.</p>
        )}
        {history.data && history.data.length > 0 && (
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2 font-medium">When</th>
                <th className="px-4 py-2 font-medium">Old</th>
                <th className="px-4 py-2 font-medium">New</th>
                <th className="px-4 py-2 font-medium">Note</th>
              </tr>
            </thead>
            <tbody>
              {history.data.map((row) => (
                <tr key={row.id} className="border-t border-slate-100">
                  <td className="px-4 py-2 text-slate-600">
                    {new Date(row.changed_at).toLocaleString()}
                  </td>
                  <td className="px-4 py-2">
                    {formatMoney(row.old_salary, row.currency_code)}
                  </td>
                  <td className="px-4 py-2 font-medium">
                    {formatMoney(row.new_salary, row.currency_code)}
                  </td>
                  <td className="px-4 py-2 text-slate-600">{row.note || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
