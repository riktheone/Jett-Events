export function dateInputValue(value: string | null | undefined): string {
  const raw = String(value ?? '').trim();
  if (!raw) return '';
  return raw.replace('T', ' ').split(' ')[0].slice(0, 10);
}

export function timeInputValue(value: string | null | undefined): string {
  const raw = String(value ?? '').trim().replace('T', ' ');
  if (!raw) return '';
  const time = raw.includes(' ') ? raw.split(' ')[1] : raw;
  return time.slice(0, 5);
}
