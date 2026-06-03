import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { PalestraService } from '../../core/services/palestra.service';
import { EventoService } from '../../core/services/evento.service';
import { Palestra } from '../../models/palestra.model';
import { Evento } from '../../models/evento.model';

@Component({
  selector: 'app-palestras',
  imports: [RouterLink],
  templateUrl: './palestras.html',
})
export class Palestras implements OnInit {
  readonly auth = inject(AuthService);
  private readonly palestraSvc = inject(PalestraService);
  private readonly eventoSvc = inject(EventoService);

  readonly lista = signal<Palestra[]>([]);
  readonly eventos = signal<Evento[]>([]);
  readonly erro = signal('');

  ngOnInit(): void {
    this.palestraSvc.obterTodos().subscribe({
      next: p => this.lista.set(p),
      error: err => this.erro.set(apiError(err))
    });
    this.eventoSvc.obterTodos().subscribe({
      next: ev => this.eventos.set(ev)
    });
  }

  nomeEvento(id: number): string {
    return this.eventos().find(e => e.id === id)?.nome ?? '—';
  }

  async remover(p: Palestra): Promise<void> {
    if (!confirm(`Remover a palestra "${p.nome}"?`)) return;
    try {
      const resp = await firstValueFrom(this.palestraSvc.remover(p.id));
      alert(resp.msg || 'Palestra removida.');
      this.palestraSvc.obterTodos().subscribe(list => this.lista.set(list));
    } catch (err) { alert(apiError(err)); }
  }
}
