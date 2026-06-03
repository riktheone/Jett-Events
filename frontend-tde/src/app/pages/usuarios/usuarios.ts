import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { UsuarioService } from '../../core/services/usuario.service';
import { Usuario } from '../../models/usuario.model';

@Component({
  selector: 'app-usuarios',
  imports: [RouterLink],
  templateUrl: './usuarios.html',
})
export class Usuarios implements OnInit {
  readonly auth = inject(AuthService);
  private readonly usuarioSvc = inject(UsuarioService);

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
    if (!confirm(`Remover ${u.nome}?`)) return;
    try {
      const resp = await firstValueFrom(this.usuarioSvc.remover(u.id));
      alert(resp.msg || 'Usuário removido.');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }

  async promover(u: Usuario): Promise<void> {
    if (!confirm(`Promover ${u.nome} a administrador?`)) return;
    try {
      const resp = await firstValueFrom(this.usuarioSvc.promover(u.id));
      alert(resp.msg || 'Promovido!');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }

  outrosUsuarios(): Usuario[] {
    return this.lista().filter(u => u.id !== this.auth.usuario()!.id);
  }
}
