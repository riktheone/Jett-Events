import { describe, expect, it } from 'vitest';
import { formatCpf, isCpfComplete, onlyCpfDigits } from './cpf.util';

describe('cpf.util', () => {
  it('formats 11 digits as a CPF mask', () => {
    expect(formatCpf('12345678901')).toBe('123.456.789-01');
  });

  it('keeps only the 11 CPF digits for API payloads', () => {
    expect(onlyCpfDigits('123.456.789-01')).toBe('12345678901');
  });

  it('rejects incomplete CPF values', () => {
    expect(isCpfComplete('123.456.789-0')).toBe(false);
    expect(isCpfComplete('123.456.789-01')).toBe(true);
  });
});
