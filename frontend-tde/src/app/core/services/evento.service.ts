import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Evento } from '../../models/evento.model';
import { environment } from '../../../environments/environment';

export interface Programacao {
  palestras: any[];
  minicursos: any[];
}

@Injectable({ providedIn: 'root' })
export class EventoService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiUrl}/evento`;

  obterTodos(): Observable<Evento[]> {
    return this.http.get<Evento[]>(this.base);
  }

  obterPorId(id: number): Observable<Evento> {
    return this.http.get<Evento>(`${this.base}/${id}`);
  }

  obterProgramacao(id: number): Observable<Programacao> {
    return this.http.get<Programacao>(`${this.base}/programacao/${id}`);
  }

  salvar(evento: Omit<Evento, 'id'>): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.base, evento);
  }

  atualizar(id: number, evento: Omit<Evento, 'id'>): Observable<{ msg: string }> {
    return this.http.put<{ msg: string }>(`${this.base}/${id}`, evento);
  }

  remover(id: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${this.base}/${id}`);
  }

  inscrever(idEvento: number, idUsuario: number): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(`${environment.apiUrl}/inscricao/evento`, {
      id_evento: idEvento,
      id_usuario_participante: idUsuario
    });
  }

  removerInscricao(idEvento: number, idUsuario: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${environment.apiUrl}/inscricao/evento/${idEvento}/${idUsuario}`);
  }

  obterInscritos(idEvento: number): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/inscricao/evento/${idEvento}`);
  }
}
