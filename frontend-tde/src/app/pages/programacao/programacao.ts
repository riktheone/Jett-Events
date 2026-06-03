import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink, ActivatedRoute } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { EventoService } from '../../core/services/evento.service';
import { MinicursoService } from '../../core/services/minicurso.service';
import { Palestra } from '../../models/palestra.model';
import { Minicurso } from '../../models/minicurso.model';

@Component({
  selector: 'app-programacao',
  imports: [RouterLink],
  templateUrl: './programacao.html',
})
export class Programacao implements OnInit {
  readonly auth = inject(AuthService);
  private readonly eventoSvc = inject(EventoService);
  private readonly minicursoSvc = inject(MinicursoService);
  private readonly route = inject(ActivatedRoute);

  readonly palestras = signal<Palestra[]>([]);
  readonly minicursos = signal<Minicurso[]>([]);
  readonly nomeEvento = signal('');
  readonly eventoId = signal(0);
  readonly erro = signal('');
  readonly carregando = signal(false);

  ngOnInit(): void {
    const id = +this.route.snapshot.params['id'];
    this.eventoId.set(id);
    this.carregando.set(true);
    this.eventoSvc.obterProgramacao(id).subscribe({
      next: prog => {
        this.palestras.set(prog.palestras ?? []);
        this.minicursos.set((prog.minicursos ?? []).map((mc: any) => ({ ...mc, inscritos: mc.inscritos ?? [] })));
        this.carregando.set(false);
      },
      error: err => { this.erro.set(apiError(err)); this.carregando.set(false); }
    });
    this.eventoSvc.obterPorId(id).subscribe({
      next: ev => this.nomeEvento.set(ev.nome)
    });
  }

  estaInscrito(mc: Minicurso): boolean {
    if (!mc.inscritos || !mc.inscritos.length) return false;
    const uid = this.auth.usuario()!.id;
    return mc.inscritos.some((i: any) => i === uid || i?.id === uid);
  }

  async inscreverMinicurso(mc: Minicurso): Promise<void> {
    try {
      const resp = await firstValueFrom(
        this.minicursoSvc.inscrever(mc.id, this.auth.usuario()!.id)
      );
      alert(resp.msg || 'Inscrição realizada!');
      this.ngOnInit();
    } catch (err) { alert(apiError(err)); }
  }

  async cancelarMinicurso(mc: Minicurso): Promise<void> {
    if (!confirm(`Cancelar inscrição em "${mc.nome}"?`)) return;
    try {
      const resp = await firstValueFrom(
        this.minicursoSvc.removerInscricao(mc.id, this.auth.usuario()!.id)
      );
      alert(resp.msg || 'Inscrição cancelada.');
      this.ngOnInit();
    } catch (err) { alert(apiError(err)); }
  }
}
