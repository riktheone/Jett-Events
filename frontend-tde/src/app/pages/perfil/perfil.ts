import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { AuthService, hashSenha, apiError } from '../../core/services/auth.service';
import { UsuarioService } from '../../core/services/usuario.service';

@Component({
  selector: 'app-perfil',
  imports: [FormsModule],
  templateUrl: './perfil.html',
})
export class Perfil {
  readonly auth = inject(AuthService);
  private readonly usuarioSvc = inject(UsuarioService);

  readonly editando = signal(false);
  nome = '';
  email = '';
  novaSenha = '';
  readonly erro = signal('');
  readonly ok = signal('');
  readonly carregando = signal(false);

  startEdit(): void {
    const u = this.auth.usuario()!;
    this.nome = u.nome;
    this.email = u.email;
    this.novaSenha = '';
    this.erro.set('');
    this.ok.set('');
    this.editando.set(true);
  }

  cancelEdit(): void { this.editando.set(false); }

  async salvar(): Promise<void> {
    if (!this.nome || !this.email) { this.erro.set('Nome e e-mail são obrigatórios.'); return; }
    this.carregando.set(true);
    this.erro.set('');
    try {
      const u = this.auth.usuario()!;
      const senha = this.novaSenha ? await hashSenha(this.novaSenha) : 'sem_alteracao';
      await firstValueFrom(
        this.usuarioSvc.atualizar(u.id, { cpf: u.cpf, nome: this.nome, email: this.email, senha })
      );
      this.auth.updateUsuario({ nome: this.nome, email: this.email });
      this.ok.set('Dados atualizados!');
      this.editando.set(false);
    } catch (err) {
      this.erro.set(apiError(err));
    } finally {
      this.carregando.set(false);
    }
  }
}
