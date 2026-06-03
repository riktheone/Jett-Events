import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Palestra } from '../../models/palestra.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PalestraService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiUrl}/palestra`;

  obterTodos(): Observable<Palestra[]> {
    return this.http.get<Palestra[]>(this.base);
  }

  obterPorId(id: number): Observable<Palestra> {
    return this.http.get<Palestra>(`${this.base}/${id}`);
  }

  salvar(palestra: Omit<Palestra, 'id'>): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.base, palestra);
  }

  atualizar(id: number, palestra: Omit<Palestra, 'id'>): Observable<{ msg: string }> {
    return this.http.put<{ msg: string }>(`${this.base}/${id}`, palestra);
  }

  remover(id: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${this.base}/${id}`);
  }
}
