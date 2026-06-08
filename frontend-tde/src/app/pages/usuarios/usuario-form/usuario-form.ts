import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { UsuarioService } from '../../../core/services/usuario.service';
import { apiError, hashSenha } from '../../../core/services/auth.service';
import { formatCpf, isCpfComplete, onlyCpfDigits } from '../../../core/utils/cpf.util';

@Component({
  selector: 'app-usuario-form',
  imports: [FormsModule, RouterLink],
  templateUrl: './usuario-form.html',
})
export class UsuarioForm implements OnInit {
  private readonly usuarioSvc = inject(UsuarioService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  readonly editando = signal(false);
  id = 0;
  cpf = '';
  nome = '';
  email = '';
  senha = '';
  novaSenha = '';
  readonly erro = signal('');
  readonly ok = signal('');
  readonly carregando = signal(false);

  ngOnInit(): void {
    const idParam = this.route.snapshot.params['id'];
    if (idParam) {
      this.editando.set(true);
      this.id = +idParam;
      this.usuarioSvc.obterTodos().subscribe({
        next: lista => {
          const u = lista.find(x => x.id === this.id);
          if (u) { this.cpf = formatCpf(u.cpf); this.nome = u.nome; this.email = u.email; }
        }
      });
    }
  }

  formatarCPF(event: Event): void {
    const input = event.target as HTMLInputElement;
    const f = formatCpf(input.value);
    this.cpf = f;
    input.value = f;
  }

  async salvar(): Promise<void> {
    if (!this.nome || !this.email) { this.erro.set('Nome e e-mail são obrigatórios.'); return; }
    if (!isCpfComplete(this.cpf)) { this.erro.set('CPF deve conter 11 digitos.'); return; }
    this.carregando.set(true);
    this.erro.set('');
    try {
      const cpf = onlyCpfDigits(this.cpf);
      if (this.editando()) {
        const senha = this.novaSenha ? await hashSenha(this.novaSenha) : 'sem_alteracao';
        const resp = await firstValueFrom(
          this.usuarioSvc.atualizar(this.id, { cpf, nome: this.nome, email: this.email, senha })
        );
        this.ok.set(resp.msg || 'Usuário atualizado!');
      } else {
        if (!this.cpf || !this.senha) { this.erro.set('Preencha CPF e senha.'); this.carregando.set(false); return; }
        if (this.senha.length < 6) { this.erro.set('Senha mínimo 6 caracteres.'); this.carregando.set(false); return; }
        const hash = await hashSenha(this.senha);
        const resp = await firstValueFrom(
          this.usuarioSvc.salvar({ cpf, nome: this.nome, email: this.email, senha: hash })
        );
        this.ok.set(resp.msg || 'Usuário cadastrado!');
      }
      setTimeout(() => this.router.navigate(['/usuarios']), 1200);
    } catch (err) {
      this.erro.set(apiError(err));
    } finally {
      this.carregando.set(false);
    }
  }
}
