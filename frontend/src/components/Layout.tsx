import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  [
    "rounded-md px-3 py-2 text-sm font-medium transition",
    isActive
      ? "bg-ink text-white"
      : "text-slate-600 hover:bg-white hover:text-ink",
  ].join(" ");

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="mx-auto min-h-screen max-w-6xl px-4 pb-16 pt-6 sm:px-6">
      <header className="mb-8 flex flex-col gap-4 border-b border-slate-200/80 pb-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">
            ACME Corp
          </p>
          <h1 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Salary Management
          </h1>
          <p className="mt-1 max-w-xl text-sm text-slate-600">
            Find people, update pay, and see how the org compensates by country
            and department.
          </p>
        </div>
        <nav className="flex gap-1 rounded-lg bg-white/70 p-1 shadow-sm ring-1 ring-slate-200/80">
          <NavLink to="/" end className={linkClass}>
            Dashboard
          </NavLink>
          <NavLink to="/employees" className={linkClass}>
            Employees
          </NavLink>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}
