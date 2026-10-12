const UNITS = {
  ru: { min: "мин", h: "ч", d: "дн", mo: "мес", y: "г" },
  en: { min: "min", h: "h", d: "d", mo: "mo", y: "y" },
};

export function formatInterval(minutes: number, language: string): string {
  const u = language === "ru" ? UNITS.ru : UNITS.en;

  if (minutes < 60) return `${minutes} ${u.min}`;
  if (minutes < 24 * 60) return `${Math.round(minutes / 60)} ${u.h}`;

  const days = Math.round(minutes / (24 * 60));
  if (days < 30) return `${days} ${u.d}`;
  if (days < 365) return `${Math.round(days / 30)} ${u.mo}`;
  return `${(days / 365).toFixed(1)} ${u.y}`;
}