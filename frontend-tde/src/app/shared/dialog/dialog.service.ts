import { Injectable, signal } from '@angular/core';

export type DialogTone = 'info' | 'success' | 'error' | 'warning';

export interface DialogState {
  title: string;
  message: string;
  tone: DialogTone;
  confirmText: string;
  cancelText: string;
  showCancel: boolean;
}

@Injectable({ providedIn: 'root' })
export class DialogService {
  readonly state = signal<DialogState | null>(null);
  private resolver: ((confirmed: boolean) => void) | null = null;

  alert(message: string, title = 'Aviso', tone: DialogTone = 'info'): Promise<void> {
    return new Promise(resolve => {
      this.open({
        title,
        message,
        tone,
        confirmText: 'OK',
        cancelText: '',
        showCancel: false
      }, () => resolve());
    });
  }

  confirm(
    message: string,
    title = 'Confirmar acao',
    confirmText = 'Confirmar',
    cancelText = 'Cancelar',
    tone: DialogTone = 'warning'
  ): Promise<boolean> {
    return new Promise(resolve => {
      this.open({ title, message, tone, confirmText, cancelText, showCancel: true }, resolve);
    });
  }

  close(confirmed: boolean): void {
    const resolve = this.resolver;
    this.resolver = null;
    this.state.set(null);
    resolve?.(confirmed);
  }

  private open(state: DialogState, resolver: (confirmed: boolean) => void): void {
    this.resolver?.(false);
    this.resolver = resolver;
    this.state.set(state);
  }
}
