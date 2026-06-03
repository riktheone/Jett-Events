import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Minicurso } from '../../models/minicurso.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class MinicursoService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiUrl}/minicurso`;

  obterTodos(): Observable<Minicurso[]> {
    return this.http.get<Minicurso[]>(this.base);
  }

  obterPorId(id: number): Observable<Minicurso> {
    return this.http.get<Minicurso>(`${this.base}/${id}`);
  }

  salvar(mc: Omit<Minicurso, 'id' | 'inscritos'>): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.base, mc);
  }

  atualizar(id: number, mc: Omit<Minicurso, 'id' | 'inscritos'>): Observable<{ msg: string }> {
    return this.http.put<{ msg: string }>(`${this.base}/${id}`, mc);
  }

  remover(id: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${this.base}/${id}`);
  }

  inscrever(idMinicurso: number, idUsuario: number): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(`${environment.apiUrl}/inscricao/minicurso`, {
      id_minicurso: idMinicurso,
      id_usuario_participante: idUsuario
    });
  }

  removerInscricao(idMinicurso: number, idUsuario: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${environment.apiUrl}/inscricao/minicurso/${idMinicurso}/${idUsuario}`);
  }

  obterInscritos(idMinicurso: number): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/inscricao/minicurso/${idMinicurso}`);
  }
}
