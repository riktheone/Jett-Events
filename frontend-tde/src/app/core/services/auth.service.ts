import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { Usuario } from '../../models/usuario.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly TOKEN_KEY = 'jett_token';
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);

  private readonly _usuario = signal<Usuario | null>(null);
  readonly usuario = this._usuario.asReadonly();
  readonly isLoggedIn = computed(() => this._usuario() !== null);
  readonly isAdmin = computed(() => this._usuario()?.administrador === true);

  getToken(): string | null {
    return sessionStorage.getItem(this.TOKEN_KEY);
  }

  private setToken(token: string): void {
    sessionStorage.setItem(this.TOKEN_KEY, token);
  }

  clearToken(): void {
    sessionStorage.removeItem(this.TOKEN_KEY);
  }

  async tryRestoreSession(): Promise<void> {
    if (!this.getToken()) return;
    try {
      const u = await firstValueFrom(
        this.http.get<Usuario>(`${environment.apiUrl}/usuario/porToken`)
      );
      u.administrador = Boolean(u.administrador);
      this._usuario.set(u);
    } catch {
      this.clearToken();
    }
  }

  async login(cpf: string, senha: string): Promise<void> {
    const hash = await hashSenha(senha);
    const resp = await firstValueFrom(
      this.http.post<{ token_jwt: string }>(`${environment.apiUrl}/usuario/logar`, { cpf, senha: hash })
    );
    this.setToken(resp.token_jwt);
    const u = await firstValueFrom(
      this.http.get<Usuario>(`${environment.apiUrl}/usuario/porToken`)
    );
    u.administrador = Boolean(u.administrador);
    this._usuario.set(u);
  }

  logout(): void {
    this.clearToken();
    this._usuario.set(null);
    this.router.navigate(['/login']);
  }

  updateUsuario(partial: Partial<Pick<Usuario, 'nome' | 'email'>>): void {
    const current = this._usuario();
    if (current) this._usuario.set({ ...current, ...partial });
  }
}

export async function hashSenha(senha: string): Promise<string> {
  const data = new TextEncoder().encode(senha);
  const buffer = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(buffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

export function apiError(err: any): string {
  if (!err) return 'Sem resposta do servidor. Verifique se o backend está rodando.';
  if (err?.error?.msg) return err.error.msg;
  if (err?.status === 401) return 'Sessão expirada. Faça login novamente.';
  if (err?.status === 403) return 'Você não tem permissão para esta ação.';
  if (err?.status === 422) return 'Dados inválidos. Verifique os campos.';
  if (err?.status === 500) return 'Erro interno no servidor.';
  return `Erro inesperado (HTTP ${err?.status ?? '?'}).`;
}

export function formatCPF(value: string): string {
  const d = value.replace(/\D/g, '').slice(0, 11);
  return d
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
}
