import json

class Produto:
    def __init__(self, nome: str = None, preco: float = None) -> None:
        self.nome = nome
        self.preco = preco
        
    def dump(self):
        return json.dumps({
            "nome": self.nome,
            "preco": self.preco,
        })
    
    def load(self, data: dict):
        self.nome = data["nome"]
        self.preco = data["preco"]

    def __str__(self) -> str:
        return f"{self.nome} - R${self.preco:.2f}"
      
produtos = {
  1: Produto("Coca-Cola", 5.00),
  2: Produto("Pepsi", 4.00),
  3: Produto("Guaraná", 3.00),
  4: Produto("Fanta", 2.00),
  5: Produto("Sprite", 1.00),
}