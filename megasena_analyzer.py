import requests
import json
from collections import Counter
from datetime import datetime
import os
import time

class MegaSenaDeepAnalyzer:

    def __init__(self):
        # API HEROKU - MAIS ESTÁVEL
        self.base_url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        self.cache_file = "megasena_cache.json"
        self.complete_file = "megasena_completo.json"
        self.all_results = []
        self.all_contests = []
        self.stats = None
        self.last_download = None
        self.last_result = None

    # -------------------------------------------------
    # DOWNLOAD DOS RESULTADOS (USANDO API HEROKU)
    # -------------------------------------------------
    def fetch_all_results(self, force_download=False):
        """
        Baixa todos os resultados usando a API Heroku
        """
        # Tenta carregar do cache primeiro
        if not force_download and self._load_cache():
            print("📂 Dados carregados do cache")
            self._calculate_stats()
            return True

        print("📥 Baixando resultados da Mega-Sena...")
        
        try:
            # A API Heroku retorna todos os concursos de uma vez!
            response = requests.get(self.base_url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                print(f"❌ Erro na API: {response.status_code}")
                return False
            
            dados = response.json()
            print(f"✅ API respondeu com {len(dados)} concursos")
            
            # Processa os dados
            self.all_contests = []
            self.all_results = []
            seen = set()
            
            for item in dados:
                concurso = item.get('concurso')
                dezenas = item.get('dezenas', [])
                data = item.get('data')
                
                if dezenas and concurso:
                    numeros = sorted([int(d) for d in dezenas])
                    game = tuple(numeros)
                    
                    if len(game) == 6 and game not in seen:
                        seen.add(game)
                        
                        contest_data = {
                            'concurso': concurso,
                            'data': data,
                            'numeros': numeros,
                            'acumulado': item.get('acumulou', False),
                            'local': item.get('local', ''),
                            'proximo_concurso': item.get('proximoConcurso'),
                            'data_proximo': item.get('dataProximoConcurso'),
                            'premiacoes': item.get('premiacoes', [])
                        }
                        
                        self.all_contests.append(contest_data)
                        self.all_results.append(numeros)
            
            # Ordena por concurso
            self.all_contests.sort(key=lambda x: x['concurso'])
            
            # Pega o último resultado
            if self.all_contests:
                self.last_result = self.all_contests[-1]
            
            print(f"✅ Processados {len(self.all_contests)} concursos válidos")
            
            # Calcula estatísticas
            self._calculate_stats()
            
            # Salva cache
            self._save_cache()
            
            # Salva arquivo completo
            self._save_complete_file()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    # -------------------------------------------------
    # PEGAR APENAS O ÚLTIMO RESULTADO (MAIS RÁPIDO)
    # -------------------------------------------------
    def get_latest_result(self):
        """
        Busca apenas o último resultado
        """
        try:
            url = f"{self.base_url}/latest"
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                data = response.json()
                dezenas = data.get('dezenas', [])
                numeros = sorted([int(d) for d in dezenas])
                
                # Processa premiações
                premiacoes = data.get('premiacoes', [])
                ganhadores_6 = 0
                ganhadores_5 = 0
                ganhadores_4 = 0
                valor_6 = 0
                
                for p in premiacoes:
                    if p.get('faixa') == 1:
                        ganhadores_6 = p.get('ganhadores', 0)
                        valor_6 = p.get('valorPremio', 0)
                    elif p.get('faixa') == 2:
                        ganhadores_5 = p.get('ganhadores', 0)
                    elif p.get('faixa') == 3:
                        ganhadores_4 = p.get('ganhadores', 0)
                
                return {
                    "concurso": data.get('concurso'),
                    "data": data.get('data'),
                    "data_proximo": data.get('dataProximoConcurso'),
                    "numeros": numeros,
                    "acumulado": data.get('acumulou', False),
                    "estimativa": data.get('valorEstimadoProximoConcurso'),
                    "acumulado_proximo": data.get('valorAcumuladoProximoConcurso'),
                    "ganhadores_6": ganhadores_6,
                    "ganhadores_5": ganhadores_5,
                    "ganhadores_4": ganhadores_4,
                    "valor_6": valor_6,
                    "local": data.get('local', ''),
                    "proximo_concurso": data.get('proximoConcurso')
                }
            return None
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar último resultado: {e}")
            return None

    # -------------------------------------------------
    # CALCULO DAS ESTATISTICAS
    # -------------------------------------------------
    def _calculate_stats(self):
        """
        Calcula todas as estatísticas com base nos resultados
        """
        print("📊 Calculando estatísticas...")

        if not self.all_results:
            print("⚠️ Sem dados para calcular estatísticas")
            return

        # Frequência dos números
        numbers = []
        for game in self.all_results:
            numbers.extend(game)

        freq = Counter(numbers)

        # Pares frequentes
        pairs = Counter()
        for game in self.all_results:
            game_sorted = sorted(game)
            for i in range(len(game_sorted)):
                for j in range(i + 1, len(game_sorted)):
                    pair = (game_sorted[i], game_sorted[j])
                    pairs[pair] += 1

        # Números quentes (mais frequentes) e frios (menos frequentes)
        all_freq = freq.most_common()
        hot = [n for n, _ in all_freq[:20]]
        cold = [n for n, _ in all_freq[-20:]]
        
        # Números médios
        if len(all_freq) > 40:
            medium = [n for n, _ in all_freq[20:40]]
        else:
            medium = [n for n in range(1, 61) if n not in hot and n not in cold]

        self.stats = {
            "frequencies": freq,
            "pairs": pairs,
            "hot_numbers": hot,
            "cold_numbers": cold,
            "medium_numbers": medium,
            "total_games": len(self.all_results),
            "last_update": datetime.now().isoformat(),
            "last_result": self.last_result['numeros'] if self.last_result else None,
            "last_contest": self.last_result['concurso'] if self.last_result else None,
            "last_date": self.last_result['data'] if self.last_result else None
        }
        
        print(f"✅ Estatísticas calculadas: {len(all_freq)} números analisados")

    # -------------------------------------------------
    # RETORNA ANALISE
    # -------------------------------------------------
    def comprehensive_analysis(self):
        """
        Retorna a análise completa
        """
        if not self.stats:
            return None
        return self.stats

    # -------------------------------------------------
    # FUNÇÕES DE CACHE
    # -------------------------------------------------
    def _save_cache(self):
        """
        Salva cache normal
        """
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "results": self.all_results,
                "contests": self.all_contests,
                "last_result": self.last_result,
                "stats": self.stats
            }
            with open(self.cache_file, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            print(f"💾 Cache salvo: {self.cache_file}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar cache: {e}")

    def _load_cache(self):
        """
        Carrega cache normal
        """
        if not os.path.exists(self.cache_file):
            return False
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.all_results = data.get("results", [])
            self.all_contests = data.get("contests", [])
            self.last_result = data.get("last_result")
            self.stats = data.get("stats")
            print(f"📂 Cache carregado: {len(self.all_results)} concursos")
            return True
        except Exception as e:
            print(f"⚠️ Erro ao carregar cache: {e}")
            return False

    def _save_complete_file(self):
        """
        Salva arquivo completo com todos os dados
        """
        try:
            complete_data = {
                'results': self.all_results,
                'contests': self.all_contests,
                'last_result': self.last_result,
                'stats': self.stats,
                'total': len(self.all_results),
                'generated_at': datetime.now().isoformat()
            }
            
            with open(self.complete_file, 'w', encoding='utf-8') as f:
                json.dump(complete_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Arquivo completo salvo: {self.complete_file}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo completo: {e}")
            return False

    # -------------------------------------------------
    # FUNÇÕES DE UTILIDADE
    # -------------------------------------------------
    def get_statistics_summary(self):
        """
        Retorna um resumo das estatísticas
        """
        if not self.stats:
            return None
        
        freq = self.stats['frequencies']
        most_common = freq.most_common(5)
        least_common = freq.most_common()[-5:]
        
        return {
            'total_concursos': self.stats['total_games'],
            'numeros_mais_frequentes': [(n, c) for n, c in most_common],
            'numeros_menos_frequentes': [(n, c) for n, c in least_common],
            'media_por_numero': sum(freq.values()) / 60
        }
    
    def get_number_frequency(self, numero):
        """
        Retorna a frequência de um número específico
        """
        if not self.stats or numero < 1 or numero > 60:
            return 0
        return self.stats['frequencies'].get(numero, 0)
    
    def check_jogo(self, jogo):
        """
        Verifica se um jogo específico já foi sorteado
        """
        if not self.all_contests:
            return None
        
        jogo_ordenado = sorted(jogo)
        
        for concurso in self.all_contests:
            if concurso['numeros'] == jogo_ordenado:
                return concurso
        
        return None

    def get_contests_by_year(self, ano):
        """
        Retorna concursos de um ano específico
        """
        if not self.all_contests:
            return []
        
        return [c for c in self.all_contests if c['data'].endswith(str(ano))]