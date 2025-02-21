from datetime import datetime, timedelta

class Contato:
    """Classe para armazenar informações de contato de uma pessoa"""
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Item:
    """Classe base para qualquer item que pode ser emprestado"""
    def __init__(self, nome, tipo, identificador):
        self.nome = nome
        self.tipo = tipo  # livro, ferramenta, jogo, etc
        self.identificador = identificador  # código único do item
        self.disponivel = True
        self.emprestimo_atual = None

class Livro(Item):
    """Classe específica para livros, herda de Item"""
    def __init__(self, titulo, autor, isbn):
        super().__init__(titulo, "livro", isbn)
        self.autor = autor
        self.isbn = isbn

class Emprestimo:
    """Registra informações sobre um empréstimo"""
    def __init__(self, item, contato, data_emprestimo):
        self.item = item
        self.contato = contato
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_emprestimo + timedelta(days=14)
        self.data_devolucao_real = None

class SistemaEmprestimos:
    """Sistema que gerencia todos os empréstimos"""
    def __init__(self):
        self.itens = {}  # identificador -> Item
        self.contatos = {}  # telefone -> Contato
        self.emprestimos = []

    def cadastrar_contato(self, nome, telefone):
        """Cadastra um novo contato no sistema"""
        if telefone in self.contatos:
            return f"Contato com telefone {telefone} já existe."
        
        contato = Contato(nome, telefone)
        self.contatos[telefone] = contato
        return f"Contato {nome} cadastrado com sucesso."

    def cadastrar_livro(self, titulo, autor, isbn):
        """Cadastra um novo livro no sistema"""
        if isbn in self.itens:
            return f"Livro com ISBN {isbn} já existe."
        
        livro = Livro(titulo, autor, isbn)
        self.itens[isbn] = livro
        return f"Livro '{titulo}' cadastrado com sucesso."

    def cadastrar_item(self, nome, tipo, identificador):
        """Cadastra um novo item genérico no sistema"""
        if identificador in self.itens:
            return f"Item com identificador {identificador} já existe."
        
        item = Item(nome, tipo, identificador)
        self.itens[identificador] = item
        return f"Item '{nome}' cadastrado com sucesso."

    def emprestar_item(self, identificador, telefone):
        """Registra o empréstimo de um item"""
        if identificador not in self.itens:
            return f"Item com identificador {identificador} não encontrado."
        
        if telefone not in self.contatos:
            return f"Contato com telefone {telefone} não encontrado."
            
        item = self.itens[identificador]
        if not item.disponivel:
            return f"Item '{item.nome}' já está emprestado."
        
        contato = self.contatos[telefone]
        emprestimo = Emprestimo(item, contato, datetime.now())
        item.disponivel = False
        item.emprestimo_atual = emprestimo
        self.emprestimos.append(emprestimo)
        
        return f"Item '{item.nome}' emprestado para {contato.nome}."

    def devolver_item(self, identificador):
        """Registra a devolução de um item"""
        if identificador not in self.itens:
            return f"Item com identificador {identificador} não encontrado."
            
        item = self.itens[identificador]
        if item.disponivel:
            return f"Item '{item.nome}' não está emprestado."
        
        emprestimo = item.emprestimo_atual
        emprestimo.data_devolucao_real = datetime.now()
        item.disponivel = True
        item.emprestimo_atual = None
        
        return f"Item '{item.nome}' devolvido com sucesso."

    def listar_itens(self):
        """Lista todos os itens cadastrados"""
        return [
            f"ID: {id} - '{item.nome}' - Tipo: {item.tipo} - "
            f"{'Disponível' if item.disponivel else 'Emprestado'}"
            for id, item in self.itens.items()
        ]

    def listar_emprestimos_ativos(self):
        """Lista todos os empréstimos ativos"""
        emprestimos_ativos = [
            emp for emp in self.emprestimos 
            if emp.data_devolucao_real is None
        ]
        return [
            f"Item: '{emp.item.nome}' - Emprestado para: {emp.contato.nome} "
            f"(Tel: {emp.contato.telefone}) - "
            f"Data: {emp.data_emprestimo.strftime('%d/%m/%Y')} - "
            f"Devolução prevista: {emp.data_devolucao_prevista.strftime('%d/%m/%Y')}"
            for emp in emprestimos_ativos
        ]

# Exemplo de uso do sistema
def exemplo_uso():
    sistema = SistemaEmprestimos()
    
    # Cadastrando contatos
    print(sistema.cadastrar_contato("João Silva", "11999887766"))
    print(sistema.cadastrar_contato("Maria Santos", "11999887755"))
    
    # Cadastrando diferentes tipos de itens
    print(sistema.cadastrar_livro("Dom Casmurro", "Machado de Assis", "123"))
    print(sistema.cadastrar_item("Furadeira", "ferramenta", "001"))
    print(sistema.cadastrar_item("Switch", "videogame", "002"))
    
    # Emprestando itens
    print(sistema.emprestar_item("123", "11999887766"))  # Emprestando livro
    print(sistema.emprestar_item("001", "11999887755"))  # Emprestando furadeira
    
    # Listando itens e empréstimos
    print("\nLista de itens:")
    for item in sistema.listar_itens():
        print(item)
        
    print("\nEmpréstimos ativos:")
    for emprestimo in sistema.listar_emprestimos_ativos():
        print(emprestimo)
    
    # Devolvendo um item
    print("\nDevolvendo item:")
    print(sistema.devolver_item("123"))

if __name__ == "__main__":
    exemplo_uso()