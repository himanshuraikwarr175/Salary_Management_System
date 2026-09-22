export type Employee = {
  id: number;
  employee_code: string;
  full_name: string;
  email: string;
  country_code: string;
  department: string;
  job_title: string;
  currency_code: string;
  annual_salary: string;
  hire_date: string;
  is_active: boolean;
};

export type EmployeeList = {
  items: Employee[];
  total: number;
  page: number;
  page_size: number;
};

export type CurrencyAggregate = {
  currency_code: string;
  headcount: number;
  total_annual_salary: string;
  avg_annual_salary: string;
};

export type AnalyticsSummary = {
  headcount: number;
  by_currency: CurrencyAggregate[];
  base_currency?: string | null;
  total_in_base?: string | null;
  avg_in_base?: string | null;
  fx_as_of?: string | null;
  fx_source?: string | null;
  fx_error?: string | null;
};

export type CountryBreakdown = {
  country_code: string;
  currency_code: string;
  headcount: number;
  total_annual_salary: string;
  avg_annual_salary: string;
};

export type DepartmentBreakdown = {
  department: string;
  currency_code: string;
  headcount: number;
  total_annual_salary: string;
  avg_annual_salary: string;
};

export type SalaryHistory = {
  id: number;
  employee_id: number;
  old_salary: string;
  new_salary: string;
  currency_code: string;
  changed_at: string;
  note: string | null;
};
