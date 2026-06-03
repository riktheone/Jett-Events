import { Component, inject, signal, OnInit } from '@angular/core';
import { EventoService } from '../../core/services/evento.service';
import { MinicursoService } from '../../core/services/minicurso.service';
import { apiError } from '../../core/services/auth.service';
import { Evento } from '../../models/evento.model';
import { Minicurso } from '../../models/minicurso.model';

interface EventoComInscritos extends Evento { inscritos: any[]; }
interface MinicursoComInscritos extends Minicurso { _inscritos: any[]; }

@Component({
  selector: 'app-inscritos',
  imports: [],
  templateUrl: './inscritos.html',
})
export class Inscritos implements OnInit {
  private readonly eventoSvc = inject(EventoService);
  private readonly minicursoSvc = inject(MinicursoService);

  readonly eventos = signal<EventoComInscritos[]>([]);
  readonly minicursos = signal<MinicursoComInscritos[]>([]);
  readonly erro = signal('');

  ngOnInit(): void {
    this.eventoSvc.obterTodos().subscribe({
      next: lista => {
        const ev = lista.map(e => ({ ...e, inscritos: [] as any[] }));
        this.eventos.set(ev);
        ev.forEach(e =>
          this.eventoSvc.obterInscritos(e.id).subscribe({
            next: ins => {
              const updated = this.eventos().map(x => x.id === e.id ? { ...x, inscritos: ins } : x);
              this.eventos.set(updated);
            }
          })
        );
      },
      error: err => this.erro.set(apiError(err))
    });

    this.minicursoSvc.obterTodos().subscribe({
      next: lista => {
        const mc = lista.map(m => ({ ...m, _inscritos: [] as any[] }));
        this.minicursos.set(mc);
        mc.forEach(m =>
          this.minicursoSvc.obterInscritos(m.id).subscribe({
            next: ins => {
              const updated = this.minicursos().map(x => x.id === m.id ? { ...x, _inscritos: ins } : x);
              this.minicursos.set(updated);
            }
          })
        );
      }
    });
  }
}
