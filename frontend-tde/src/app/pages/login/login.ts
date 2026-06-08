import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService, apiError } from '../../core/services/auth.service';
import { formatCpf, isCpfComplete, onlyCpfDigits } from '../../core/utils/cpf.util';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterLink],
  templateUrl: './login.html',
})
export class Login {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  cpf = '';
  senha = '';
  readonly erro = signal('');
  readonly carregando = signal(false);

  formatarCPF(event: Event): void {
    const input = event.target as HTMLInputElement;
    const formatted = formatCpf(input.value);
    this.cpf = formatted;
    input.value = formatted;
  }

  async login(): Promise<void> {
    if (!this.cpf || !this.senha) { this.erro.set('Preencha CPF e senha.'); return; }
    if (!isCpfComplete(this.cpf)) { this.erro.set('CPF deve conter 11 digitos.'); return; }
    this.carregando.set(true);
    this.erro.set('');
    try {
      await this.auth.login(onlyCpfDigits(this.cpf), this.senha);
      this.router.navigate(['/dashboard']);
    } catch (err) {
      this.erro.set(apiError(err));
    } finally {
      this.carregando.set(false);
    }
  }
}
