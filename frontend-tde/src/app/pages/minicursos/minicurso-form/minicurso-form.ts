import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { MinicursoService } from '../../../core/services/minicurso.service';
import { EventoService } from '../../../core/services/evento.service';
import { apiError } from '../../../core/services/auth.service';
import { dateInputValue, timeInputValue } from '../../../core/utils/date.util';
import { Minicurso } from '../../../models/minicurso.model';
import { Evento } from '../../../models/evento.model';

@Component({
  selector: 'app-minicurso-form',
  imports: [FormsModule, RouterLink],
  templateUrl: './minicurso-form.html',
})
export class MinicursoForm implements OnInit {
  private readonly minicursoSvc = inject(MinicursoService);
  private readonly eventoSvc = inject(EventoService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  readonly editando = signal(false);
  id = 0;
  nome = '';
  descricao = '';
  dt_minicurso = '';
  horario_inicio_minicurso = '';
  horario_fim_minicurso = '';
  nome_instrutor = '';
  minicurriculo_instrutor = '';
  dt_limite_inscricao = '';
  numero_vagas = 0;
  id_evento = 0;
  readonly eventos = signal<Evento[]>([]);
  readonly erro = signal('');
  readonly ok = signal('');
  readonly carregando = signal(false);

  ngOnInit(): void {
    this.eventoSvc.obterTodos().subscribe(ev => this.eventos.set(ev));
    const idParam = this.route.snapshot.params['id'];
    if (idParam) {
      this.editando.set(true);
      this.id = +idParam;
      this.minicursoSvc.obterPorId(this.id).subscribe({
        next: mc => this.preencher(mc),
        error: err => this.erro.set(apiError(err))
      });
    }
  }

  private preencher(mc: Minicurso): void {
    this.nome = mc.nome;
    this.descricao = mc.descricao ?? '';
    this.dt_minicurso = dateInputValue(mc.dt_minicurso);
    this.horario_inicio_minicurso = timeInputValue(mc.horario_inicio_minicurso);
    this.horario_fim_minicurso = timeInputValue(mc.horario_fim_minicurso);
    this.nome_instrutor = mc.nome_instrutor;
    this.minicurriculo_instrutor = mc.minicurriculo_instrutor ?? '';
    this.dt_limite_inscricao = dateInputValue(mc.dt_limite_inscricao);
    this.numero_vagas = mc.numero_vagas;
    this.id_evento = mc.id_evento;
  }

  async salvar(): Promise<void> {
    if (!this.id_evento || !this.nome || !this.descricao || !this.dt_minicurso ||
        !this.horario_inicio_minicurso || !this.horario_fim_minicurso ||
        !this.nome_instrutor || !this.minicurriculo_instrutor ||
        !this.dt_limite_inscricao || !this.numero_vagas) {
      this.erro.set('Preencha todos os campos obrigatorios.');
      return;
    }
    const payload = {
      nome: this.nome,
      descricao: this.descricao,
      dt_minicurso: this.dt_minicurso,
      horario_inicio_minicurso: this.horario_inicio_minicurso,
      horario_fim_minicurso: this.horario_fim_minicurso,
      nome_instrutor: this.nome_instrutor,
      minicurriculo_instrutor: this.minicurriculo_instrutor,
      dt_limite_inscricao: this.dt_limite_inscricao,
      numero_vagas: this.numero_vagas,
      id_evento: this.id_evento
    };
    this.carregando.set(true);
    this.erro.set('');
    try {
      const obs = this.editando()
        ? this.minicursoSvc.atualizar(this.id, payload)
        : this.minicursoSvc.salvar(payload);
      const resp = await firstValueFrom(obs);
      this.ok.set(resp.msg || 'Minicurso salvo!');
      setTimeout(() => this.router.navigate(['/minicursos']), 1200);
    } catch (err) {
      this.erro.set(apiError(err));
    } finally {
      this.carregando.set(false);
    }
  }
}
