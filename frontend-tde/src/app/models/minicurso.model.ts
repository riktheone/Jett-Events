export interface Minicurso {
  id: number;
  nome: string;
  descricao: string;
  dt_minicurso: string;
  horario_inicio_minicurso: string;
  horario_fim_minicurso: string;
  nome_instrutor: string;
  minicurriculo_instrutor: string;
  dt_limite_inscricao: string;
  numero_vagas: number;
  id_evento: number;
  inscritos?: Array<number | { id: number }>;
}
