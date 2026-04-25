from dataclasses import dataclass

@dataclass
class Livro:
    id: int
    titulo: str
    livraria: str

    def formatar_localizacao(self) -> str:
       return f"{self.titulo} (Disponível em: {self.livraria})"
    
    def pertence_a_livraria(self, nome_livraria: str) -> bool:
        return self.livraria.lower() == nome_livraria.lower()