export function onlyCpfDigits(value: string | null | undefined): string {
  return String(value ?? '').replace(/\D/g, '').slice(0, 11);
}

export function formatCpf(value: string | null | undefined): string {
  const digits = onlyCpfDigits(value);

  return digits
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
}

export function isCpfComplete(value: string | null | undefined): boolean {
  return onlyCpfDigits(value).length === 11;
}
