/* =============================================
   JETT EVENTS - App AngularJS
   Trabalho ADS 3° Semestre
   — Integração real com backend Flask (localhost:5000)
============================================= */

var app = angular.module('jettEventsApp', []);

/* ---- Filtro: inicial do nome ---- */
app.filter('ini', function() {
  return function(v) { return v ? v.charAt(0).toUpperCase() : '?'; };
});

/* =============================================
   CONSTANTE: URL base do backend
============================================= */
app.constant('API', 'http://localhost:5000/api/v1');

/* =============================================
   FACTORY - TokenService
   Guarda/recupera o JWT em sessionStorage
============================================= */
app.factory('TokenService', function() {
  return {
    set: function(t)  { sessionStorage.setItem('jett_token', t); },
    get: function()   { return sessionStorage.getItem('jett_token'); },
    del: function()   { sessionStorage.removeItem('jett_token'); },
    header: function(){ return { Authorization: sessionStorage.getItem('jett_token') || '' }; }
  };
});

/* =============================================
   FACTORY - HashService
   SHA-256 simples via SubtleCrypto
============================================= */
app.factory('HashService', function($q) {
  return {
    sha256: function(str) {
      var defer = $q.defer();
      var buf = new TextEncoder().encode(str);
      crypto.subtle.digest('SHA-256', buf).then(function(hash) {
        var hex = Array.from(new Uint8Array(hash))
          .map(function(b){ return ('00'+b.toString(16)).slice(-2); })
          .join('')
          .toUpperCase();
        defer.resolve(hex);
      }).catch(function(e){ defer.resolve(str); /* fallback */ });
      return defer.promise;
    }
  };
});

/* =============================================
   FACTORY - ApiErro
   Traduz status HTTP para mensagem amigável
============================================= */
app.factory('ApiErro', function() {
  return function(resp) {
    if (!resp) return 'Sem resposta do servidor. Verifique se o backend está rodando.';
    if (resp.data && resp.data.msg) return resp.data.msg;
    if (resp.status === 401) return 'Sessão expirada. Faça login novamente.';
    if (resp.status === 403) return 'Você não tem permissão para esta ação.';
    if (resp.status === 422) return 'Dados inválidos. Verifique os campos.';
    if (resp.status === 500) return 'Erro interno no servidor.';
    return 'Erro inesperado (HTTP ' + resp.status + ').';
  };
});

/* =============================================
   CONTROLLER - NavController
============================================= */
app.controller('NavController', function($scope, $rootScope, TokenService) {
  $scope.$watch(function(){ return $rootScope.sessao; }, function(v){ $scope.sessao = v; });
  $scope.logout = function() {
    TokenService.del();
    $rootScope.sessao = null;
    $rootScope.$broadcast('navegar', 'login');
  };
});

