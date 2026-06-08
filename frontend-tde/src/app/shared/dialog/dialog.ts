import { Component, inject } from '@angular/core';
import { DialogService } from './dialog.service';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.html',
})
export class Dialog {
  readonly dialog = inject(DialogService);

  close(confirmed: boolean): void {
    this.dialog.close(confirmed);
  }
}
