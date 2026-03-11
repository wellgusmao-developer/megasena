import requests
import json
from collections import Counter
from datetime import datetime
import os

class MegaSenaDeepAnalyzer:
    def __init__(self):
        self.base_url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        
        # No Cloud, usa /tmp para cache
        if os.path.exists('/tmp'):
            self.cache_file = "/tmp/megasena_cache.json"
            self.complete_file = "/tmp/megasena_completo.json"
        else:
            self.cache_file = "megasena_cache.json"
            self.complete_file = "megasena_completo.json"
        
        self.all_results = []
        self.all_contests = []
        self.stats = None
        self.last_result = None
        
        # Tenta carregar cache
        self._load_cache()

    def fetch_all_results(self, force_download=False):
        """Baixa todos os resultados da Mega-Sena"""
        
        # Tenta cache primeiro
        if not force_download and self._load_cache():
            print("📂 Dados carregados do cache")
            self._calculate_stats()
            return True

        print("📥 Baixando resultados...")
        
        try:
            response = requests.get(self.base_url, timeout=15)
            
            if response.status_code != 200:
                return False
            
            dados = response.json()
            self.all_contests = []
            self.all_results = []
            
            for item in dados:
                numeros = item.get('dezenas', [])
                concurso = item.get('concurso')
                
                if numeros and concurso:
                    nums = sorted([int(d) for d in numeros])
                    self.all_results.append(nums)
                    self.all_contests.append({
                        'concurso': concurso,
                        'data': item.get('data'),
                        'numeros': nums,
                        'acumulado': item.get('acumulou', False)
                    })
            
            if self.all_contests:
                self.last_result = self.all_contests[-1]
            
            self._calculate_stats()
            self._save_cache()
            return True
            
        except Exception as e:
            print(f"Erro: {e}")
            return False

    def get_latest_result(self):
        """Busca apenas o último resultado"""
        try:
            response = requests.get(f"{self.base_url}/latest", timeout=5)
            if response.status_code == 200:
                data = response.json()
                numeros = sorted([int(d) for d in data.get('dezenas', [])])
                return {
                    'concurso': data.get('concurso'),
                    'data': data.get('data'),
                    'numeros': numeros,
                    'acumulado': data.get('acumulou', False)
                }
            return None
        except:
            return None

    def _calculate_stats(self):
        """Calcula estatísticas"""
        if not self.all_results:
            return
        
        numbers = []
        for game in self.all_results:
            numbers.extend(game)
        
        freq = Counter(numbers)
        
        # Pares
        pairs = Counter()
        for game in self.all_results:
            g = sorted(game)
            for i in range(len(g)):
                for j in range(i+1, len(g)):
                    pairs[(g[i], g[j])] += 1
        
        all_freq = freq.most_common()
        hot = [n for n, _ in all_freq[:20]]
        cold = [n for n, _ in all_freq[-20:]]
        
        self.stats = {
            'frequencies': freq,
            'pairs': pairs,
            'hot_numbers': hot,
            'cold_numbers': cold,
            'total_games': len(self.all_results),
            'last_result': self.last_result
        }

    def _save_cache(self):
        """Salva cache"""
        try:
            data = {
                'results': self.all_results,
                'contests': self.all_contests,
                'last_result': self.last_result,
                'stats': self.stats
            }
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except:
            pass

    def _load_cache(self):
        """Carrega cache"""
        if not os.path.exists(self.cache_file):
            return False
        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
            self.all_results = data.get('results', [])
            self.all_contests = data.get('contests', [])
            self.last_result = data.get('last_result')
            self.stats = data.get('stats')
            return True
        except:
            return False

    def comprehensive_analysis(self):
        """Retorna análise"""
        return self.stats