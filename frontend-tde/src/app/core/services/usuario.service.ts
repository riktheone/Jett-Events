import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario } from '../../models/usuario.model';
import { environment } from '../../../environments/environment';

type UsuarioPayload = { cpf: string; nome: string; email: string; senha: string };

@Injectable({ providedIn: 'root' })
export class UsuarioService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiUrl}/usuario`;

  obterTodos(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.base);
  }

  salvar(payload: UsuarioPayload): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.base, payload);
  }

  atualizar(id: number, payload: UsuarioPayload): Observable<{ msg: string }> {
    return this.http.put<{ msg: string }>(`${this.base}/${id}`, payload);
  }

  remover(id: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${this.base}/${id}`);
  }

  promover(id: number): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(`${this.base}/promover/${id}`, {});
  }
}
