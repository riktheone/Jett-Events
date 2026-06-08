import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { EventoService, InscricaoPayload } from '../../core/services/evento.service';
import { MinicursoService } from '../../core/services/minicurso.service';
import { formatCpf, isCpfComplete, onlyCpfDigits } from '../../core/utils/cpf.util';
import { Palestra } from '../../models/palestra.model';
import { Minicurso } from '../../models/minicurso.model';
import { DialogService } from '../../shared/dialog/dialog.service';

@Component({
  selector: 'app-programacao',
  imports: [FormsModule, RouterLink],
  templateUrl: './programacao.html',
})
export class Programacao implements OnInit {
  readonly auth = inject(AuthService);
  private readonly eventoSvc = inject(EventoService);
  private readonly minicursoSvc = inject(MinicursoService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly dialog = inject(DialogService);

  readonly palestras = signal<Palestra[]>([]);
  readonly minicursos = signal<Minicurso[]>([]);
  readonly nomeEvento = signal('');
  readonly eventoId = signal(0);
  readonly erro = signal('');
  readonly carregando = signal(false);
  readonly inscricaoEventoAberta = signal(false);
  readonly inscricaoMinicursoId = signal<number | null>(null);
  readonly inscritosEvento = signal<Array<number | { id: number }>>([]);

  cpf_evento = '';
  nome_evento = '';
  email_evento = '';
  telefone_evento = '';

  cpf_participante = '';
  nome_participante = '';
  email_participante = '';
  telefone_participante = '';

  ngOnInit(): void {
    const id = +this.route.snapshot.params['id'];
    this.eventoId.set(id);
    this.carregando.set(true);
    this.eventoSvc.obterProgramacao(id).subscribe({
      next: prog => {
        this.palestras.set(prog.palestras ?? []);
        const minicursos = (prog.minicursos ?? []).map((mc: any) => ({ ...mc, inscritos: mc.inscritos ?? [] }));
        this.minicursos.set(minicursos);
        minicursos.forEach((mc: Minicurso) => this.carregarInscritosMinicurso(mc.id));
        this.carregando.set(false);
      },
      error: err => { this.erro.set(apiError(err)); this.carregando.set(false); }
    });
    this.eventoSvc.obterPorId(id).subscribe({
      next: ev => this.nomeEvento.set(ev.nome)
    });
    this.carregarInscritosEvento(id);
  }

  estaInscritoNoEvento(): boolean {
    const inscritos = this.inscritosEvento();
    if (!inscritos.length) return false;
    const uid = this.auth.usuario()!.id;
    return inscritos.some((i: any) => i === uid || i?.id === uid);
  }

  estaInscrito(mc: Minicurso): boolean {
    if (!mc.inscritos || !mc.inscritos.length) return false;
    const uid = this.auth.usuario()!.id;
    return mc.inscritos.some((i: any) => i === uid || i?.id === uid);
  }

  private carregarInscritosEvento(idEvento: number): void {
    this.eventoSvc.obterInscritos(idEvento).subscribe({
      next: inscritos => this.inscritosEvento.set(inscritos)
    });
  }

  private carregarInscritosMinicurso(idMinicurso: number): void {
    this.minicursoSvc.obterInscritos(idMinicurso).subscribe({
      next: inscritos => {
        const atualizada = this.minicursos().map(mc =>
          mc.id === idMinicurso ? { ...mc, inscritos } : mc
        );
        this.minicursos.set(atualizada);
      }
    });
  }

  iniciarInscricaoEvento(): void {
    const u = this.auth.usuario()!;
    this.inscricaoEventoAberta.set(true);
    this.inscricaoMinicursoId.set(null);
    this.cpf_evento = formatCpf(u.cpf);
    this.nome_evento = u.nome;
    this.email_evento = u.email;
    this.telefone_evento = '';
    this.erro.set('');
  }

  cancelarFormularioEvento(): void {
    this.inscricaoEventoAberta.set(false);
    this.telefone_evento = '';
  }

  formatarCPFEvento(event: Event): void {
    const input = event.target as HTMLInputElement;
    const formatted = formatCpf(input.value);
    this.cpf_evento = formatted;
    input.value = formatted;
  }

  private montarPayloadInscricaoEvento(): InscricaoPayload | null {
    if (!isCpfComplete(this.cpf_evento)) {
      this.erro.set('CPF do participante deve conter 11 digitos.');
      return null;
    }
    if (!this.nome_evento || !this.email_evento || !this.telefone_evento) {
      this.erro.set('Informe nome, e-mail e telefone do participante.');
      return null;
    }
    return {
      cpf_participante: onlyCpfDigits(this.cpf_evento),
      nome_participante: this.nome_evento,
      email_participante: this.email_evento,
      telefone_participante: this.telefone_evento,
    };
  }

  async confirmarInscricaoEvento(): Promise<void> {
    const payload = this.montarPayloadInscricaoEvento();
    if (!payload) return;
    try {
      const resp = await firstValueFrom(this.eventoSvc.inscrever(this.eventoId(), payload));
      await this.dialog.alert(resp.msg || 'Inscricao realizada!', 'Inscricao no evento realizada', 'success');
      this.cancelarFormularioEvento();
      this.carregarInscritosEvento(this.eventoId());
    } catch (err) {
      await this.dialog.alert(apiError(err), 'Erro na inscricao do evento', 'error');
    }
  }

  async cancelarInscricaoEvento(): Promise<void> {
    const confirmado = await this.dialog.confirm(`Cancelar inscricao em "${this.nomeEvento() || 'Evento'}"?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(
        this.eventoSvc.removerInscricao(this.eventoId(), this.auth.usuario()!.id)
      );
      await this.dialog.alert(resp.msg || 'Inscricao cancelada.', 'Inscricao cancelada', 'success');
      this.carregarInscritosEvento(this.eventoId());
    } catch (err) {
      await this.dialog.alert(apiError(err), 'Erro ao cancelar', 'error');
    }
  }

  iniciarInscricaoMinicurso(mc: Minicurso): void {
    const u = this.auth.usuario()!;
    this.inscricaoMinicursoId.set(mc.id);
    this.inscricaoEventoAberta.set(false);
    this.cpf_participante = formatCpf(u.cpf);
    this.nome_participante = u.nome;
    this.email_participante = u.email;
    this.telefone_participante = '';
    this.erro.set('');
  }

  cancelarFormularioInscricao(): void {
    this.inscricaoMinicursoId.set(null);
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

  async confirmarInscricaoMinicurso(mc: Minicurso): Promise<void> {
    const payload = this.montarPayloadInscricao();
    if (!payload) return;
    try {
      const resp = await firstValueFrom(this.minicursoSvc.inscrever(mc.id, payload));
      await this.dialog.alert(resp.msg || 'Inscricao realizada!', 'Inscricao realizada', 'success');
      this.cancelarFormularioInscricao();
      this.ngOnInit();
    } catch (err) {
      await this.tratarErroInscricaoMinicurso(err);
    }
  }

  async cancelarMinicurso(mc: Minicurso): Promise<void> {
    const confirmado = await this.dialog.confirm(`Cancelar inscricao em "${mc.nome}"?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(
        this.minicursoSvc.removerInscricao(mc.id, this.auth.usuario()!.id)
      );
      await this.dialog.alert(resp.msg || 'Inscricao cancelada.', 'Inscricao cancelada', 'success');
      this.ngOnInit();
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro ao cancelar', 'error'); }
  }

  private async tratarErroInscricaoMinicurso(err: unknown): Promise<void> {
    const mensagem = apiError(err);
    if (mensagem.toLowerCase().includes('nao esta inscrito no evento')) {
      const irParaProgramacao = await this.dialog.confirm(
        'Para participar deste minicurso, primeiro faca sua inscricao no evento correspondente pela pagina de programacao.',
        'Inscricao no evento necessaria',
        'Ir para programacao',
        'Agora nao',
        'warning'
      );
      if (irParaProgramacao) {
        await this.router.navigate(['/programacao', this.eventoId()]);
      }
      return;
    }
    await this.dialog.alert(mensagem, 'Erro na inscricao', 'error');
  }
}
