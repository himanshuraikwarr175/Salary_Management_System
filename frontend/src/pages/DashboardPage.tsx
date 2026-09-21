import { useQuery } from "@tanstack/react-query";
import {
  fetchByCountry,
  fetchByDepartment,
  fetchSummary,
  formatMoney,
} from "../api/client";
import { ErrorBox, Spinner } from "../components/Status";

export function DashboardPage() {
  const summary = useQuery({ queryKey: ["summary"], queryFn: fetchSummary });
  const byCountry = useQuery({
    queryKey: ["by-country"],
    queryFn: fetchByCountry,
  });
  const byDepartment = useQuery({
    queryKey: ["by-department"],
    queryFn: fetchByDepartment,
  });

  if (summary.isLoading || byCountry.isLoading || byDepartment.isLoading) {
    return <Spinner label="Loading compensation insights…" />;
  }

  if (summary.isError || byCountry.isError || byDepartment.isError) {
    return (
      <ErrorBox message="Could not load analytics. Is the API running on port 8000?" />
    );
  }

  const data = summary.data!;

  return (
    <div className="space-y-8">
      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article className="rounded-xl bg-ink px-5 py-6 text-white shadow-sm">
          <p className="text-xs uppercase tracking-wider text-teal-200">
            Active headcount
          </p>
          <p className="mt-2 font-display text-4xl font-semibold">
            {data.headcount.toLocaleString()}
          </p>
          <p className="mt-2 text-sm text-slate-300">
            Totals stay per currency — no FX mixing.
          </p>
        </article>
        {data.by_currency.slice(0, 5).map((row) => (
          <article
            key={row.currency_code}
            className="rounded-xl bg-white/90 px-5 py-5 shadow-sm ring-1 ring-slate-200/80"
          >
            <p className="text-xs font-semibold uppercase tracking-wider text-accent">
              {row.currency_code}
            </p>
            <p className="mt-2 text-2xl font-semibold text-ink">
              {formatMoney(row.total_annual_salary, row.currency_code)}
            </p>
            <p className="mt-1 text-sm text-slate-600">
              {row.headcount.toLocaleString()} people · avg{" "}
              {formatMoney(row.avg_annual_salary, row.currency_code)}
            </p>
          </article>
        ))}
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <BreakdownTable
          title="By country"
          rows={byCountry.data!.map((r) => ({
            key: `${r.country_code}-${r.currency_code}`,
            label: r.country_code,
            currency: r.currency_code,
            headcount: r.headcount,
            total: r.total_annual_salary,
            avg: r.avg_annual_salary,
          }))}
        />
        <BreakdownTable
          title="By department"
          rows={byDepartment.data!.map((r) => ({
            key: `${r.department}-${r.currency_code}`,
            label: r.department,
            currency: r.currency_code,
            headcount: r.headcount,
            total: r.total_annual_salary,
            avg: r.avg_annual_salary,
          }))}
        />
      </div>
    </div>
  );
}

type Row = {
  key: string;
  label: string;
  currency: string;
  headcount: number;
  total: string;
  avg: string;
};

function BreakdownTable({ title, rows }: { title: string; rows: Row[] }) {
  return (
    <section className="overflow-hidden rounded-xl bg-white/90 shadow-sm ring-1 ring-slate-200/80">
      <div className="border-b border-slate-100 px-4 py-3">
        <h2 className="font-display text-lg font-semibold text-ink">{title}</h2>
      </div>
      <div className="max-h-96 overflow-auto">
        <table className="w-full text-left text-sm">
          <thead className="sticky top-0 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Name</th>
              <th className="px-4 py-2 font-medium">CCY</th>
              <th className="px-4 py-2 font-medium">People</th>
              <th className="px-4 py-2 font-medium">Avg</th>
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 40).map((row) => (
              <tr key={row.key} className="border-t border-slate-100">
                <td className="px-4 py-2 font-medium text-ink">{row.label}</td>
                <td className="px-4 py-2 text-slate-600">{row.currency}</td>
                <td className="px-4 py-2 text-slate-600">
                  {row.headcount.toLocaleString()}
                </td>
                <td className="px-4 py-2 text-slate-700">
                  {formatMoney(row.avg, row.currency)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
