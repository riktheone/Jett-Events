import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { EventoService } from '../../../core/services/evento.service';
import { apiError } from '../../../core/services/auth.service';
import { formatCpf, isCpfComplete, onlyCpfDigits } from '../../../core/utils/cpf.util';
import { dateInputValue } from '../../../core/utils/date.util';
import { Evento } from '../../../models/evento.model';

@Component({
  selector: 'app-evento-form',
  imports: [FormsModule, RouterLink],
  templateUrl: './evento-form.html',
})
export class EventoForm implements OnInit {
  private readonly eventoSvc = inject(EventoService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  readonly editando = signal(false);
  id = 0;
  nome = ''; descricao = '';
  dt_inicio = ''; dt_fim = ''; dt_limite_inscricao = '';
  numero_vagas = 0;
  nome_responsavel = ''; cpf_responsavel = ''; email_responsavel = '';
  readonly erro = signal('');
  readonly ok = signal('');
  readonly carregando = signal(false);

  ngOnInit(): void {
    const idParam = this.route.snapshot.params['id'];
    if (idParam) {
      this.editando.set(true);
      this.id = +idParam;
      this.eventoSvc.obterPorId(this.id).subscribe({
        next: ev => this.preencher(ev),
        error: err => this.erro.set(apiError(err))
      });
    }
  }

  private preencher(ev: Evento): void {
    this.nome = ev.nome; this.descricao = ev.descricao ?? '';
    this.dt_inicio = dateInputValue(ev.dt_inicio); this.dt_fim = dateInputValue(ev.dt_fim);
    this.dt_limite_inscricao = dateInputValue(ev.dt_limite_inscricao);
    this.numero_vagas = ev.numero_vagas;
    this.nome_responsavel = ev.nome_responsavel;
    this.cpf_responsavel = formatCpf(ev.cpf_responsavel);
    this.email_responsavel = ev.email_responsavel;
  }

  formatarCPFResponsavel(event: Event): void {
    const input = event.target as HTMLInputElement;
    const formatted = formatCpf(input.value);
    this.cpf_responsavel = formatted;
    input.value = formatted;
  }

  async salvar(): Promise<void> {
    if (!this.nome || !this.descricao || !this.dt_inicio || !this.dt_fim || !this.dt_limite_inscricao ||
        !this.numero_vagas || !this.nome_responsavel || !this.cpf_responsavel || !this.email_responsavel) {
      this.erro.set('Preencha todos os campos obrigatórios.'); return;
    }
    if (!isCpfComplete(this.cpf_responsavel)) { this.erro.set('CPF do responsavel deve conter 11 digitos.'); return; }
    const payload = {
      nome: this.nome, descricao: this.descricao,
      dt_inicio: this.dt_inicio, dt_fim: this.dt_fim,
      dt_limite_inscricao: this.dt_limite_inscricao,
      numero_vagas: this.numero_vagas,
      nome_responsavel: this.nome_responsavel,
      cpf_responsavel: onlyCpfDigits(this.cpf_responsavel),
      email_responsavel: this.email_responsavel
    };
    this.carregando.set(true); this.erro.set('');
    try {
      const obs = this.editando()
        ? this.eventoSvc.atualizar(this.id, payload)
        : this.eventoSvc.salvar(payload);
      const resp = await firstValueFrom(obs);
      this.ok.set(resp.msg || 'Evento salvo!');
      setTimeout(() => this.router.navigate(['/eventos']), 1200);
    } catch (err) {
      this.erro.set(apiError(err));
    } finally {
      this.carregando.set(false);
    }
  }
}
