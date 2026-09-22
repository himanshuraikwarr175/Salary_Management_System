import type {
  AnalyticsSummary,
  CountryBreakdown,
  DepartmentBreakdown,
  Employee,
  EmployeeList,
  SalaryHistory,
} from "./types";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body.detail ?? JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === "string" ? detail : "Request failed");
  }

  return response.json() as Promise<T>;
}

export type EmployeeQuery = {
  q?: string;
  country?: string;
  department?: string;
  page?: number;
  page_size?: number;
};

export function fetchEmployees(params: EmployeeQuery = {}) {
  const qs = new URLSearchParams();
  if (params.q) qs.set("q", params.q);
  if (params.country) qs.set("country", params.country);
  if (params.department) qs.set("department", params.department);
  qs.set("page", String(params.page ?? 1));
  qs.set("page_size", String(params.page_size ?? 20));
  return request<EmployeeList>(`/api/v1/employees?${qs.toString()}`);
}

export function fetchEmployee(id: number) {
  return request<Employee>(`/api/v1/employees/${id}`);
}

export function updateSalary(id: number, annual_salary: string, note?: string) {
  return request<Employee>(`/api/v1/employees/${id}/salary`, {
    method: "PATCH",
    body: JSON.stringify({ annual_salary, note: note || null }),
  });
}

export function fetchSalaryHistory(id: number) {
  return request<SalaryHistory[]>(`/api/v1/employees/${id}/salary-history`);
}

export function fetchSummary(baseCurrency = "USD") {
  const qs = new URLSearchParams({ base_currency: baseCurrency });
  return request<AnalyticsSummary>(`/api/v1/analytics/summary?${qs.toString()}`);
}

export function fetchByCountry() {
  return request<CountryBreakdown[]>("/api/v1/analytics/by-country");
}

export function fetchByDepartment() {
  return request<DepartmentBreakdown[]>("/api/v1/analytics/by-department");
}

export function formatMoney(amount: string | number, currency: string) {
  const value = typeof amount === "string" ? Number(amount) : amount;
  try {
    return new Intl.NumberFormat(undefined, {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(value);
  } catch {
    return `${currency} ${value.toLocaleString()}`;
  }
}
