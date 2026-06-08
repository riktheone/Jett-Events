import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { PalestraService } from '../../../core/services/palestra.service';
import { EventoService } from '../../../core/services/evento.service';
import { apiError } from '../../../core/services/auth.service';
import { dateInputValue, timeInputValue } from '../../../core/utils/date.util';
import { Palestra } from '../../../models/palestra.model';
import { Evento } from '../../../models/evento.model';

@Component({
  selector: 'app-palestra-form',
  imports: [FormsModule, RouterLink],
  templateUrl: './palestra-form.html',
})
export class PalestraForm implements OnInit {
  private readonly palestraSvc = inject(PalestraService);
  private readonly eventoSvc = inject(EventoService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  readonly editando = signal(false);
  id = 0;
  nome = '';
  descricao = '';
  dt_palestra = '';
  horario_inicio_palestra = '';
  horario_fim_palestra = '';
  nome_palestrante = '';
  minicurriculo_palestrante = '';
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
      this.palestraSvc.obterPorId(this.id).subscribe({
        next: p => this.preencher(p),
        error: err => this.erro.set(apiError(err))
      });
    }
  }

  private preencher(p: Palestra): void {
    this.nome = p.nome;
    this.descricao = p.descricao ?? '';
    this.dt_palestra = dateInputValue(p.dt_palestra);
    this.horario_inicio_palestra = timeInputValue(p.horario_inicio_palestra);
    this.horario_fim_palestra = timeInputValue(p.horario_fim_palestra);
    this.nome_palestrante = p.nome_palestrante;
    this.minicurriculo_palestrante = p.minicurriculo_palestrante ?? '';
    this.id_evento = p.id_evento;
  }

  async salvar(): Promise<void> {
    if (!this.id_evento || !this.nome || !this.descricao || !this.dt_palestra ||
        !this.horario_inicio_palestra || !this.horario_fim_palestra ||
        !this.nome_palestrante || !this.minicurriculo_palestrante) {
      this.erro.set('Preencha todos os campos obrigatorios.');
      return;
    }
    const payload = {
      nome: this.nome,
      descricao: this.descricao,
      dt_palestra: this.dt_palestra,
      horario_inicio_palestra: this.horario_inicio_palestra,
      horario_fim_palestra: this.horario_fim_palestra,
      nome_palestrante: this.nome_palestrante,
      minicurriculo_palestrante: this.minicurriculo_palestrante,
      id_evento: this.id_evento
    };
    this.carregando.set(true);
    this.erro.set('');
    try {
      const obs = this.editando()
        ? this.palestraSvc.atualizar(this.id, payload)
        : this.palestraSvc.salvar(payload);
      const resp = await firstValueFrom(obs);
      this.ok.set(resp.msg || 'Palestra salva!');
      setTimeout(() => this.router.navigate(['/palestras']), 1200);
    } catch (err) {
      this.erro.set(apiError(err));
    } finally {
      this.carregando.set(false);
    }
  }
}
