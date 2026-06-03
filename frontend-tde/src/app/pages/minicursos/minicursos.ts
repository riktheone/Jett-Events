import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { MinicursoService } from '../../core/services/minicurso.service';
import { EventoService } from '../../core/services/evento.service';
import { Minicurso } from '../../models/minicurso.model';
import { Evento } from '../../models/evento.model';

@Component({
  selector: 'app-minicursos',
  imports: [RouterLink],
  templateUrl: './minicursos.html',
})
export class Minicursos implements OnInit {
  readonly auth = inject(AuthService);
  private readonly minicursoSvc = inject(MinicursoService);
  private readonly eventoSvc = inject(EventoService);

  readonly lista = signal<Minicurso[]>([]);
  readonly eventos = signal<Evento[]>([]);
  readonly erro = signal('');

  ngOnInit(): void {
    this.carregar();
    this.eventoSvc.obterTodos().subscribe(ev => this.eventos.set(ev));
  }

  carregar(): void {
    this.minicursoSvc.obterTodos().subscribe({
      next: mc => this.lista.set(mc),
      error: err => this.erro.set(apiError(err))
    });
  }

  nomeEvento(id: number): string {
    return this.eventos().find(e => e.id === id)?.nome ?? '—';
  }

  async remover(mc: Minicurso): Promise<void> {
    if (!confirm(`Remover o minicurso "${mc.nome}"?`)) return;
    try {
      const resp = await firstValueFrom(this.minicursoSvc.remover(mc.id));
      alert(resp.msg || 'Minicurso removido.');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }

  async inscrever(mc: Minicurso): Promise<void> {
    try {
      const resp = await firstValueFrom(
        this.minicursoSvc.inscrever(mc.id, this.auth.usuario()!.id)
      );
      alert(resp.msg || 'Inscrição realizada!');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }

  async cancelarInscricao(mc: Minicurso): Promise<void> {
    if (!confirm(`Cancelar inscrição em "${mc.nome}"?`)) return;
    try {
      const resp = await firstValueFrom(
        this.minicursoSvc.removerInscricao(mc.id, this.auth.usuario()!.id)
      );
      alert(resp.msg || 'Inscrição cancelada.');
      this.carregar();
    } catch (err) { alert(apiError(err)); }
  }
}
