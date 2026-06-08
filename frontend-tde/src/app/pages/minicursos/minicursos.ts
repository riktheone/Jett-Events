import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService, apiError } from '../../core/services/auth.service';
import { MinicursoService } from '../../core/services/minicurso.service';
import { EventoService, InscricaoPayload } from '../../core/services/evento.service';
import { formatCpf, isCpfComplete, onlyCpfDigits } from '../../core/utils/cpf.util';
import { Minicurso } from '../../models/minicurso.model';
import { Evento } from '../../models/evento.model';
import { DialogService } from '../../shared/dialog/dialog.service';

@Component({
  selector: 'app-minicursos',
  imports: [FormsModule, RouterLink],
  templateUrl: './minicursos.html',
})
export class Minicursos implements OnInit {
  readonly auth = inject(AuthService);
  private readonly minicursoSvc = inject(MinicursoService);
  private readonly eventoSvc = inject(EventoService);
  private readonly dialog = inject(DialogService);
  private readonly router = inject(Router);

  readonly lista = signal<Minicurso[]>([]);
  readonly eventos = signal<Evento[]>([]);
  readonly erro = signal('');
  readonly inscricaoMinicursoId = signal<number | null>(null);

  cpf_participante = '';
  nome_participante = '';
  email_participante = '';
  telefone_participante = '';

  ngOnInit(): void {
    this.carregar();
    this.eventoSvc.obterTodos().subscribe(ev => this.eventos.set(ev));
  }

  carregar(): void {
    this.minicursoSvc.obterTodos().subscribe({
      next: mc => {
        const minicursos = mc.map(item => ({ ...item, inscritos: [] }));
        this.lista.set(minicursos);
        minicursos.forEach(item => this.carregarInscritos(item.id));
      },
      error: err => this.erro.set(apiError(err))
    });
  }

  estaInscrito(mc: Minicurso): boolean {
    if (!mc.inscritos || !mc.inscritos.length) return false;
    const uid = this.auth.usuario()!.id;
    return mc.inscritos.some((i: any) => i === uid || i?.id === uid);
  }

  private carregarInscritos(idMinicurso: number): void {
    this.minicursoSvc.obterInscritos(idMinicurso).subscribe({
      next: inscritos => {
        const atualizada = this.lista().map(mc =>
          mc.id === idMinicurso ? { ...mc, inscritos } : mc
        );
        this.lista.set(atualizada);
      }
    });
  }

  nomeEvento(id: number): string {
    return this.eventos().find(e => e.id === id)?.nome ?? '-';
  }

  iniciarInscricao(mc: Minicurso): void {
    const u = this.auth.usuario()!;
    this.inscricaoMinicursoId.set(mc.id);
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

  async remover(mc: Minicurso): Promise<void> {
    const confirmado = await this.dialog.confirm(`Remover o minicurso "${mc.nome}"?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(this.minicursoSvc.remover(mc.id));
      await this.dialog.alert(resp.msg || 'Minicurso removido.', 'Minicurso removido', 'success');
      this.carregar();
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro ao remover', 'error'); }
  }

  async confirmarInscricao(mc: Minicurso): Promise<void> {
    const payload = this.montarPayloadInscricao();
    if (!payload) return;
    try {
      const resp = await firstValueFrom(this.minicursoSvc.inscrever(mc.id, payload));
      await this.dialog.alert(resp.msg || 'Inscricao realizada!', 'Inscricao realizada', 'success');
      this.cancelarFormularioInscricao();
      this.carregar();
    } catch (err) {
      await this.tratarErroInscricaoMinicurso(err, mc);
    }
  }

  async cancelarInscricao(mc: Minicurso): Promise<void> {
    const confirmado = await this.dialog.confirm(`Cancelar inscricao em "${mc.nome}"?`);
    if (!confirmado) return;
    try {
      const resp = await firstValueFrom(
        this.minicursoSvc.removerInscricao(mc.id, this.auth.usuario()!.id)
      );
      await this.dialog.alert(resp.msg || 'Inscricao cancelada.', 'Inscricao cancelada', 'success');
      this.carregar();
    } catch (err) { await this.dialog.alert(apiError(err), 'Erro ao cancelar', 'error'); }
  }

  private async tratarErroInscricaoMinicurso(err: unknown, mc: Minicurso): Promise<void> {
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
        await this.router.navigate(['/programacao', mc.id_evento]);
      }
      return;
    }
    await this.dialog.alert(mensagem, 'Erro na inscricao', 'error');
  }
}
