export const fmtDate = (d: Date | string, opts: Intl.DateTimeFormatOptions = { year: "numeric", month: "short", day: "numeric" }) =>
  new Intl.DateTimeFormat("en-US", { timeZone: "UTC", ...opts }).format(typeof d === "string" ? new Date(d) : d);

export const fmtMonthYear = (d: Date | string) => fmtDate(d, { year: "numeric", month: "long" });

export const isoDate = (d: Date | string) => (typeof d === "string" ? new Date(d) : d).toISOString().slice(0, 10);

/** "2025-01" → "January 2025"; "2025-01-15" → "January 2025"; "2025" → "2025" */
export const fmtYm = (s?: string) => {
  if (!s) return "";
  const [y, m] = s.split("-");
  if (!m) return y;
  return new Intl.DateTimeFormat("en-US", { timeZone: "UTC", year: "numeric", month: "long" }).format(new Date(Date.UTC(+y, +m - 1, 1)));
};

export const buildDate = new Date();
