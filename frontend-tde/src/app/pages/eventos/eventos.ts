import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { EventoService } from '../../core/services/evento.service';
import { Evento } from '../../models/evento.model';

@Component({
  selector: 'app-eventos',
  imports: [RouterLink],
  templateUrl: './eventos.html',
})
export class Eventos implements OnInit {
  readonly auth = inject(AuthService);
  private readonly eventoSvc = inject(EventoService);

  readonly lista = signal<Evento[]>([]);
  readonly erro = signal('');

  ngOnInit(): void { this.carregar(); }

  carregar(): void {
    this.eventoSvc.obterTodos().subscribe({
      next: ev => this.lista.set(ev),
      error: err => this.erro.set(apiError(err))
    });
  }

  async remover(ev: Evento): Promise<void> {
    if (!confirm(`Remover o evento "${ev.nome}"?`)) return;
    try {
      const resp = await firstValueFrom(this.eventoSvc.remover(ev.id));
      alert(resp.msg || 'Evento removido.');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }

  async inscrever(ev: Evento): Promise<void> {
    try {
      const resp = await firstValueFrom(
        this.eventoSvc.inscrever(ev.id, this.auth.usuario()!.id)
      );
      alert(resp.msg || 'Inscrição realizada!');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }

  async cancelarInscricao(ev: Evento): Promise<void> {
    if (!confirm(`Cancelar inscrição em "${ev.nome}"?`)) return;
    try {
      const resp = await firstValueFrom(
        this.eventoSvc.removerInscricao(ev.id, this.auth.usuario()!.id)
      );
      alert(resp.msg || 'Inscrição cancelada.');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }
}
