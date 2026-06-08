import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { UsuarioService } from '../../core/services/usuario.service';
import { apiError, hashSenha } from '../../core/services/auth.service';
import { formatCpf, isCpfComplete, onlyCpfDigits } from '../../core/utils/cpf.util';

@Component({
  selector: 'app-cadastro',
  imports: [FormsModule, RouterLink],
  templateUrl: './cadastro.html',
})
export class Cadastro {
  private readonly usuarioSvc = inject(UsuarioService);
  private readonly router = inject(Router);

  cpf = '';
  nome = '';
  email = '';
  senha = '';
  readonly erro = signal('');
  readonly ok = signal('');
  readonly carregando = signal(false);

  formatarCPF(event: Event): void {
    const input = event.target as HTMLInputElement;
    const formatted = formatCpf(input.value);
    this.cpf = formatted;
    input.value = formatted;
  }

  async cadastrar(): Promise<void> {
    if (!this.nome || !this.cpf || !this.email || !this.senha) {
      this.erro.set('Preencha todos os campos.'); return;
    }
    if (!isCpfComplete(this.cpf)) { this.erro.set('CPF deve conter 11 digitos.'); return; }
    if (this.senha.length < 6) { this.erro.set('Senha com no mínimo 6 caracteres.'); return; }
    this.carregando.set(true);
    this.erro.set('');
    try {
      const hash = await hashSenha(this.senha);
      const resp = await firstValueFrom(
        this.usuarioSvc.salvar({ cpf: onlyCpfDigits(this.cpf), nome: this.nome, email: this.email, senha: hash })
      );
      this.ok.set(resp.msg || 'Cadastro realizado! Faça login.');
      setTimeout(() => this.router.navigate(['/login']), 1500);
    } catch (err) {
      this.erro.set(apiError(err));
    } finally {
      this.carregando.set(false);
    }
  }
}
