import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { EventoService, InscricaoPayload } from '../../core/services/evento.service';
import { formatCpf, isCpfComplete, onlyCpfDigits } from '../../core/utils/cpf.util';
import { Evento } from '../../models/evento.model';
import { DialogService } from '../../shared/dialog/dialog.service';

@Component({
  selector: 'app-eventos',
  imports: [FormsModule, RouterLink],
  templateUrl: './eventos.html',
})
export class Eventos implements OnInit {
  readonly auth = inject(AuthService);
  private readonly eventoSvc = inject(EventoService);
  private readonly dialog = inject(DialogService);

  readonly lista = signal<Evento[]>([]);
  readonly erro = signal('');
  readonly inscricaoEventoId = signal<number | null>(null);

  filtroInicio = '';
  filtroFim = '';
  cpf_participante = '';
  nome_participante = '';
  email_participante = '';
  telefone_participante = '';

  ngOnInit(): void { this.carregar(); }

  carregar(): void {
    this.eventoSvc.obterTodos().subscribe({
      next: ev => {
        const eventos = ev.map(item => ({ ...item, inscritos: [] }));
        this.lista.set(eventos);
        eventos.forEach(item => this.carregarInscritos(item.id));
      },
      error: err => this.erro.set(apiError(err))
    });
  }

  estaInscrito(ev: Evento): boolean {
    if (!ev.inscritos || !ev.inscritos.length) return false;
    const uid = this.auth.usuario()!.id;
    return ev.inscritos.some((i: any) => i === uid || i?.id === uid);
  }

  private carregarInscritos(idEvento: number): void {
    this.eventoSvc.obterInscritos(idEvento).subscribe({
      next: inscritos => {
        const atualizada = this.lista().map(ev =>
          ev.id === idEvento ? { ...ev, inscritos } : ev
        );
        this.lista.set(atualizada);
      }
    });
  }

  filtrar(): void {
    if (!this.filtroInicio || !this.filtroFim) {
      this.erro.set('Informe data de inicio e fim para filtrar.');
      return;
    }
    this.eventoSvc.obterPorPeriodo(this.filtroInicio, this.filtroFim).subscribe({
      next: ev => {
        const eventos = ev.map(item => ({ ...item, inscritos: [] }));
        this.lista.set(eventos);
        eventos.forEach(item => this.carregarInscritos(item.id));
        this.erro.set('');
      },
      error: err => this.erro.set(apiError(err))
    });
  }

  limparFiltro(): void {
    this.filtroInicio = '';
    this.filtroFim = '';
    this.carregar();
  }

  iniciarInscricao(ev: Evento): void {
    const u = this.auth.usuario()!;
    this.inscricaoEventoId.set(ev.id);
    this.cpf_participante = formatCpf(u.cpf);
    this.nome_participante = u.nome;
    this.email_participante = u.email;
    this.telefone_participante = '';
    this.erro.set('');
  }

  cancelarFormularioInscricao(): void {
    this.inscricaoEventoId.set(null);
    this.telefone_participante = '';
  }

  formatarCPFInscricao(event: Event): void {
    const input = event.target as HTMLInputElement;
    const formatted = formatCpf(input.value);
    this.cpf_participante = formatted;
    input.value = formatted;
  }

  private montarPayloadInscricao(): InscricaoPayload | null {
    if (!isCpfComplete(this.cpf_participante)) {
      this.erro.set('CPF do participante deve conter 11 digitos.');
      return null;
    }
    if (!this.nome_participante || !this.email_participante || !this.telefone_participante) {
      this.erro.set('Informe nome, e-mail e telefone do participante.');
      return null;
    }
    return {
      cpf_participante: onlyCpfDigits(this.cpf_participante),
      nome_participante: this.nome_participante,
      email_participante: this.email_participante,
      telefone_participante: this.telefone_participante,
    };
  }

  async remover(ev: Evento): Promise<void> {
    const confirmado = await this.dialog.confirm(`Remover o evento "${ev.nome}"?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(this.eventoSvc.remover(ev.id));
      await this.dialog.alert(resp.msg || 'Evento removido.', 'Evento removido', 'success');
      this.carregar();
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro ao remover', 'error'); }
  }

  async confirmarInscricao(ev: Evento): Promise<void> {
    const payload = this.montarPayloadInscricao();
    if (!payload) return;
    try {
      const resp = await firstValueFrom(this.eventoSvc.inscrever(ev.id, payload));
      await this.dialog.alert(resp.msg || 'Inscricao realizada!', 'Inscricao realizada', 'success');
      this.cancelarFormularioInscricao();
      this.carregarInscritos(ev.id);
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro na inscricao', 'error'); }
  }

  async cancelarInscricao(ev: Evento): Promise<void> {
    const confirmado = await this.dialog.confirm(`Cancelar inscricao em "${ev.nome}"?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(
        this.eventoSvc.removerInscricao(ev.id, this.auth.usuario()!.id)
      );
      await this.dialog.alert(resp.msg || 'Inscricao cancelada.', 'Inscricao cancelada', 'success');
      this.carregarInscritos(ev.id);
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro ao cancelar', 'error'); }
  }
}