/* =============================================
   CONTROLLER - AppController
============================================= */
app.controller('AppController', function(
  $scope, $rootScope, $http, $q,
  API, TokenService, HashService, ApiErro
) {

  /* ---- Estado inicial ---- */
  $scope.tela     = 'login';
  $scope.me       = null;
  $scope.editando = false;
  $scope.carregando = false;

  /* ---- Formulários ---- */
  $scope.lf  = {};
  $scope.cf  = {};
  $scope.ef  = {};
  $scope.rsf = {};
  $scope.uf  = {};
  $scope.evf = {};
  $scope.plf = {};
  $scope.mcf = {};
  $scope.filtro = { dt_inicio:'', dt_fim:'' };

  /* ---- Flags de edição ---- */
  $scope.editandoUsuario   = false;
  $scope.editandoEvento    = false;
  $scope.editandoPalestra  = false;
  $scope.editandoMinicurso = false;

  $rootScope.$on('navegar', function(e, dest){ $scope.ir(dest); });

  /* ---- Listas ---- */
  $scope.listaUsers      = [];
  $scope.listaEventos    = [];
  $scope.listaPalestras  = [];
  $scope.listaMinicursos = [];
  $scope.listaEventosOpcoes = []; /* dropdown em forms */

  /* ---- Atalhos HTTP com token ---- */
  function H() { return { headers: TokenService.header() }; }

  /* Mapeia resposta do backend para { ok, msg, data } */
  function ok(resp)  { return { ok:true,  data: resp.data,  msg: (resp.data && resp.data.msg) || 'OK' }; }
  function err(resp) { return { ok:false, msg: ApiErro(resp) }; }

  /* =============================================
     NAVEGAÇÃO
  ============================================= */
  var protegidas = [
    'dashboard','perfil','usuarios','novoUsuario',
    'eventos','novoEvento','palestras','novaPalestra',
    'minicursos','novoMinicurso','inscritos',
    'redefinirSenha','programacao'
  ];

  $scope.ir = function(dest) {
    $scope.lErro=$scope.cErro=$scope.cOk='';
    $scope.eErro=$scope.eOk=$scope.rsErro=$scope.rsOk='';
    $scope.ufErro=$scope.ufOk=$scope.evErro=$scope.evOk='';
    $scope.plErro=$scope.plOk=$scope.mcErro=$scope.mcOk='';
    $scope.editando = false;

    if (protegidas.indexOf(dest) !== -1 && !$scope.me) { $scope.tela='login'; return; }
    $scope.tela = dest;

    if (dest === 'usuarios')    $scope.carregarUsuarios();
    if (dest === 'eventos')   { $scope.carregarEventos(); $scope.filtrando=false; }
    if (dest === 'palestras') { $scope.carregarPalestras(); $scope.carregarEventosOpcoes(); }
    if (dest === 'minicursos'){ $scope.carregarMinicursos(); $scope.carregarEventosOpcoes(); }
    if (dest === 'inscritos') { $scope.carregarEventos(); $scope.carregarMinicursos(); }
    if (dest === 'novoEvento'    && !$scope.editandoEvento)    $scope.evf = {};
    if (dest === 'novaPalestra'  && !$scope.editandoPalestra)  { $scope.plf={}; $scope.carregarEventosOpcoes(); }
    if (dest === 'novoMinicurso' && !$scope.editandoMinicurso) { $scope.mcf={}; $scope.carregarEventosOpcoes(); }
    if (dest === 'novoUsuario'   && !$scope.editandoUsuario)   $scope.uf = { tipo:'comum' };

    if (dest !== 'novoEvento')    $scope.editandoEvento    = false;
    if (dest !== 'novaPalestra')  $scope.editandoPalestra  = false;
    if (dest !== 'novoMinicurso') $scope.editandoMinicurso = false;
    if (dest !== 'novoUsuario')   $scope.editandoUsuario   = false;
  };

  /* =============================================
     MÁSCARAS CPF
  ============================================= */
  function aplicarMascaraCPF(v) {
    v = (v||'').replace(/\D/g,'').slice(0,11);
    v = v.replace(/(\d{3})(\d)/,'$1.$2');
    v = v.replace(/(\d{3})(\d)/,'$1.$2');
    v = v.replace(/(\d{3})(\d{1,2})$/,'$1-$2');
    return v;
  }
  $scope.fmtCPFLogin = function() { $scope.lf.cpf = aplicarMascaraCPF($scope.lf.cpf); };
  $scope.fmtCPF      = function() { $scope.cf.cpf = aplicarMascaraCPF($scope.cf.cpf); };

  /* =============================================
     AUTH — LOGIN
  ============================================= */
  $scope.login = function() {
    if (!$scope.lf.cpf || !$scope.lf.senha) { $scope.lErro='Preencha CPF e senha.'; return; }
    $scope.carregando = true;
    HashService.sha256($scope.lf.senha).then(function(hash) {
      return $http.post(API+'/usuario/logar', { cpf: $scope.lf.cpf.replace(/\D/g, ''), senha: hash });
    }).then(function(resp) {
      var token = resp.data.token_jwt;
      TokenService.set(token);
      /* Busca dados do usuário logado pelo token */
      return $http.get(API+'/usuario/porToken', H());
    }).then(function(resp) {
      var u = resp.data;
      u.administrador = u.administrador === true || u.administrador === 1;
      $scope.me = u;
      $rootScope.sessao = u;
      $scope.lf = {};
      $scope.ir('dashboard');
    }).catch(function(resp) {
      $scope.lErro = ApiErro(resp);
    }).finally(function() {
      $scope.carregando = false;
    });
  };

  /* =============================================
     AUTH — CADASTRO
  ============================================= */
  $scope.cadastrar = function() {
    var f = $scope.cf;
    if (!f.nome||!f.cpf||!f.email||!f.senha){ $scope.cErro='Preencha todos os campos.'; return; }
    if (f.senha.length < 6){ $scope.cErro='Senha com no mínimo 6 caracteres.'; return; }
    $scope.carregando = true;
    HashService.sha256(f.senha).then(function(hash) {
      return $http.post(API+'/usuario', { cpf:f.cpf, nome:f.nome, email:f.email, senha:hash });
    }).then(function(resp) {
      $scope.cOk = resp.data.msg || 'Cadastro realizado! Faça login.';
      $scope.cf = {};
      setTimeout(function(){ $scope.$apply(function(){ $scope.ir('login'); }); }, 1500);
    }).catch(function(resp) {
      $scope.cErro = ApiErro(resp);
    }).finally(function() {
      $scope.carregando = false;
    });
  };

  /* =============================================
     AUTH — REDEFINIR SENHA (PUT no próprio usuário)
  ============================================= */
  $scope.redefinirSenha = function() {
    var f = $scope.rsf;
    if (!f.cpf||!f.novaSenha||!f.confirmarSenha){ $scope.rsErro='Preencha todos os campos.'; return; }
    if (f.novaSenha.length < 6){ $scope.rsErro='Nova senha deve ter no mínimo 6 caracteres.'; return; }
    if (f.novaSenha !== f.confirmarSenha){ $scope.rsErro='As senhas não coincidem.'; return; }
    /* Para redefinir: busca usuário pelo CPF (precisa estar logado ou via fluxo de suporte).
       O backend exige autenticação para PUT /usuario/{id}, então redireciona para login
       se não estiver logado, ou usa o id do usuário logado. */
    if (!$scope.me) { $scope.rsErro='Faça login para redefinir sua senha.'; return; }
    $scope.carregando = true;
    HashService.sha256(f.novaSenha).then(function(hash) {
      return $http.put(API+'/usuario/'+$scope.me.id,
        { cpf:$scope.me.cpf, nome:$scope.me.nome, email:$scope.me.email, senha:hash },
        H()
      );
    }).then(function(resp) {
      $scope.rsOk = resp.data.msg || 'Senha redefinida!';
      $scope.rsf = {};
      setTimeout(function(){ $scope.$apply(function(){ $scope.ir($scope.me?'perfil':'login'); }); }, 1800);
    }).catch(function(resp) {
      $scope.rsErro = ApiErro(resp);
    }).finally(function() {
      $scope.carregando = false;
    });
  };

  /* =============================================
     PERFIL — EDITAR DADOS
  ============================================= */
  $scope.startEdit  = function() { $scope.ef = { nome:$scope.me.nome, email:$scope.me.email }; $scope.editando=true; };
  $scope.cancelEdit = function() { $scope.editando = false; };
  $scope.saveEdit   = function() {
    if (!$scope.ef.nome||!$scope.ef.email){ $scope.eErro='Nome e e-mail são obrigatórios.'; return; }
    $scope.carregando = true;
    var payload = { cpf:$scope.me.cpf, nome:$scope.ef.nome, email:$scope.ef.email };
    /* reutiliza senha atual: envia o campo senha como hash vazio — backend mantém se igual */
    HashService.sha256($scope.ef.novaSenha || '').then(function(hash) {
      payload.senha = $scope.ef.novaSenha ? hash : $scope.me.senhaHash || hash;
      return $http.put(API+'/usuario/'+$scope.me.id, payload, H());
    }).then(function(resp) {
      $scope.me.nome  = $scope.ef.nome;
      $scope.me.email = $scope.ef.email;
      $rootScope.sessao = $scope.me;
      $scope.eOk = resp.data.msg || 'Dados atualizados!';
      $scope.editando = false;
    }).catch(function(resp) {
      $scope.eErro = ApiErro(resp);
    }).finally(function() {
      $scope.carregando = false;
    });
  };

  /* =============================================
     USUÁRIOS (admin)
  ============================================= */
  $scope.carregarUsuarios = function() {
    $http.get(API+'/usuario', H()).then(function(resp) {
      $scope.listaUsers = (resp.data || []).map(function(u){
        u.administrador = u.administrador === true || u.administrador === 1;
        return u;
      });
    }).catch(function(resp){ $scope.ufErro = ApiErro(resp); });
  };

  $scope.remover = function(u) {
    if (!confirm('Remover '+u.nome+'?')) return;
    $http.delete(API+'/usuario/'+u.id, H()).then(function(resp) {
      alert(resp.data.msg || 'Usuário removido.');
      $scope.carregarUsuarios();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  $scope.promover = function(u) {
    if (!confirm('Promover '+u.nome+' a administrador?')) return;
    $http.post(API+'/usuario/promover/'+u.id, {}, H()).then(function(resp) {
      alert(resp.data.msg || 'Promovido!');
      $scope.carregarUsuarios();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  /* rebaixar: não existe endpoint no backend; usa PUT para mudar tipo */
  $scope.rebaixar = function(u) {
    if (!confirm('Rebaixar '+u.nome+' para usuário comum?')) return;
    HashService.sha256('').then(function(hash) {
      return $http.put(API+'/usuario/'+u.id,
        { cpf:u.cpf, nome:u.nome, email:u.email, senha:hash, tipo:'comum' }, H());
    }).then(function(resp) {
      alert(resp.data.msg || 'Rebaixado!');
      $scope.carregarUsuarios();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  $scope.semOutros = function() {
    if (!$scope.listaUsers || !$scope.me) return true;
    return $scope.listaUsers.filter(function(u){ return u.id !== $scope.me.id; }).length === 0;
  };

  $scope.editarUsuario = function(u) {
    $scope.editandoUsuario = true;
    $scope.uf = { id:u.id, nome:u.nome, email:u.email, cpf:u.cpf, tipo:u.tipo };
    $scope.ir('novoUsuario');
  };

  $scope.salvarUsuario = function() {
    var f = $scope.uf;
    if (!f.nome||!f.email){ $scope.ufErro='Nome e e-mail são obrigatórios.'; return; }
    $scope.carregando = true;
    if ($scope.editandoUsuario) {
      var senhaPromise = f.novaSenha
        ? HashService.sha256(f.novaSenha)
        : $q.resolve('');
      senhaPromise.then(function(hash) {
        var payload = { cpf:f.cpf, nome:f.nome, email:f.email, senha:hash||'sem_alteracao' };
        return $http.put(API+'/usuario/'+f.id, payload, H());
      }).then(function(resp) {
        $scope.ufOk = resp.data.msg || 'Usuário atualizado!';
        setTimeout(function(){ $scope.$apply(function(){ $scope.ir('usuarios'); }); }, 1200);
      }).catch(function(resp){ $scope.ufErro = ApiErro(resp); })
        .finally(function(){ $scope.carregando = false; });
    } else {
      if (!f.cpf||!f.senha){ $scope.ufErro='Preencha CPF e senha.'; $scope.carregando=false; return; }
      if (f.senha.length < 6){ $scope.ufErro='Senha mínimo 6 caracteres.'; $scope.carregando=false; return; }
      HashService.sha256(f.senha).then(function(hash) {
        return $http.post(API+'/usuario', { cpf:f.cpf, nome:f.nome, email:f.email, senha:hash });
      }).then(function(resp) {
        $scope.ufOk = resp.data.msg || 'Usuário cadastrado!';
        setTimeout(function(){ $scope.$apply(function(){ $scope.ir('usuarios'); }); }, 1200);
      }).catch(function(resp){ $scope.ufErro = ApiErro(resp); })
        .finally(function(){ $scope.carregando = false; });
    }
  };

  /* =============================================
     EVENTOS
  ============================================= */
  $scope.carregarEventos = function() {
    $http.get(API+'/evento', H()).then(function(resp) {
      $scope.listaEventos = resp.data || [];
      /* adiciona array inscritos local para controle de UI */
      $scope.listaEventos.forEach(function(ev){ if (!ev.inscritos) ev.inscritos=[]; });
    }).catch(function(resp){ $scope.evErro = ApiErro(resp); });
  };

  $scope.carregarEventosOpcoes = function() {
    $http.get(API+'/evento', H()).then(function(resp) {
      $scope.listaEventosOpcoes = resp.data || [];
    }).catch(function(){ $scope.listaEventosOpcoes = []; });
  };

  $scope.filtrarEventos = function() {
    if (!$scope.filtro.dt_inicio||!$scope.filtro.dt_fim){ $scope.evErro='Informe data de início e fim para filtrar.'; return; }
    $scope.carregando = true;
    $http.get(API+'/evento/periodo',
      { headers: TokenService.header(), params: { dt_inicio: $scope.filtro.dt_inicio, dt_fim: $scope.filtro.dt_fim } }
    ).then(function(resp) {
      $scope.listaEventos = resp.data || [];
      $scope.filtrando = true;
      $scope.evErro = '';
    }).catch(function(resp){ $scope.evErro = ApiErro(resp); })
      .finally(function(){ $scope.carregando = false; });
  };

  $scope.limparFiltro = function() {
    $scope.filtro = { dt_inicio:'', dt_fim:'' };
    $scope.filtrando = false;
    $scope.carregarEventos();
  };

  $scope.editarEvento = function(ev) {
    $scope.editandoEvento = true;
    $scope.evf = angular.copy(ev);
    $scope.ir('novoEvento');
  };

  $scope.salvarEvento = function() {
    var f = $scope.evf;
    if (!f.nome||!f.dt_inicio||!f.dt_fim||!f.dt_limite_inscricao||!f.numero_vagas||!f.nome_responsavel||!f.cpf_responsavel||!f.email_responsavel) {
      $scope.evErro = 'Preencha todos os campos obrigatórios.'; return;
    }
    $scope.carregando = true;
    var req = $scope.editandoEvento
      ? $http.put(API+'/evento/'+f.id, f, H())
      : $http.post(API+'/evento', f, H());
    req.then(function(resp) {
      $scope.evOk = resp.data.msg || 'Evento salvo!';
      setTimeout(function(){ $scope.$apply(function(){ $scope.ir('eventos'); }); }, 1200);
    }).catch(function(resp){ $scope.evErro = ApiErro(resp); })
      .finally(function(){ $scope.carregando = false; });
  };

  $scope.removerEvento = function(ev) {
    if (!confirm('Remover o evento "'+ev.nome+'"?')) return;
    $http.delete(API+'/evento/'+ev.id, H()).then(function(resp) {
      alert(resp.data.msg || 'Evento removido.');
      $scope.carregarEventos();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  /* ---- Inscrição em evento ---- */
  $scope.inscreverEvento = function(ev) {
    $http.post(API+'/inscricao/evento',
      { id_evento: ev.id, id_usuario_participante: $scope.me.id }, H()
    ).then(function(resp) {
      alert(resp.data.msg || 'Inscrição realizada!');
      $scope.carregarEventos();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  $scope.cancelarInscricaoEvento = function(ev) {
    if (!confirm('Cancelar inscrição em "'+ev.nome+'"?')) return;
    $http.delete(API+'/inscricao/evento/'+ev.id+'/'+$scope.me.id, H()).then(function(resp) {
      alert(resp.data.msg || 'Inscrição cancelada.');
      $scope.carregarEventos();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  $scope.estaInscritoEvento = function(ev) {
    if (!ev || !ev.inscritos || !$scope.me) return false;
    return ev.inscritos.some(function(i){ return i === $scope.me.id || i.id === $scope.me.id; });
  };

  $scope.vagasRestantesEvento = function(ev) {
    if (!ev) return 0;
    var inscritos = ev.inscritos ? ev.inscritos.length : 0;
    return (ev.numero_vagas || 0) - inscritos;
  };

  /* =============================================
     PALESTRAS
  ============================================= */
  $scope.carregarPalestras = function() {
    $http.get(API+'/palestra', H()).then(function(resp) {
      $scope.listaPalestras = resp.data || [];
    }).catch(function(resp){ $scope.plErro = ApiErro(resp); });
  };

  $scope.getNomeEvento = function(id) {
    var ev = ($scope.listaEventosOpcoes || []).find(function(e){ return e.id === id; });
    return ev ? ev.nome : '—';
  };

  $scope.editarPalestra = function(pl) {
    $scope.editandoPalestra = true;
    $scope.plf = angular.copy(pl);
    $scope.carregarEventosOpcoes();
    $scope.ir('novaPalestra');
  };

  $scope.salvarPalestra = function() {
    var f = $scope.plf;
    if (!f.nome||!f.nome_palestrante||!f.dt_palestra||!f.horario_inicio_palestra||!f.horario_fim_palestra) {
      $scope.plErro = 'Preencha título, palestrante, data e horários.'; return;
    }
    $scope.carregando = true;
    var req = $scope.editandoPalestra
      ? $http.put(API+'/palestra/'+f.id, f, H())
      : $http.post(API+'/palestra', f, H());
    req.then(function(resp) {
      $scope.plOk = resp.data.msg || 'Palestra salva!';
      setTimeout(function(){ $scope.$apply(function(){ $scope.ir('palestras'); }); }, 1200);
    }).catch(function(resp){ $scope.plErro = ApiErro(resp); })
      .finally(function(){ $scope.carregando = false; });
  };

  $scope.removerPalestra = function(pl) {
    if (!confirm('Remover a palestra "'+pl.nome+'"?')) return;
    $http.delete(API+'/palestra/'+pl.id, H()).then(function(resp) {
      alert(resp.data.msg || 'Palestra removida.');
      $scope.carregarPalestras();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  /* =============================================
     MINICURSOS
  ============================================= */
  $scope.carregarMinicursos = function() {
    $http.get(API+'/minicurso', H()).then(function(resp) {
      $scope.listaMinicursos = (resp.data || []).map(function(mc){
        if (!mc.inscritos) mc.inscritos = [];
        return mc;
      });
    }).catch(function(resp){ $scope.mcErro = ApiErro(resp); });
  };

  $scope.editarMinicurso = function(mc) {
    $scope.editandoMinicurso = true;
    $scope.mcf = angular.copy(mc);
    $scope.carregarEventosOpcoes();
    $scope.ir('novoMinicurso');
  };

  $scope.salvarMinicurso = function() {
    var f = $scope.mcf;
    if (!f.nome||!f.nome_instrutor||!f.dt_minicurso||!f.horario_inicio_minicurso||!f.horario_fim_minicurso||!f.dt_limite_inscricao) {
      $scope.mcErro = 'Preencha todos os campos obrigatórios.'; return;
    }
    $scope.carregando = true;
    var req = $scope.editandoMinicurso
      ? $http.put(API+'/minicurso/'+f.id, f, H())
      : $http.post(API+'/minicurso', f, H());
    req.then(function(resp) {
      $scope.mcOk = resp.data.msg || 'Minicurso salvo!';
      setTimeout(function(){ $scope.$apply(function(){ $scope.ir('minicursos'); }); }, 1200);
    }).catch(function(resp){ $scope.mcErro = ApiErro(resp); })
      .finally(function(){ $scope.carregando = false; });
  };

  $scope.removerMinicurso = function(mc) {
    if (!confirm('Remover o minicurso "'+mc.nome+'"?')) return;
    $http.delete(API+'/minicurso/'+mc.id, H()).then(function(resp) {
      alert(resp.data.msg || 'Minicurso removido.');
      $scope.carregarMinicursos();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  $scope.inscreverMinicurso = function(mc) {
    $http.post(API+'/inscricao/minicurso',
      { id_minicurso: mc.id, id_usuario_participante: $scope.me.id }, H()
    ).then(function(resp) {
      alert(resp.data.msg || 'Inscrição realizada!');
      $scope.carregarMinicursos();
      if ($scope.tela === 'programacao') $scope.verProgramacao($scope.eventoSelecionado);
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  $scope.cancelarInscricaoMinicurso = function(mc) {
    if (!confirm('Cancelar inscrição em "'+mc.nome+'"?')) return;
    $http.delete(API+'/inscricao/minicurso/'+mc.id+'/'+$scope.me.id, H()).then(function(resp) {
      alert(resp.data.msg || 'Inscrição cancelada.');
      $scope.carregarMinicursos();
    }).catch(function(resp){ alert(ApiErro(resp)); });
  };

  $scope.estaInscritoMinicurso = function(mc) {
    if (!mc || !mc.inscritos || !$scope.me) return false;
    return mc.inscritos.some(function(i){ return i === $scope.me.id || i.id === $scope.me.id; });
  };

  $scope.vagasRestantesMinicurso = function(mc) {
    if (!mc) return 0;
    var inscritos = mc.inscritos ? mc.inscritos.length : 0;
    return (mc.numero_vagas || mc.vagas_disponiveis || 0) - inscritos;
  };

  /* =============================================
     PROGRAMAÇÃO DO EVENTO
  ============================================= */
  $scope.verProgramacao = function(ev) {
    $scope.eventoSelecionado = ev;
    $scope.carregando = true;
    $http.get(API+'/evento/programacao/'+ev.id, H()).then(function(resp) {
      $scope.programacaoPalestras  = resp.data.palestras  || [];
      $scope.programacaoMinicursos = (resp.data.minicursos || []).map(function(mc){
        if (!mc.inscritos) mc.inscritos = [];
        return mc;
      });
      $scope.ir('programacao');
    }).catch(function(resp) {
      alert(ApiErro(resp));
    }).finally(function(){ $scope.carregando = false; });
  };

  /* =============================================
     INSCRITOS — admin
     Usa os endpoints GET /inscricao/evento/{id} e
     GET /inscricao/minicurso/{id}
  ============================================= */
  $scope.carregarInscritosPorEvento = function(ev) {
    $http.get(API+'/inscricao/evento/'+ev.id, H()).then(function(resp){
      ev._inscritos = resp.data || [];
    }).catch(function(){ ev._inscritos = []; });
  };

  $scope.carregarInscritosPorMinicurso = function(mc) {
    $http.get(API+'/inscricao/minicurso/'+mc.id, H()).then(function(resp){
      mc._inscritos = resp.data || [];
    }).catch(function(){ mc._inscritos = []; });
  };

  /* Ao entrar na tela inscritos, carrega listas e dispara busca de inscritos */
  $scope.$watch('tela', function(t) {
    if (t === 'inscritos') {
      $http.get(API+'/evento', H()).then(function(resp){
        $scope.listaEventos = resp.data || [];
        $scope.listaEventos.forEach(function(ev){ $scope.carregarInscritosPorEvento(ev); });
      });
      $http.get(API+'/minicurso', H()).then(function(resp){
        $scope.listaMinicursos = resp.data || [];
        $scope.listaMinicursos.forEach(function(mc){ $scope.carregarInscritosPorMinicurso(mc); });
      });
    }
  });

  $scope.semInscritosEventos = function() {
    return ($scope.listaEventos || []).every(function(e){ return !e._inscritos || e._inscritos.length===0; });
  };
  $scope.semInscritosMinicursos = function() {
    return ($scope.listaMinicursos || []).every(function(m){ return !m._inscritos || m._inscritos.length===0; });
  };

});
