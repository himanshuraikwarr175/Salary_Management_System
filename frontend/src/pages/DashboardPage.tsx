import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import {
  fetchByCountry,
  fetchByDepartment,
  fetchSummary,
  formatMoney,
} from "../api/client";
import { ErrorBox, Spinner } from "../components/Status";

const BASE_OPTIONS = ["USD", "EUR", "INR", "GBP", "CAD", "AUD", "SGD", "JPY"];

export function DashboardPage() {
  const [baseCurrency, setBaseCurrency] = useState("USD");

  const summary = useQuery({
    queryKey: ["summary", baseCurrency],
    queryFn: () => fetchSummary(baseCurrency),
  });
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
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="font-display text-xl font-semibold text-ink">
            Org pay snapshot
          </h2>
          <p className="text-sm text-slate-600">
            Native totals stay per currency; rollup uses live Frankfurter FX.
          </p>
        </div>
        <label className="block text-sm">
          <span className="mb-1 block text-xs font-medium uppercase tracking-wide text-slate-500">
            Rollup currency
          </span>
          <select
            value={baseCurrency}
            onChange={(e) => setBaseCurrency(e.target.value)}
            className="rounded-md border border-slate-200 bg-white px-3 py-2 outline-none ring-accent focus:ring-2"
          >
            {BASE_OPTIONS.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
      </div>

      {data.fx_error && (
        <ErrorBox
          message={`Live FX unavailable (${data.fx_error}). Per-currency totals still shown.`}
        />
      )}

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article className="rounded-xl bg-ink px-5 py-6 text-white shadow-sm">
          <p className="text-xs uppercase tracking-wider text-teal-200">
            Active headcount
          </p>
          <p className="mt-2 font-display text-4xl font-semibold">
            {data.headcount.toLocaleString()}
          </p>
          {data.total_in_base != null && data.base_currency && !data.fx_error ? (
            <p className="mt-3 text-sm text-slate-200">
              Payroll rollup ≈{" "}
              <span className="font-semibold text-white">
                {formatMoney(data.total_in_base, data.base_currency)}
              </span>
              {data.fx_as_of ? ` · FX ${data.fx_as_of}` : ""}
            </p>
          ) : (
            <p className="mt-2 text-sm text-slate-300">
              Choose a rollup currency for a single org-wide total.
            </p>
          )}
        </article>

        {data.total_in_base != null &&
          data.avg_in_base != null &&
          data.base_currency &&
          !data.fx_error && (
            <article className="rounded-xl bg-accent px-5 py-5 text-white shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wider text-teal-100">
                Avg in {data.base_currency}
              </p>
              <p className="mt-2 text-2xl font-semibold">
                {formatMoney(data.avg_in_base, data.base_currency)}
              </p>
              <p className="mt-1 text-sm text-teal-50">
                Live rates via {data.fx_source ?? "FX provider"}
              </p>
            </article>
          )}

        {data.by_currency.slice(0, 4).map((row) => (
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
