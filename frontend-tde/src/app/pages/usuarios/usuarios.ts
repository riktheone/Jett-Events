import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { UsuarioService } from '../../core/services/usuario.service';
import { Usuario } from '../../models/usuario.model';
import { DialogService } from '../../shared/dialog/dialog.service';

@Component({
  selector: 'app-usuarios',
  imports: [RouterLink],
  templateUrl: './usuarios.html',
})
export class Usuarios implements OnInit {
  readonly auth = inject(AuthService);
  private readonly usuarioSvc = inject(UsuarioService);
  private readonly dialog = inject(DialogService);

  readonly lista = signal<Usuario[]>([]);
  readonly erro = signal('');
  readonly carregando = signal(false);

  ngOnInit(): void { this.carregar(); }

  carregar(): void {
    this.usuarioSvc.obterTodos().subscribe({
      next: us => this.lista.set(us.map(u => ({ ...u, administrador: Boolean(u.administrador) }))),
      error: err => this.erro.set(apiError(err))
    });
  }

  async remover(u: Usuario): Promise<void> {
    const confirmado = await this.dialog.confirm(`Remover ${u.nome}?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(this.usuarioSvc.remover(u.id));
      await this.dialog.alert(resp.msg || 'Usuario removido.', 'Usuario removido', 'success');
      this.carregar();
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro ao remover', 'error'); }
  }

  async promover(u: Usuario): Promise<void> {
    const confirmado = await this.dialog.confirm(`Promover ${u.nome} a administrador?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(this.usuarioSvc.promover(u.id));
      await this.dialog.alert(resp.msg || 'Promovido!', 'Usuario promovido', 'success');
      this.carregar();
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro ao promover', 'error'); }
  }

  outrosUsuarios(): Usuario[] {
    return this.lista().filter(u => u.id !== this.auth.usuario()!.id);
  }
}
