import { Routes } from '@angular/router';
import { authGuard, adminGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then(m => m.Login)
  },
  {
    path: 'cadastro',
    loadComponent: () => import('./pages/cadastro/cadastro').then(m => m.Cadastro)
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/dashboard/dashboard').then(m => m.Dashboard)
  },
  {
    path: 'perfil',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/perfil/perfil').then(m => m.Perfil)
  },
  {
    path: 'eventos',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/eventos/eventos').then(m => m.Eventos)
  },
  {
    path: 'eventos/novo',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/eventos/evento-form/evento-form').then(m => m.EventoForm)
  },
  {
    path: 'eventos/:id/editar',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/eventos/evento-form/evento-form').then(m => m.EventoForm)
  },
  {
    path: 'palestras',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/palestras/palestras').then(m => m.Palestras)
  },
  {
    path: 'palestras/novo',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/palestras/palestra-form/palestra-form').then(m => m.PalestraForm)
  },
  {
    path: 'palestras/:id/editar',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/palestras/palestra-form/palestra-form').then(m => m.PalestraForm)
  },
  {
    path: 'minicursos',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/minicursos/minicursos').then(m => m.Minicursos)
  },
  {
    path: 'minicursos/novo',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/minicursos/minicurso-form/minicurso-form').then(m => m.MinicursoForm)
  },
  {
    path: 'minicursos/:id/editar',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/minicursos/minicurso-form/minicurso-form').then(m => m.MinicursoForm)
  },
  {
    path: 'usuarios',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/usuarios/usuarios').then(m => m.Usuarios)
  },
  {
    path: 'usuarios/novo',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/usuarios/usuario-form/usuario-form').then(m => m.UsuarioForm)
  },
  {
    path: 'usuarios/:id/editar',
    canActivate: [authGuard, adminGuard],
    loadComponent: () => import('./pages/usuarios/usuario-form/usuario-form').then(m => m.UsuarioForm)
  },
  {
    path: 'inscritos',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/inscritos/inscritos').then(m => m.Inscritos)
  },
  {
    path: 'programacao/:id',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/programacao/programacao').then(m => m.Programacao)
  },
  { path: '**', redirectTo: '/login' }
];
